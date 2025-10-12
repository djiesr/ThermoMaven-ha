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

    return unload_ok


class ThermoMavenDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ThermoMaven data."""

    def __init__(self, hass: HomeAssistant, api: ThermoMavenAPI):
        """Initialize."""
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            # Récupérer les données
            devices = await self.api.async_get_devices()
            user_info = await self.api.async_get_user_info()
            
            # Si on a des données MQTT plus récentes, les utiliser
            if self.api._latest_mqtt_data:
                mqtt_data = self.api._latest_mqtt_data
                if mqtt_data.get("cmdType") == "user:device:list":
                    mqtt_devices = mqtt_data.get("cmdData", {}).get("devices", [])
                    if mqtt_devices:
                        _LOGGER.info("Using MQTT device data: %d devices", len(mqtt_devices))
                        devices = mqtt_devices
                elif "status:report" in mqtt_data.get("cmdType", ""):
                    # Mettre à jour les données de température des appareils existants
                    device_id = mqtt_data.get("deviceId")
                    if device_id and devices:
                        for device in devices:
                            if str(device.get("deviceId")) == str(device_id):
                                # Mettre à jour les données de température
                                device["lastStatusCmd"] = mqtt_data
                                break
            
            return {
                "devices": devices,
                "user_info": user_info,
            }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

