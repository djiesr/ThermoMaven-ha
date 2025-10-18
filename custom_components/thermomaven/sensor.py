"""Sensor platform for ThermoMaven."""
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_MODELS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ThermoMaven sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    # Track which devices we've already added - use a more persistent approach
    if not hasattr(coordinator, '_added_devices'):
        coordinator._added_devices = set()
    
    async def add_devices():
        """Add new devices that haven't been added yet."""
        entities = []
        devices = coordinator.data.get("devices", [])
        
        _LOGGER.debug("Checking for new devices to add. Current devices: %d", len(devices))
        
        for device in devices:
            device_id = str(device.get("deviceId"))
            
            # Skip if already added
            if device_id in coordinator._added_devices:
                continue
                
            _LOGGER.info("Adding new device: %s (%s)", device.get("deviceName"), device_id)
            coordinator._added_devices.add(device_id)
            
            device_model = device.get("deviceModel", "Unknown")
            num_probes = _get_num_probes(device_model)
            
            # Add temperature sensors for each probe
            for probe_num in range(1, num_probes + 1):
                entities.append(
                    ThermoMavenTemperatureSensor(
                        coordinator, device, probe_num, entry.entry_id
                    )
                )
            
            # Add battery sensor
            entities.append(
                ThermoMavenBatterySensor(coordinator, device, entry.entry_id)
            )
        
        if entities:
            _LOGGER.info("Adding %d new entities", len(entities))
            async_add_entities(entities)
    
    # Add initial devices
    await add_devices()
    
    # Register callback to add new devices when coordinator updates
    coordinator.async_add_listener(lambda: hass.async_create_task(add_devices()))


def _get_num_probes(model: str) -> int:
    """Get number of probes for device model."""
    probe_counts = {
        "WT02": 2,  # P2
        "WT06": 4,  # P4
        "WT07": 2,  # G2
        "WT09": 4,  # G4
        "WT10": 1,  # G1
        "WT11": 1,  # P1
    }
    return probe_counts.get(model, 1)


class ThermoMavenTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._probe_num = probe_num
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_name = f"{self._device_name} Probe {probe_num}"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self._device_id))},
            name=self._device_name,
            manufacturer="ThermoMaven",
            model=DEVICE_MODELS.get(self._device_model, self._device_model),
            sw_version=device.get("firmwareVersion"),
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # Vérifier si l'appareil est en ligne
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    # Si l'appareil est hors ligne, retourner None pour que available gère l'affichage
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes", [])
                    if self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        # La température est en dixièmes de degré Fahrenheit (748 = 74.8°F)
                        temp_raw = probe_data.get("curTemperature")
                        if temp_raw is not None:
                            # Convertir de °F/10 vers °C
                            temp_f = temp_raw / 10.0  # 748 -> 74.8°F
                            temp_c = (temp_f - 32) * 5/9  # Conversion °F -> °C
                            return round(temp_c, 1)
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Toujours disponible si le coordinateur fonctionne et que l'appareil existe
        if not self.coordinator.last_update_success:
            return False
        
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # L'entité est toujours "disponible", même si l'appareil est offline
                # Cela permet d'afficher l'état "offline" au lieu de "indisponible"
                return True
        return False
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    status = cmd_data.get("globalStatus", "unknown")
                    
                    # Traduction du statut
                    status_translation = {
                        "online": "En ligne",
                        "offline": "Hors ligne",
                        "unknown": "Inconnu"
                    }
                    
                    attributes = {
                        "status": status_translation.get(status, status),
                        "connection": cmd_data.get("connectStatus", "unknown"),
                    }
                    
                    # Ajouter les infos de la sonde si disponible
                    probes = cmd_data.get("probes", [])
                    if self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        attributes["cooking_state"] = probe_data.get("cookingState", "idle")
                        attributes["probe_battery"] = probe_data.get("batteryValue")
                    
                    return attributes
        return {}


class ThermoMavenBatterySensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    def __init__(self, coordinator, device, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_name = f"{self._device_name} Battery"
        self._attr_unique_id = f"{self._device_id}_battery"
        
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, str(self._device_id))},
            name=self._device_name,
            manufacturer="ThermoMaven",
            model=DEVICE_MODELS.get(self._device_model, self._device_model),
            sw_version=device.get("firmwareVersion"),
        )

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # Vérifier si l'appareil est en ligne
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    # Si l'appareil est hors ligne, retourner None
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    return cmd_data.get("batteryValue")
                # Fallback sur les données statiques
                return device.get("batteryLevel")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        # Toujours disponible si le coordinateur fonctionne et que l'appareil existe
        if not self.coordinator.last_update_success:
            return False
        
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # L'entité est toujours "disponible", même si l'appareil est offline
                return True
        return False
    
    @property
    def extra_state_attributes(self):
        """Return additional state attributes."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    status = cmd_data.get("globalStatus", "unknown")
                    
                    # Traduction du statut
                    status_translation = {
                        "online": "En ligne",
                        "offline": "Hors ligne",
                        "unknown": "Inconnu"
                    }
                    
                    return {
                        "status": status_translation.get(status, status),
                        "battery_status": cmd_data.get("batteryStatus", "unknown"),
                        "connection": cmd_data.get("connectStatus", "unknown"),
                        "wifi_rssi": cmd_data.get("wifiRssi"),
                    }
        return {}

