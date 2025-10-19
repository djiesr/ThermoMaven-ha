"""
ThermoMaven integration for Home Assistant.
"""
import asyncio
import logging
import time
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_REGION
from .thermomaven_api import ThermoMavenAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR, Platform.CLIMATE]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThermoMaven from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]
    app_key = entry.data.get("app_key", "bcd4596f1bb8419a92669c8017bf25e8")
    app_id = entry.data.get("app_id", "ap4060eff28137181bd")
    region = entry.data.get(CONF_REGION, "US")

    # Créer l'API client
    api = ThermoMavenAPI(hass, email, password, app_key, app_id, region)
    
    # Se connecter
    try:
        await api.async_login()
    except Exception as err:
        _LOGGER.error("Failed to login to ThermoMaven: %s", err)
        return False

    # Créer le coordinator pour les mises à jour
    coordinator = ThermoMavenDataUpdateCoordinator(hass, api)
    
    # Stocker l'API et le coordinator AVANT le setup
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    # Setup MQTT AVANT le premier refresh pour avoir les données MQTT disponibles
    _LOGGER.debug("⏳ Setting up MQTT before first data refresh...")
    await api.async_setup_mqtt(coordinator)
    
    # Attendre que MQTT reçoive la liste des appareils (max 10 secondes)
    mqtt_ready = await api.async_wait_for_mqtt_device_list(timeout=10)
    
    if mqtt_ready:
        _LOGGER.debug("✅ MQTT device list ready, proceeding with data refresh")
    else:
        _LOGGER.warning("⚠️ Proceeding without MQTT device list (timeout)")
    
    # Maintenant faire le premier refresh avec les données MQTT disponibles
    _LOGGER.debug("🔄 Performing first data refresh with MQTT data...")
    await coordinator.async_config_entry_first_refresh()

    # Register services
    async def handle_sync_devices(call):
        """Handle the sync_devices service call."""
        _LOGGER.debug("Manual device sync requested via service")
        # Reset auto-sync counter to allow new attempts
        coordinator._auto_sync_attempts = 0
        await api._trigger_device_sync()
        await coordinator.async_request_refresh()
    
    hass.services.async_register(DOMAIN, "sync_devices", handle_sync_devices)

    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # NOUVEAU: Forcer une mise à jour après setup des platforms pour réveiller les entités
    await asyncio.sleep(2)
    _LOGGER.debug("🔄 Post-setup refresh to ensure entities are updated...")
    await coordinator.async_request_refresh()

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        # Disconnect MQTT
        api = hass.data[DOMAIN][entry.entry_id]["api"]
        await api.async_disconnect_mqtt()
        
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Unregister services if no more entries
        if not hass.data[DOMAIN]:
            hass.services.async_remove(DOMAIN, "sync_devices")

    return unload_ok


class ThermoMavenDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ThermoMaven data."""

    def __init__(self, hass: HomeAssistant, api: ThermoMavenAPI):
        """Initialize."""
        self.api = api
        self._auto_sync_attempts = 0
        self._max_auto_sync_attempts = 3  # Limite pour éviter de spammer l'API
        self._merged_devices_cache = {}  # Cache des devices fusionnés (deviceName -> device)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=300),  # 5 minutes (MQTT is primary)
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            _LOGGER.debug("=== COORDINATOR UPDATE START ===")
            
            # Interroger l'API seulement si nécessaire (démarrage ou toutes les 5 minutes)
            current_time = time.time()
            should_fetch_api = (
                not hasattr(self, '_last_api_fetch') or 
                current_time - self._last_api_fetch > 300  # 5 minutes
            )
            
            if should_fetch_api:
                _LOGGER.debug("📡 Fetching fresh API data (last fetch: %s)", 
                           getattr(self, '_last_api_fetch', 'never'))
                devices = await self.api.async_get_devices()
                user_info = await self.api.async_get_user_info()
                self._last_api_fetch = current_time
                self._api_devices = devices  # Stocker les données API
                _LOGGER.debug("API devices: %s", [{"name": d.get("deviceName"), "id": d.get("deviceId")} for d in devices] if devices else [])
            else:
                _LOGGER.debug("🔄 Using cached API data (last fetch: %s ago)", 
                           int(current_time - self._last_api_fetch))
                devices = getattr(self, '_api_devices', [])
                user_info = {}  # Pas besoin de user_info pour les mises à jour de température
            
            # If no devices are returned and MQTT client exists, trigger a sync
            # Limited to prevent API spam if thermometer is offline
            if not devices and self.api.mqtt_client:
                if self._auto_sync_attempts < self._max_auto_sync_attempts:
                    self._auto_sync_attempts += 1
                    _LOGGER.debug(
                        "No devices found, triggering MQTT sync (attempt %d/%d)",
                        self._auto_sync_attempts,
                        self._max_auto_sync_attempts
                    )
                    await self.api._trigger_device_sync()
                else:
                    _LOGGER.debug(
                        "Max auto-sync attempts reached. Use 'thermomaven.sync_devices' service to retry manually."
                    )
            
            # Utiliser les données précédentes si disponibles
            if hasattr(self, 'data') and self.data:
                previous_devices = self.data.get("devices", [])
            else:
                previous_devices = []
            
            # Enrichir les données API avec le cache si deviceId est manquant
            if devices and self._merged_devices_cache:
                _LOGGER.debug("🔍 Checking for devices with missing deviceId...")
                for device in devices:
                    if not device.get("deviceId") or device.get("deviceId") == "None":
                        device_name = device.get("deviceName")
                        if device_name and device_name in self._merged_devices_cache:
                            cached_device = self._merged_devices_cache[device_name]
                            device["deviceId"] = cached_device.get("deviceId")
                            device["deviceSn"] = cached_device.get("deviceSn")
                            _LOGGER.debug("✅ Restored deviceId from cache for: %s (ID: %s)", 
                                       device_name, device.get("deviceId"))
                        else:
                            _LOGGER.warning("⚠️ No cache found for device: %s", device_name)
            
            # Fusionner les données API et MQTT en utilisant deviceName comme clé
            if self.api._latest_mqtt_data:
                mqtt_data = self.api._latest_mqtt_data
                _LOGGER.debug("=== FUSION API + MQTT DATA ===")
                _LOGGER.debug("MQTT cmdType: %s", mqtt_data.get("cmdType"))
                
                if mqtt_data.get("cmdType") == "user:device:list":
                    mqtt_devices = mqtt_data.get("cmdData", {}).get("devices", [])
                    _LOGGER.debug("MQTT device list: %d devices", len(mqtt_devices))
                    _LOGGER.debug("MQTT devices: %s", [{"name": d.get("deviceName"), "id": d.get("deviceId")} for d in mqtt_devices] if mqtt_devices else [])
                    
                    if mqtt_devices:
                        # Fusionner les données API et MQTT
                        merged_devices = []
                        
                        # Créer un dictionnaire des appareils API par nom
                        api_devices_by_name = {}
                        for api_device in devices:
                            device_name = api_device.get("deviceName")
                            if device_name:
                                api_devices_by_name[device_name] = api_device
                        
                        _LOGGER.debug("API devices by name: %s", list(api_devices_by_name.keys()))
                        
                        # Fusionner chaque appareil MQTT avec les données API correspondantes
                        for mqtt_device in mqtt_devices:
                            device_name = mqtt_device.get("deviceName")
                            _LOGGER.debug("Processing MQTT device: %s", device_name)
                            
                            # Commencer avec les données MQTT (plus complètes)
                            merged_device = mqtt_device.copy()
                            
                            # Ajouter les données API si disponibles
                            if device_name in api_devices_by_name:
                                api_device = api_devices_by_name[device_name]
                                _LOGGER.debug("✅ Found matching API device for: %s", device_name)
                                
                                # Ajouter les métadonnées API manquantes
                                merged_device.update({
                                    "deviceShareId": api_device.get("deviceShareId"),
                                    "fromUserName": api_device.get("fromUserName"),
                                    "shareStatus": api_device.get("shareStatus"),
                                })
                                
                                _LOGGER.debug("Merged device: %s (ID: %s, ShareID: %s, has lastStatusCmd: %s)", 
                                            device_name, 
                                            merged_device.get("deviceId"),
                                            merged_device.get("deviceShareId"),
                                            "lastStatusCmd" in merged_device)
                            else:
                                _LOGGER.debug("⚠️ No matching API device found for: %s", device_name)
                            
                            merged_devices.append(merged_device)
                            
                            # Sauvegarder dans le cache (par nom ET par ID)
                            if device_name:
                                self._merged_devices_cache[device_name] = merged_device
                            device_id = merged_device.get("deviceId")
                            if device_id:
                                self._merged_devices_cache[str(device_id)] = merged_device
                        
                        _LOGGER.debug("✅ Fusion complete: %d merged devices", len(merged_devices))
                        _LOGGER.debug("Merged devices: %s", [{"name": d.get("deviceName"), "id": d.get("deviceId")} for d in merged_devices])
                        _LOGGER.debug("💾 Cached %d device mappings", len(self._merged_devices_cache))
                        devices = merged_devices
                    else:
                        _LOGGER.warning("MQTT device list is empty")
                        
                elif "status:report" in mqtt_data.get("cmdType", ""):
                    # Mettre à jour les données de température des appareils existants
                    device_id = mqtt_data.get("deviceId")
                    _LOGGER.debug("=== PROCESSING TEMPERATURE UPDATE ===")
                    _LOGGER.debug("Status report for device ID: %s", device_id)
                    _LOGGER.debug("Current devices: %d, Previous devices: %d", 
                                len(devices) if devices else 0, len(previous_devices))
                    
                    # Utiliser les appareils précédents si l'API n'en retourne pas
                    if not devices and previous_devices:
                        devices = previous_devices
                        _LOGGER.debug("Using previous device list: %d devices", len(devices))
                    
                    if device_id and devices:
                        device_found = False
                        for device in devices:
                            device_device_id = str(device.get("deviceId"))
                            if device_device_id == str(device_id):
                                # Mettre à jour les données de température
                                device["lastStatusCmd"] = mqtt_data
                                
                                # Extraire les données de température pour debug
                                cmd_data = mqtt_data.get("cmdData", {})
                                probes = cmd_data.get("probes", [])
                                temp_str = "N/A"
                                if probes:
                                    probe_data = probes[0]
                                    temp_raw = probe_data.get("curTemperature")
                                    if temp_raw:
                                        temp_f = temp_raw / 10.0
                                        temp_c = (temp_f - 32) * 5/9
                                        temp_str = f"{temp_f}°F ({round(temp_c, 1)}°C)"
                                
                                _LOGGER.debug("✅ Temperature updated: %s = %s", device.get("deviceName"), temp_str)
                                device_found = True
                                break
                        
                        if not device_found:
                            _LOGGER.warning("❌ Device ID %s not found in device list", device_id)
                            _LOGGER.debug("Available device IDs: %s", [str(d.get("deviceId")) for d in devices])
                            
                            # Ne créer un nouveau device que si nécessaire
                            # D'abord vérifier si le device avec ce deviceId existe déjà
                            # (peut avoir été restauré depuis le cache)
                            device_exists_with_valid_id = any(
                                str(d.get("deviceId")) == str(device_id) and 
                                d.get("deviceId") not in [None, "None"]
                                for d in devices
                            )
                            
                            if device_exists_with_valid_id:
                                _LOGGER.debug("ℹ️ Device %s already exists with valid ID, skipping creation", device_id)
                                # Juste mettre à jour le lastStatusCmd du device existant
                                for device in devices:
                                    if str(device.get("deviceId")) == str(device_id):
                                        device["lastStatusCmd"] = mqtt_data
                                        _LOGGER.debug("✅ Updated existing device with temperature data")
                                        break
                            else:
                                # Essayer de trouver l'appareil dans le cache d'abord
                                cached_device = self._merged_devices_cache.get(str(device_id))
                                
                                if cached_device:
                                    _LOGGER.debug("💾 Found device in cache by ID: %s", device_id)
                                    merged_device = cached_device.copy()
                                    merged_device["lastStatusCmd"] = mqtt_data
                                else:
                                    # Essayer de fusionner avec un appareil API existant par nom
                                    device_name = None
                                    api_device = None
                                    for api_dev in getattr(self, '_api_devices', []):
                                        if api_dev.get("deviceName"):
                                            device_name = api_dev.get("deviceName")
                                            api_device = api_dev
                                            break
                                    
                                    if device_name and api_device:
                                        _LOGGER.debug("🔧 Creating merged device with API name: %s", device_name)
                                        merged_device = {
                                            "deviceId": device_id,
                                            "deviceName": device_name,
                                            "deviceModel": mqtt_data.get("deviceModel", "Unknown"),
                                            "deviceSn": mqtt_data.get("deviceSn"),
                                            "lastStatusCmd": mqtt_data,
                                            "deviceShareId": api_device.get("deviceShareId"),
                                            "fromUserName": api_device.get("fromUserName"),
                                            "shareStatus": api_device.get("shareStatus"),
                                        }
                                    else:
                                        _LOGGER.debug("🔧 Creating device from MQTT data only")
                                        merged_device = {
                                            "deviceId": device_id,
                                            "deviceName": f"ThermoMaven Device {device_id}",
                                            "deviceModel": mqtt_data.get("deviceModel", "Unknown"),
                                            "deviceSn": mqtt_data.get("deviceSn"),
                                            "lastStatusCmd": mqtt_data
                                        }
                                    
                                    # Sauvegarder dans le cache
                                    if device_name:
                                        self._merged_devices_cache[device_name] = merged_device
                                    self._merged_devices_cache[str(device_id)] = merged_device
                                
                                devices.append(merged_device)
                                _LOGGER.debug("✅ Created/Updated merged device: %s (ID: %s)", 
                                             merged_device.get("deviceName"), merged_device.get("deviceId"))
                    else:
                        _LOGGER.warning("❌ Cannot update device %s: device_id=%s, devices=%s", 
                                       device_id, device_id, len(devices) if devices else 0)
            
            # Si on n'a pas de données d'appareils mais qu'on en avait avant, les conserver
            if not devices and previous_devices:
                devices = previous_devices
                _LOGGER.debug("No new device data, keeping previous: %d devices", len(devices))
            
            # Dédupliquer les appareils (par deviceId)
            if devices:
                seen_ids = set()
                unique_devices = []
                for device in devices:
                    device_id = str(device.get("deviceId"))
                    if device_id not in seen_ids:
                        seen_ids.add(device_id)
                        unique_devices.append(device)
                    else:
                        _LOGGER.debug("🔄 Skipping duplicate device: %s (ID: %s)", 
                                     device.get("deviceName"), device_id)
                
                if len(unique_devices) != len(devices):
                    _LOGGER.debug("🧹 Deduplicated: %d → %d devices", len(devices), len(unique_devices))
                    devices = unique_devices
            
            _LOGGER.debug("=== FINAL: %d device(s) with lastStatusCmd: %s ===", 
                        len(devices) if devices else 0,
                        [bool(d.get("lastStatusCmd")) for d in devices] if devices else [])
            
            # Reset auto-sync counter if devices are found
            if devices:
                self._auto_sync_attempts = 0
            
            result = {
                "devices": devices,
                "user_info": user_info,
            }
            
            _LOGGER.debug("=== COORDINATOR UPDATE COMPLETE ===")
            return result
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

