"""ThermoMaven API wrapper."""
import asyncio
import hashlib
import json
import logging
import random
import ssl
import tempfile
import time
import uuid
from typing import Any

import aiohttp
import paho.mqtt.client as mqtt
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.primitives import serialization

from homeassistant.core import HomeAssistant

from .const import API_BASE_URL_COM, API_BASE_URL_DE, EUROPEAN_COUNTRIES, MQTT_BROKERS, MQTT_PORT

_LOGGER = logging.getLogger(__name__)


class ThermoMavenAPI:
    """ThermoMaven API client."""

    def __init__(
        self,
        hass: HomeAssistant,
        email: str,
        password: str,
        app_key: str,
        app_id: str,
        region: str = "US",
    ):
        """Initialize the API."""
        self.hass = hass
        self.email = email
        self.password = password
        self.app_key = app_key
        self.app_id = app_id
        self.region = region
        self.token = None
        self.user_id = None
        self.device_sn = "".join(random.choices("0123456789abcdef", k=16))
        self._mqtt_device_list_received = False  # Flag pour savoir si on a reçu la liste MQTT
        
        # Determine API base URL based on region
        if region in EUROPEAN_COUNTRIES:
            self.api_base_url = API_BASE_URL_DE
            _LOGGER.debug("Using European API (DE) for region %s", region)
        else:
            self.api_base_url = API_BASE_URL_COM
            _LOGGER.debug("Using Global API (COM) for region %s", region)
        
        self.mqtt_client = None
        self.mqtt_config = None
        self.coordinator = None
        self._latest_mqtt_data = None
        
        # Fichiers temporaires pour les certificats
        self.cert_files = []

    def _generate_sign(self, params_str: str, body_str: str = "") -> str:
        """Generate MD5 signature."""
        sign_str = self.app_key + "|" + params_str
        if body_str:
            sign_str += "|" + body_str
        sign_str = sign_str.replace("\n", "")
        return hashlib.md5(sign_str.encode("utf-8")).hexdigest()

    def _build_headers(self, body: dict | None = None) -> dict:
        """Build request headers with signature."""
        timestamp = str(int(time.time() * 1000))
        nonce = str(uuid.uuid4()).replace("-", "").lower()
        token_value = self.token if self.token else "none"

        params = {
            "x-appId": self.app_id,
            "x-appVersion": "1804",
            "x-deviceSn": self.device_sn,
            "x-lang": "en_US",
            "x-nonce": nonce,
            "x-region": self.region,
            "x-timestamp": timestamp,
            "x-token": token_value,
        }

        params_sorted = sorted(params.items())
        params_str = ";".join([f"{k}={v}" for k, v in params_sorted])

        if body:
            body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        else:
            body_str = ""

        sign = self._generate_sign(params_str, body_str)

        headers = params.copy()
        headers["x-sign"] = sign
        headers["Content-Type"] = "application/json"
        headers["User-Agent"] = "okhttp/4.12.0"

        return headers

    async def async_login(self) -> dict[str, Any]:
        """Login to ThermoMaven API."""
        endpoint = f"{self.api_base_url}/app/account/login"
        password_md5 = hashlib.md5(self.password.encode("utf-8")).hexdigest()

        payload = {
            "accountName": self.email,
            "accountPassword": password_md5,
            "deviceInfo": "google sdk_gphone_x86_64 11",
        }

        headers = self._build_headers(payload)
        body_str = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint, data=body_str, headers=headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == "0":
                        self.token = data["data"]["token"]
                        self.user_id = data["data"]["userId"]
                        _LOGGER.debug("Login successful for user %s", self.email)
                        return data
                raise Exception(f"Login failed: {await response.text()}")

    async def async_get_devices(self) -> list[dict]:
        """Get list of devices."""
        _LOGGER.debug("=== API DEVICE REQUEST ===")
        
        my_devices = await self._async_request("POST", "/app/device/share/my/device/list", {})
        shared_devices = await self._async_request("POST", "/app/device/share/shared/device/list", {})
        
        _LOGGER.debug("My devices response: %s", json.dumps(my_devices, indent=2))
        _LOGGER.debug("Shared devices response: %s", json.dumps(shared_devices, indent=2))
        
        devices = []
        if my_devices and my_devices.get("code") == "0":
            my_data = my_devices.get("data", [])
            devices.extend(my_data)
            
        if shared_devices and shared_devices.get("code") == "0":
            shared_data = shared_devices.get("data", [])
            devices.extend(shared_data)
        
        _LOGGER.debug("API returned: %d devices (My: %d, Shared: %d)", 
                    len(devices),
                    len(my_data) if my_devices and my_devices.get("code") == "0" else 0,
                    len(shared_data) if shared_devices and shared_devices.get("code") == "0" else 0)
            
        return devices

    async def async_get_user_info(self) -> dict:
        """Get user information."""
        result = await self._async_request("POST", "/app/user/get", {})
        if result and result.get("code") == "0":
            return result.get("data", {})
        return {}

    async def async_get_mqtt_certificate(self) -> dict:
        """Get MQTT certificate configuration."""
        result = await self._async_request("POST", "/app/mqtt/cert/apply", {})
        if result and result.get("code") == "0":
            return result.get("data", {})
        return {}

    async def _async_request(self, method: str, endpoint: str, body: dict) -> dict:
        """Make an authenticated request."""
        url = f"{self.api_base_url}{endpoint}"
        headers = self._build_headers(body)
        
        if body:
            body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        else:
            body_str = ""

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, data=body_str if body else None, headers=headers
            ) as response:
                if response.status == 200:
                    return await response.json()
                _LOGGER.error(
                    "Request to %s failed: %s", endpoint, await response.text()
                )
                return {}

    async def async_wait_for_mqtt_device_list(self, timeout=10):
        """Wait for MQTT to receive the device list."""
        _LOGGER.debug("⏳ Waiting for MQTT device list (timeout: %ds)...", timeout)
        start_time = time.time()
        
        # Vérifier aussi que c'est bien un user:device:list et pas un status:report
        while not self._mqtt_device_list_received or \
              self._latest_mqtt_data.get("cmdType") != "user:device:list":
            if time.time() - start_time > timeout:
                _LOGGER.warning("⚠️ Timeout waiting for MQTT device list after %ds", timeout)
                _LOGGER.warning("Last MQTT cmdType: %s", 
                              self._latest_mqtt_data.get("cmdType") if self._latest_mqtt_data else "None")
                return False
            await asyncio.sleep(0.5)  # Check every 500ms
        
        _LOGGER.debug("✅ MQTT device list received in %.1fs", time.time() - start_time)
        return True
    
    async def async_setup_mqtt(self, coordinator):
        """Setup MQTT connection."""
        self.coordinator = coordinator
        
        # Reset flag and latest data to wait for fresh device list
        self._mqtt_device_list_received = False
        self._latest_mqtt_data = None  # Effacer les anciennes données MQTT
        _LOGGER.debug("🔄 Reset MQTT flag and data, waiting for fresh device list...")
        
        # Check if MQTT is already running (reload case)
        mqtt_already_running = self.mqtt_client is not None and hasattr(self.mqtt_client, '_thread') and self.mqtt_client._thread is not None
        
        if mqtt_already_running:
            _LOGGER.debug("♻️ MQTT already running, forcing device list refresh...")
            # Trigger device sync to get a fresh user:device:list
            await self._trigger_device_sync()
            # Pas besoin de re-setup MQTT, juste attendre le nouveau message
        else:
            # Get MQTT certificate
            self.mqtt_config = await self.async_get_mqtt_certificate()
            if not self.mqtt_config:
                _LOGGER.error("Failed to get MQTT certificate")
                return False

            # Download and convert certificate in executor
            await self.hass.async_add_executor_job(self._setup_mqtt_sync)
            
            # Trigger initial device sync after MQTT setup
            # The on_connect callback will also trigger sync, but this ensures it happens
            # even if there's a timing issue with MQTT connection
            await asyncio.sleep(2)  # Give MQTT time to connect
            await self._trigger_device_sync()
        
        return True

    def _setup_mqtt_sync(self):
        """Setup MQTT synchronously (runs in executor)."""
        import requests
        
        # Download P12 certificate
        response = requests.get(self.mqtt_config["p12Url"])
        if response.status_code != 200:
            _LOGGER.error("Failed to download P12 certificate")
            return False
        
        p12_file = tempfile.NamedTemporaryFile(delete=False, suffix=".p12")
        p12_file.write(response.content)
        p12_file.close()
        self.cert_files.append(p12_file.name)
        
        # Convert P12 to PEM
        with open(p12_file.name, "rb") as f:
            p12_data = f.read()
        
        private_key, certificate, _ = pkcs12.load_key_and_certificates(
            p12_data, self.mqtt_config["p12Password"].encode()
        )
        
        # Save certificate
        cert_pem = certificate.public_bytes(serialization.Encoding.PEM)
        cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".crt", mode="wb")
        cert_file.write(cert_pem)
        cert_file.close()
        self.cert_files.append(cert_file.name)
        
        # Save private key
        key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".key", mode="wb")
        key_file.write(key_pem)
        key_file.close()
        self.cert_files.append(key_file.name)
        
        # Setup MQTT client
        client_id = self.mqtt_config["clientId"]
        region = client_id.split("-")[2] if "-" in client_id else "US"
        broker = MQTT_BROKERS.get(region, MQTT_BROKERS["US"])
        
        self.mqtt_client = mqtt.Client(
            client_id=client_id,
            protocol=mqtt.MQTTv311,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
        )
        
        self.mqtt_client.on_connect = self._on_mqtt_connect
        self.mqtt_client.on_message = self._on_mqtt_message
        self.mqtt_client.on_disconnect = self._on_mqtt_disconnect
        
        # Configure TLS
        self.mqtt_client.tls_set(
            certfile=cert_file.name,
            keyfile=key_file.name,
            cert_reqs=ssl.CERT_REQUIRED,
            tls_version=ssl.PROTOCOL_TLSv1_2,
        )
        
        # Connect
        self.mqtt_client.connect(broker, MQTT_PORT, keepalive=60)
        self.mqtt_client.loop_start()
        
        _LOGGER.debug("MQTT client started for region %s", region)
        return True

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        """Handle MQTT connection."""
        if rc == 0:
            _LOGGER.debug("Connected to MQTT broker")
            # Subscribe to topics
            for topic in self.mqtt_config["subTopics"]:
                client.subscribe(topic)
                _LOGGER.debug("Subscribed to %s", topic)
            
            # Trigger device list sync by calling API endpoints
            # This will cause the MQTT broker to publish user:device:list message
            _LOGGER.debug("Triggering device list synchronization via API")
            self.hass.add_job(self._trigger_device_sync())
        else:
            _LOGGER.error("Failed to connect to MQTT broker: %s", rc)

    def _on_mqtt_message(self, client, userdata, msg):
        """Handle MQTT message."""
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            cmd_type = data.get("cmdType", "")
            
            # Log compact header
            _LOGGER.debug("📨 MQTT: %s on %s", cmd_type, msg.topic)
            
            # Full message only at debug level
            _LOGGER.debug("Full message: %s", json.dumps(data, indent=2))
            
            # Store the latest message data for coordinator
            self._latest_mqtt_data = data
            
            # Trigger coordinator update on device list changes
            if cmd_type == "user:device:list":
                # Log the device data for debugging
                cmd_data = data.get("cmdData", {})
                devices = cmd_data.get("devices", [])
                _LOGGER.debug("Device list updated via MQTT: %d devices found", len(devices))
                
                # Marquer que la liste MQTT a été reçue
                self._mqtt_device_list_received = True
                _LOGGER.debug("✅ MQTT device list received and processed")
                
                # Log device details for debugging
                for device in devices:
                    device_id = device.get("deviceId")
                    device_name = device.get("deviceName", "Unknown")
                    device_sn = device.get("deviceSn", "Unknown")
                    _LOGGER.debug("MQTT Device: %s, ID: %s, SN: %s", device_name, device_id, device_sn)
                
                _LOGGER.debug("Full MQTT device data: %s", json.dumps(devices, indent=2))
                
                # Subscribe to each device's topic for real-time updates
                for device in devices:
                    device_topics = device.get("subTopics", [])
                    for topic in device_topics:
                        _LOGGER.debug("Subscribing to device topic: %s", topic)
                        self.mqtt_client.subscribe(topic)
                
                if self.coordinator:
                    self.hass.add_job(self.coordinator.async_request_refresh())
            
            # Handle temperature updates
            elif "status:report" in cmd_type:
                _LOGGER.debug("=== TEMPERATURE UPDATE VIA MQTT ===")
                device_id = data.get("deviceId")
                cmd_data = data.get("cmdData", {})
                
                # Log compact info instead of full JSON
                temp = "N/A"
                probes = cmd_data.get("probes", [])
                if probes:
                    cur_temp = probes[0].get("curTemperature")
                    if cur_temp:
                        temp_f = cur_temp / 10.0
                        temp = f"{temp_f}°F"
                
                _LOGGER.debug("🌡️ Temperature update: Device %s = %s (Battery: %s%%)", 
                           device_id, temp, cmd_data.get("batteryValue", "?"))
                
                # Store the status report data for the coordinator to use
                if self.coordinator:
                    _LOGGER.debug("Triggering coordinator refresh for temperature update")
                    self.hass.add_job(self.coordinator.async_request_refresh())
                else:
                    _LOGGER.warning("No coordinator available for temperature update")
                    
        except Exception as err:
            _LOGGER.error("Error processing MQTT message: %s", err)

    def _on_mqtt_disconnect(self, client, userdata, rc):
        """Handle MQTT disconnection."""
        if rc != 0:
            _LOGGER.warning("Unexpected MQTT disconnection: %s", rc)

    async def _trigger_device_sync(self):
        """Trigger device synchronization by calling API endpoints.
        
        This causes the MQTT broker to publish the user:device:list message,
        which is needed for device discovery.
        """
        try:
            # Small delay to ensure MQTT subscription is active
            await asyncio.sleep(1)
            
            _LOGGER.debug("Calling API endpoints to trigger MQTT device list...")
            # These API calls will trigger the MQTT broker to send user:device:list
            await self.async_get_devices()
            _LOGGER.debug("Device sync triggered successfully")
        except Exception as err:
            _LOGGER.error("Failed to trigger device sync: %s", err)

    async def async_disconnect_mqtt(self):
        """Disconnect MQTT client."""
        if self.mqtt_client:
            await self.hass.async_add_executor_job(self.mqtt_client.disconnect)
            await self.hass.async_add_executor_job(self.mqtt_client.loop_stop)
        
        # Clean up certificate files
        for file_path in self.cert_files:
            try:
                import os
                os.unlink(file_path)
            except Exception:
                pass

