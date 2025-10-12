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
    
    entities = []
    
    # Add device sensors
    devices = coordinator.data.get("devices", [])
    for device in devices:
        device_id = device.get("deviceId")
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
    
    async_add_entities(entities)


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
                # Chercher dans les données de statut récentes
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
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
        if not self.coordinator.last_update_success:
            return False
        
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # Vérifier le statut en ligne depuis les données MQTT
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    return cmd_data.get("globalStatus") == "online"
                return True  # Si pas de données MQTT, considérer comme disponible
        return False


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
                # Chercher dans les données de statut récentes
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    return cmd_data.get("batteryValue")
                # Fallback sur les données statiques
                return device.get("batteryLevel")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                # Vérifier le statut en ligne depuis les données MQTT
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    return cmd_data.get("globalStatus") == "online"
                return True  # Si pas de données MQTT, considérer comme disponible
        return False

