"""Sensor platform for ThermoMaven."""
import asyncio
import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfTemperature,
    UnitOfTime,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)
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
    
    # Attendre que le coordinator ait des données
    if not coordinator.data or not coordinator.data.get("devices"):
        _LOGGER.debug("⏳ Waiting for coordinator data...")
        await asyncio.sleep(2)
        
        if not coordinator.data or not coordinator.data.get("devices"):
            _LOGGER.error("❌ No devices after waiting")
            return
    
    _LOGGER.debug("✅ Coordinator has %d device(s), proceeding with sensor setup", 
                 len(coordinator.data.get("devices", [])))
    
    entities_to_add = []
    
    async def add_devices():
        """Add devices."""
        nonlocal entities_to_add
        
        devices = coordinator.data.get("devices", [])
        _LOGGER.debug("🔍 Adding sensors for %d device(s)", len(devices))
        
        if not devices:
            return
        
        for device in devices:
            device_id = str(device.get("deviceId"))
            
            if not device_id or device_id == "None":
                _LOGGER.warning("Skipping device with invalid deviceId: %s", device.get("deviceName"))
                continue
            
            device_model = device.get("deviceModel", "Unknown")
            num_probes = _get_num_probes(device_model)
            
            _LOGGER.debug("➕ Adding sensors for device: %s (%s)", device.get("deviceName"), device_id)
            
            # Add all sensors for this device
            for probe_num in range(1, num_probes + 1):
                entities_to_add.append(
                    ThermoMavenTemperatureSensor(
                        coordinator, device, probe_num, entry.entry_id
                    )
                )
            
            entities_to_add.append(
                ThermoMavenBatterySensor(coordinator, device, entry.entry_id)
            )
            
            for probe_num in range(1, num_probes + 1):
                entities_to_add.append(
                    ThermoMavenProbeBatterySensor(
                        coordinator, device, probe_num, entry.entry_id
                    )
                )
            
            for probe_num in range(1, num_probes + 1):
                for area_num in range(1, 6):
                    entities_to_add.append(
                        ThermoMavenAreaTemperatureSensor(
                            coordinator, device, probe_num, area_num, entry.entry_id
                        )
                    )

            for probe_num in range(1, num_probes + 1):
                entities_to_add.append(
                    ThermoMavenAmbientTemperatureSensor(
                        coordinator, device, probe_num, entry.entry_id
                    )
                )
            for probe_num in range(1, num_probes + 1):
                for sensor_class in (
                    ThermoMavenTargetTemperatureSensor,
                    ThermoMavenTotalCookTimeSensor,
                    ThermoMavenCurrentCookTimeSensor,
                    ThermoMavenRemainingCookTimeSensor,
                    ThermoMavenCookingModeSensor,
                    ThermoMavenCookingStateSensor,
                ):
                    entities_to_add.append(
                        sensor_class(coordinator, device, probe_num, entry.entry_id)
                    )
            entities_to_add.append(
                ThermoMavenWiFiRSSISensor(coordinator, device, entry.entry_id)
            )
    
    # Create entities
    await add_devices()
    
    if entities_to_add:
        _LOGGER.debug("➕ Adding %d new entities", len(entities_to_add))
        async_add_entities(entities_to_add, update_before_add=True)
        

    # Register callback for future device additions
    coordinator.async_add_listener(lambda: hass.async_create_task(add_devices()))
    
    _LOGGER.debug("✅ Sensor setup complete")


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


