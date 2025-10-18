"""
ThermoMaven integration for Home Assistant.
"""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .thermomaven_api import ThermoMavenAPI

_LOGGER = logging.getLogger(__name__)

PLATFORMS = [Platform.SENSOR]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up ThermoMaven from a config entry."""
    email = entry.data["email"]
    password = entry.data["password"]
    app_key = entry.data.get("app_key", "bcd4596f1bb8419a92669c8017bf25e8")
    app_id = entry.data.get("app_id", "ap4060eff28137181bd")

    # Créer l'API client
    api = ThermoMavenAPI(hass, email, password, app_key, app_id)
    
    # Se connecter
    try:
        await api.async_login()
    except Exception as err:
        _LOGGER.error("Failed to login to ThermoMaven: %s", err)
        return False

    # Créer le coordinator pour les mises à jour
    coordinator = ThermoMavenDataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()

    # Stocker l'API et le coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    # Setup MQTT si disponible
    await api.async_setup_mqtt(coordinator)

    # Register services
    async def handle_sync_devices(call):
        """Handle the sync_devices service call."""
        _LOGGER.info("Manual device sync requested via service")
        # Reset auto-sync counter to allow new attempts
        coordinator._auto_sync_attempts = 0
        await api._trigger_device_sync()
        await coordinator.async_request_refresh()
    
    hass.services.async_register(DOMAIN, "sync_devices", handle_sync_devices)

    # Forward entry setup to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

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
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=300),  # 5 minutes (MQTT is primary)
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # Récupérer les données (ou utiliser le cache)
            devices = await self.api.async_get_devices()
            user_info = await self.api.async_get_user_info()
            
            _LOGGER.debug("API returned %d devices", len(devices) if devices else 0)
            
            # If no devices are returned and MQTT client exists, trigger a sync
            # Limited to prevent API spam if thermometer is offline
            if not devices and self.api.mqtt_client:
                if self._auto_sync_attempts < self._max_auto_sync_attempts:
                    self._auto_sync_attempts += 1
                    _LOGGER.info(
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
            
            # Si on a des données MQTT plus récentes, les utiliser
            if self.api._latest_mqtt_data:
                mqtt_data = self.api._latest_mqtt_data
                _LOGGER.debug("Processing MQTT data with cmdType: %s", mqtt_data.get("cmdType"))
                
                if mqtt_data.get("cmdType") == "user:device:list":
                    mqtt_devices = mqtt_data.get("cmdData", {}).get("devices", [])
                    _LOGGER.info("MQTT device list: %d devices", len(mqtt_devices))
                    if mqtt_devices:
                        _LOGGER.info("Using MQTT device data: %d devices", len(mqtt_devices))
                        devices = mqtt_devices
                    else:
                        _LOGGER.warning("MQTT device list is empty")
                elif "status:report" in mqtt_data.get("cmdType", ""):
                    # Mettre à jour les données de température des appareils existants
                    device_id = mqtt_data.get("deviceId")
                    _LOGGER.debug("Status report for device %s", device_id)
                    
                    # Utiliser les appareils précédents si l'API n'en retourne pas
                    if not devices and previous_devices:
                        devices = previous_devices
                        _LOGGER.debug("Using previous device list: %d devices", len(devices))
                    
                    if device_id and devices:
                        for device in devices:
                            if str(device.get("deviceId")) == str(device_id):
                                # Mettre à jour les données de température
                                device["lastStatusCmd"] = mqtt_data
                                _LOGGER.info("Updated temperature data for device %s", device.get("deviceName"))
                                break
                    else:
                        _LOGGER.warning("Cannot update device %s: no devices in list", device_id)
            
            _LOGGER.info("Final device count: %d", len(devices) if devices else 0)
            
            # Reset auto-sync counter if devices are found
            if devices:
                self._auto_sync_attempts = 0
            
            return {
                "devices": devices,
                "user_info": user_info,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

