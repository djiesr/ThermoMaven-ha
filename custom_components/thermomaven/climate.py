"""Climate platform for ThermoMaven."""
import asyncio
import logging
from typing import Any

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature, ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, DEVICE_MODELS

_LOGGER = logging.getLogger(__name__)

# Cooking states to HVAC modes
COOKING_STATE_TO_HVAC = {
    "cooking": HVACMode.HEAT,
    "ready": HVACMode.OFF,
    "resting": HVACMode.AUTO,
    "remove": HVACMode.OFF,
}

# Preset modes for cooking states
PRESET_COOKING = "cooking"
PRESET_READY = "ready"
PRESET_RESTING = "resting"
PRESET_REMOVE = "remove"

PRESET_MODES = [PRESET_COOKING, PRESET_READY, PRESET_RESTING, PRESET_REMOVE]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up ThermoMaven climate entities."""
    _LOGGER.info("🔧 Climate setup started")
    
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]
    
    _LOGGER.info("📊 Coordinator data available: %s, devices: %s", 
                 bool(coordinator.data), 
                 len(coordinator.data.get("devices", [])) if coordinator.data else 0)
    
    # Wait for coordinator data
    if not coordinator.data or not coordinator.data.get("devices"):
        _LOGGER.debug("⏳ Waiting for coordinator data...")
        await asyncio.sleep(2)
        
        if not coordinator.data or not coordinator.data.get("devices"):
            _LOGGER.error("❌ No devices after waiting")
            return
    
    _LOGGER.debug("✅ Coordinator has %d device(s), proceeding with climate setup", 
                 len(coordinator.data.get("devices", [])))
    
    entities_to_add = []
    devices = coordinator.data.get("devices", [])
    
    _LOGGER.info("📱 Processing %d device(s) for climate entities", len(devices))
    
    for device in devices:
        device_id = str(device.get("deviceId"))
        device_name = device.get("deviceName", "Unknown")
        device_model = device.get("deviceModel", "Unknown")
        
        _LOGGER.info("🔍 Checking device: %s (ID: %s, Model: %s)", 
                     device_name, device_id, device_model)
        
        if not device_id or device_id == "None":
            _LOGGER.warning("⚠️ Skipping device with invalid deviceId: %s", device_name)
            continue
        
        num_probes = _get_num_probes(device_model)
        
        _LOGGER.info("➕ Adding %d climate entities for device: %s (%s)", 
                     num_probes, device_name, device_id)
        
        # Add climate entity for each probe
        for probe_num in range(1, num_probes + 1):
            entities_to_add.append(
                ThermoMavenClimate(
                    coordinator, api, device, probe_num, entry.entry_id
                )
            )
    
    if entities_to_add:
        _LOGGER.info("🌡️ Adding %d climate entities to Home Assistant", len(entities_to_add))
        async_add_entities(entities_to_add, update_before_add=False)
    else:
        _LOGGER.warning("⚠️ No climate entities to add - check device data")
    
    _LOGGER.info("✅ Climate setup complete")


def _get_num_probes(device_model: str) -> int:
    """Get number of probes for a device model."""
    probe_counts = {
        "WT02": 2,  # P2
        "WT06": 4,  # P4
        "WT07": 2,  # G2
        "WT09": 4,  # G4
        "WT10": 1,  # G1
        "WT11": 1,  # P1
    }
    return probe_counts.get(device_model, 1)


class ThermoMavenClimate(CoordinatorEntity, ClimateEntity):
    """Representation of a ThermoMaven Climate entity."""

    _attr_has_entity_name = True
    _attr_temperature_unit = UnitOfTemperature.FAHRENHEIT
    _attr_hvac_modes = [HVACMode.OFF, HVACMode.HEAT, HVACMode.AUTO]
    _attr_supported_features = (
        ClimateEntityFeature.TARGET_TEMPERATURE |
        ClimateEntityFeature.PRESET_MODE |
        ClimateEntityFeature.TURN_ON |
        ClimateEntityFeature.TURN_OFF
    )
    _attr_preset_modes = PRESET_MODES
    _attr_min_temp = 32  # 0°C
    _attr_max_temp = 572  # 300°C
    _attr_target_temperature_step = 1

    def __init__(self, coordinator, api, device, probe_num, entry_id):
        """Initialize the climate entity."""
        super().__init__(coordinator)
        self._api = api
        self._device = device
        self._probe_num = probe_num
        self._entry_id = entry_id
        
        device_id = str(device.get("deviceId"))
        device_name = device.get("deviceName", "ThermoMaven")
        device_model = device.get("deviceModel", "Unknown")
        
        # Unique ID
        self._attr_unique_id = f"{device_id}_probe_{probe_num}_climate"
        
        # Entity name
        probe_name = f"Probe {probe_num}"
        self._attr_name = f"{probe_name} Control"
        
        # Device info
        model_name = DEVICE_MODELS.get(device_model, device_model)
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=device_name,
            manufacturer="ThermoMaven",
            model=model_name,
        )
        
        _LOGGER.debug("Created climate entity: %s (probe %d)", device_name, probe_num)

    @property
    def current_temperature(self) -> float | None:
        """Return the current temperature."""
        if not self.coordinator.data:
            return None
        
        devices = self.coordinator.data.get("devices", [])
        device_id = str(self._device.get("deviceId"))
        
        for device in devices:
            if str(device.get("deviceId")) == device_id:
                last_status = device.get("lastStatusCmd")
                if not last_status:
                    return None
                
                cmd_data = last_status.get("cmdData", {})
                probes = cmd_data.get("probes", [])
                
                if self._probe_num <= len(probes):
                    probe_data = probes[self._probe_num - 1]
                    cur_temp = probe_data.get("curTemperature")
                    if cur_temp is not None:
                        # Temperature is in tenths of degrees F
                        return cur_temp / 10.0
        
        return None

    @property
    def target_temperature(self) -> float | None:
        """Return the target temperature."""
        if not self.coordinator.data:
            return None
        
        devices = self.coordinator.data.get("devices", [])
        device_id = str(self._device.get("deviceId"))
        
        for device in devices:
            if str(device.get("deviceId")) == device_id:
                last_status = device.get("lastStatusCmd")
                if not last_status:
                    return None
                
                cmd_data = last_status.get("cmdData", {})
                probes = cmd_data.get("probes", [])
                
                if self._probe_num <= len(probes):
                    probe_data = probes[self._probe_num - 1]
                    set_params = probe_data.get("setParams", [])
                    
                    if set_params and len(set_params) > 0:
                        set_temp = set_params[0].get("setTemperature")
                        if set_temp is not None:
                            # Temperature is in tenths of degrees F
                            return set_temp / 10.0
        
        return None

    @property
    def hvac_mode(self) -> HVACMode:
        """Return current HVAC mode."""
        cooking_state = self._get_cooking_state()
        
        if cooking_state:
            return COOKING_STATE_TO_HVAC.get(cooking_state, HVACMode.OFF)
        
        return HVACMode.OFF

    @property
    def preset_mode(self) -> str | None:
        """Return current preset mode."""
        cooking_state = self._get_cooking_state()
        
        if cooking_state == "cooking":
            return PRESET_COOKING
        elif cooking_state == "ready":
            return PRESET_READY
        elif cooking_state == "resting":
            return PRESET_RESTING
        elif cooking_state == "remove":
            return PRESET_REMOVE
        
        return None

    def _get_cooking_state(self) -> str | None:
        """Get the cooking state for this probe."""
        if not self.coordinator.data:
            return None
        
        devices = self.coordinator.data.get("devices", [])
        device_id = str(self._device.get("deviceId"))
        
        for device in devices:
            if str(device.get("deviceId")) == device_id:
                last_status = device.get("lastStatusCmd")
                if not last_status:
                    return None
                
                cmd_data = last_status.get("cmdData", {})
                probes = cmd_data.get("probes", [])
                
                if self._probe_num <= len(probes):
                    probe_data = probes[self._probe_num - 1]
                    return probe_data.get("cookingState")
        
        return None

    async def async_set_temperature(self, **kwargs) -> None:
        """Set new target temperature."""
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        
        _LOGGER.debug("Setting target temperature to %.1f°F for probe %d", temperature, self._probe_num)
        
        # Get probe color (bright/dark)
        probe_color = self._get_probe_color()
        
        # Convert temperature to tenths
        temp_tenths = int(temperature * 10)
        
        # Send command via MQTT
        success = await self._api.async_set_probe_temperature(
            device_id=str(self._device.get("deviceId")),
            device_type=self._device.get("deviceModel", "WT02"),
            probe_color=probe_color,
            target_temperature=temp_tenths
        )
        
        if success:
            _LOGGER.debug("✅ Temperature set successfully")
            # Request coordinator refresh
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("❌ Failed to set temperature")

    async def async_set_hvac_mode(self, hvac_mode: HVACMode) -> None:
        """Set new HVAC mode."""
        _LOGGER.debug("Setting HVAC mode to %s for probe %d", hvac_mode, self._probe_num)
        
        probe_color = self._get_probe_color()
        
        # Map HVAC mode to cooking action
        if hvac_mode == HVACMode.HEAT:
            # Start cooking
            await self._api.async_start_cooking(
                device_id=str(self._device.get("deviceId")),
                device_type=self._device.get("deviceModel", "WT02"),
                probe_color=probe_color,
                target_temperature=int((self.target_temperature or 165) * 10)
            )
        elif hvac_mode == HVACMode.OFF:
            # Stop cooking
            await self._api.async_stop_cooking(
                device_id=str(self._device.get("deviceId")),
                device_type=self._device.get("deviceModel", "WT02"),
                probe_color=probe_color
            )
        
        await self.coordinator.async_request_refresh()

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        """Set new preset mode."""
        _LOGGER.debug("Setting preset mode to %s for probe %d", preset_mode, self._probe_num)
        
        # Map preset to HVAC mode
        if preset_mode == PRESET_COOKING:
            await self.async_set_hvac_mode(HVACMode.HEAT)
        elif preset_mode in [PRESET_READY, PRESET_REMOVE]:
            await self.async_set_hvac_mode(HVACMode.OFF)
        elif preset_mode == PRESET_RESTING:
            await self.async_set_hvac_mode(HVACMode.AUTO)

    async def async_turn_on(self) -> None:
        """Turn the entity on."""
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_turn_off(self) -> None:
        """Turn the entity off."""
        await self.async_set_hvac_mode(HVACMode.OFF)

    def _get_probe_color(self) -> str:
        """Get probe color (bright/dark) based on probe number."""
        # Odd numbered probes are "bright", even are "dark"
        return "bright" if self._probe_num % 2 == 1 else "dark"