def _create_device_info(device: dict) -> DeviceInfo:
    """Create DeviceInfo with diagnostic information."""
    device_id = str(device.get("deviceId", "unknown"))
    device_name = device.get("deviceName", "ThermoMaven")
    device_model = device.get("deviceModel", "Unknown")
    device_sn = device.get("deviceSn", "Unknown")
    share_id = device.get("deviceShareId")
    from_user = device.get("fromUserName")
    
    # Serial number affiche le SN physique et l'ID MQTT pour diagnostic
    serial_display = f"{device_sn} | MQTT: {device_id}"
    
    # Configuration URL vers l'app ThermoMaven
    config_url = "https://www.thermomaven.com/app"
    
    # Via pour les appareils partagés
    via_device = None
    if share_id and from_user:
        via_device = (DOMAIN, f"shared_from_{from_user}")
    
    return DeviceInfo(
        identifiers={(DOMAIN, device_id)},
        name=device_name,
        manufacturer="ThermoMaven",
        model=DEVICE_MODELS.get(device_model, device_model),
        sw_version=device.get("firmwareVersion"),
        serial_number=serial_display,
        configuration_url=config_url,
        suggested_area="Kitchen",  # Zone suggérée
    )


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
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num}"
        self._attr_translation_key = f"probe_{probe_num}"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        _LOGGER.debug("Temperature sensor %s looking for device %s", self._attr_name, self._device_id)
        
        for device in devices:
            device_id = str(device.get("deviceId"))
            _LOGGER.debug("Checking device: %s (ID: %s)", device.get("deviceName"), device_id)
            
            if device_id == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                
                if not last_status:
                    _LOGGER.warning("❌ %s: No lastStatusCmd in device data!", self._attr_name)
                    return None
                
                cmd_data = last_status.get("cmdData", {})
                if cmd_data.get("globalStatus") != "online":
                    return None
                
                probes = cmd_data.get("probes", [])
                if self._probe_num <= len(probes):
                    probe_data = probes[self._probe_num - 1]
                    temp_raw = probe_data.get("curTemperature")
                    
                    if temp_raw is not None:
                        temp_f = temp_raw / 10.0
                        temp_c = (temp_f - 32) * 5/9
                        result = round(temp_c, 1)
                        _LOGGER.debug("✅ %s = %s°C", self._attr_name, result)
                        return result
        
        _LOGGER.warning("❌ %s: No data (deviceId: %s, devices: %d)", 
                       self._attr_name, self._device_id, len(devices))
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
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
        
        self._attr_has_entity_name = True
        self._attr_name = "Battery"
        self._attr_translation_key = "battery"
        self._attr_unique_id = f"{self._device_id}_battery"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

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
                    
                    # Get device info for diagnostics
                    mqtt_device_id = device.get("deviceId")
                    api_share_id = device.get("deviceShareId")
                    device_sn = device.get("deviceSn")
                    
                    return {
                        "status": status_translation.get(status, status),
                        "battery_status": cmd_data.get("batteryStatus", "unknown"),
                        "connection": cmd_data.get("connectStatus", "unknown"),
                        "wifi_rssi": cmd_data.get("wifiRssi"),
                        # Diagnostic info
                        "mqtt_device_id": mqtt_device_id,
                        "api_share_id": api_share_id,
                        "device_serial": device_sn,
                        "from_user": device.get("fromUserName"),
                        "share_status": device.get("shareStatus"),
                    }
        return {}


class ThermoMavenProbeBatterySensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven probe battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = "%"

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._probe_num = probe_num
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Battery"
        self._attr_translation_key = f"probe_{probe_num}_battery"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_battery"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes", [])
                    if self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        return probe_data.get("batteryValue")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenAreaTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven per-probe area temperature sensor (tip to handle)."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, device, probe_num, area_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._probe_num = probe_num
        self._area_num = area_num
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")

        area_labels = ["Area 1 Tip", "Area 2", "Area 3", "Area 4", "Area 5 Handle"]
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} {area_labels[area_num - 1]}"
        self._attr_translation_key = f"probe_{probe_num}_area_{area_num}"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_area_{area_num}"

        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None

                    probes = cmd_data.get("probes", [])
                    if self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        # areaTemperature is absent while the probe is docked/charging
                        area_temps = probe_data.get("areaTemperature") or []
                        if len(area_temps) >= self._area_num:
                            temp_raw = area_temps[self._area_num - 1]
                            if temp_raw is not None:
                                temp_f = temp_raw / 10.0
                                temp_c = (temp_f - 32) * 5/9
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
                return True
        return False


class ThermoMavenAmbientTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven per-probe ambient temperature sensor."""

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

        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Ambient Temperature"
        self._attr_translation_key = f"probe_{probe_num}_ambient_temp"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_ambient_temp"

        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None

                    probes = cmd_data.get("probes", [])
                    if self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        # curAmbientTemperature is absent while the probe is docked/charging
                        temp_raw = probe_data.get("curAmbientTemperature")
                        if temp_raw is not None:
                            temp_f = temp_raw / 10.0
                            temp_c = (temp_f - 32) * 5/9
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
                return True
        return False


class ThermoMavenTargetTemperatureSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven target temperature sensor."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Target Temperature"
        self._attr_translation_key = f"probe_{probe_num}_target_temp"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_target_temp"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        set_params = probe_data.get("setParams")
                        if isinstance(set_params, list) and set_params and isinstance(set_params[0], dict):
                            temp_raw = set_params[0].get("setTemperature")
                            if isinstance(temp_raw, (int, float)):
                                temp_f = temp_raw / 10.0
                                temp_c = (temp_f - 32) * 5/9
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
                return True
        return False


class ThermoMavenTotalCookTimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven total cook time sensor."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.TOTAL
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Total Cook Time"
        self._attr_translation_key = f"probe_{probe_num}_total_cook_time"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_total_cook_time"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        return probe_data.get("totalCookSec")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenCurrentCookTimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven current cook time sensor."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Current Cook Time"
        self._attr_translation_key = f"probe_{probe_num}_current_cook_time"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_current_cook_time"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        return probe_data.get("curCookSec")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenRemainingCookTimeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven remaining cook time sensor."""

    _attr_device_class = SensorDeviceClass.DURATION
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.SECONDS

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Remaining Cook Time"
        self._attr_translation_key = f"probe_{probe_num}_remaining_cook_time"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_remaining_cook_time"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        return probe_data.get("curRemainedSec")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenCookingModeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven cooking mode sensor."""

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Cooking Mode"
        self._attr_translation_key = f"probe_{probe_num}_cooking_mode"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_cooking_mode"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        return probe_data.get("cookingMode")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenCookingStateSensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven cooking state sensor."""

    def __init__(self, coordinator, device, probe_num, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._probe_num = probe_num
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = f"Probe {probe_num} Cooking State"
        self._attr_translation_key = f"probe_{probe_num}_cooking_state"
        self._attr_unique_id = f"{self._device_id}_probe_{probe_num}_cooking_state"
        self._attr_icon = "mdi:chef-hat"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    
                    probes = cmd_data.get("probes")
                    if isinstance(probes, list) and self._probe_num <= len(probes):
                        probe_data = probes[self._probe_num - 1]
                        if not isinstance(probe_data, dict):
                            return None
                        cooking_state = probe_data.get("cookingState")
                        # Return raw value, translation is handled by Home Assistant
                        return cooking_state
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False


class ThermoMavenWiFiRSSISensor(CoordinatorEntity, SensorEntity):
    """Representation of a ThermoMaven WiFi RSSI sensor."""

    _attr_device_class = SensorDeviceClass.SIGNAL_STRENGTH
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = SIGNAL_STRENGTH_DECIBELS_MILLIWATT

    def __init__(self, coordinator, device, entry_id):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._device_id = device.get("deviceId")
        self._device_name = device.get("deviceName", "ThermoMaven")
        self._device_model = device.get("deviceModel", "Unknown")
        
        self._attr_has_entity_name = True
        self._attr_name = "WiFi Signal"
        self._attr_translation_key = "wifi_rssi"
        self._attr_unique_id = f"{self._device_id}_wifi_rssi"
        
        # Use helper function to create device info with diagnostic data
        self._attr_device_info = _create_device_info(device)

    @property
    def native_value(self):
        """Return the state of the sensor."""
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                last_status = device.get("lastStatusCmd", {})
                if last_status:
                    cmd_data = last_status.get("cmdData", {})
                    if cmd_data.get("globalStatus") != "online":
                        return None
                    return cmd_data.get("wifiRssi")
        return None

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        if not self.coordinator.last_update_success:
            return False
        devices = self.coordinator.data.get("devices", [])
        for device in devices:
            if str(device.get("deviceId")) == str(self._device_id):
                return True
        return False

