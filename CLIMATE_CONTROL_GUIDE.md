# 🎛️ ThermoMaven Climate Control Guide

This guide explains how to use the climate control features added in v1.4.0.

## 🌡️ Climate Entities

Each probe on your ThermoMaven device has its own climate entity that provides temperature control.

### Entity Format

```
climate.thermomaven_[device_name]_probe_[number]_control
```

**Examples:**
- `climate.thermomaven_my_grill_probe_1_control`
- `climate.thermomaven_kitchen_probe_2_control`

### Available Entities by Device Model

| Model | Name | Probes | Climate Entities |
|-------|------|--------|------------------|
| **WT02** | ThermoMaven P2 | 2 | probe_1_control, probe_2_control |
| **WT06** | ThermoMaven P4 | 4 | probe_1 through probe_4_control |
| **WT07** | ThermoMaven G2 | 2 | probe_1_control, probe_2_control |
| **WT09** | ThermoMaven G4 | 4 | probe_1 through probe_4_control |
| **WT10** | ThermoMaven G1 | 1 | probe_1_control |
| **WT11** | ThermoMaven P1 | 1 | probe_1_control |

## 🎯 Features

### Temperature Display

Each climate entity shows:
- **Current Temperature** - Real-time probe temperature
- **Target Temperature** - Your desired cooking temperature
- **Temperature Unit** - Fahrenheit (°F)

### HVAC Modes

| Mode | Icon | Description |
|------|------|-------------|
| **Off** | ⏹️ | Cooking stopped/paused |
| **Heat** | 🔥 | Actively cooking to target |
| **Auto** | 🔄 | Resting state |

### Preset Modes

| Preset | Icon | Description | HVAC Mode |
|--------|------|-------------|-----------|
| **Cooking** | 🍳 | Active cooking session | Heat |
| **Ready** | ✅ | Target temperature reached | Off |
| **Resting** | 😴 | Resting period | Auto |
| **Remove** | 🍽️ | Ready to serve | Off |

### Temperature Range

- **Minimum:** 32°F (0°C)
- **Maximum:** 572°F (300°C)
- **Step:** 1°F

## 📱 User Interface

### Lovelace Card Example

```yaml
type: thermostat
entity: climate.thermomaven_grill_probe_1_control
name: Steak Temperature
features:
  - type: climate-hvac-modes
    hvac_modes:
      - "off"
      - heat
  - type: climate-preset-modes
```

### Advanced Card with Multiple Probes

```yaml
type: vertical-stack
cards:
  - type: thermostat
    entity: climate.thermomaven_grill_probe_1_control
    name: Probe 1 - Steak
  - type: thermostat
    entity: climate.thermomaven_grill_probe_2_control
    name: Probe 2 - Chicken
  - type: entities
    entities:
      - entity: sensor.thermomaven_grill_area_1_tip
        name: Probe 1 Current Temp
      - entity: sensor.thermomaven_grill_area_2
        name: Probe 2 Current Temp
```

## 🔧 Services

### Set Target Temperature

Set the target cooking temperature:

```yaml
service: climate.set_temperature
target:
  entity_id: climate.thermomaven_grill_probe_1_control
data:
  temperature: 165
```

### Start Cooking

Start a cooking session:

```yaml
service: climate.turn_on
target:
  entity_id: climate.thermomaven_grill_probe_1_control
```

Or set mode to heat:

```yaml
service: climate.set_hvac_mode
target:
  entity_id: climate.thermomaven_grill_probe_1_control
data:
  hvac_mode: heat
```

### Stop Cooking

Stop/pause cooking:

```yaml
service: climate.turn_off
target:
  entity_id: climate.thermomaven_grill_probe_1_control
```

### Set Preset Mode

Change cooking state:

```yaml
service: climate.set_preset_mode
target:
  entity_id: climate.thermomaven_grill_probe_1_control
data:
  preset_mode: cooking
```

## 🤖 Automation Examples

### Notify When Target Reached

Get notified when your food reaches the target temperature:

```yaml
automation:
  - alias: "Cooking - Target Temperature Reached"
    trigger:
      - platform: template
        value_template: >
          {{ state_attr('climate.thermomaven_grill_probe_1_control', 'current_temperature') >= 
             state_attr('climate.thermomaven_grill_probe_1_control', 'target_temperature') }}
    condition:
      - condition: state
        entity_id: climate.thermomaven_grill_probe_1_control
        state: heat
    action:
      - service: notify.mobile_app
        data:
          title: "🍳 Cooking Complete!"
          message: "Probe 1 has reached {{ states('sensor.thermomaven_grill_probe_1') }}°F"
```

### Auto-Start Cooking at Specific Time

Start cooking at a scheduled time:

```yaml
automation:
  - alias: "Start Cooking Dinner"
    trigger:
      - platform: time
        at: "17:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.thermomaven_grill_probe_1_control
        data:
          temperature: 145
      - service: climate.turn_on
        target:
          entity_id: climate.thermomaven_grill_probe_1_control
```

### Temperature Alert

Alert if temperature exceeds safe limit:

```yaml
automation:
  - alias: "Temperature Too High Alert"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_probe_1
        above: 180
    condition:
      - condition: state
        entity_id: climate.thermomaven_grill_probe_1_control
        state: heat
    action:
      - service: climate.turn_off
        target:
          entity_id: climate.thermomaven_grill_probe_1_control
      - service: notify.mobile_app
        data:
          title: "⚠️ Temperature Alert!"
          message: "Probe 1 exceeded safe temperature. Cooking stopped."
```

### Multi-Probe Cooking

Cook different items to different temperatures:

```yaml
script:
  start_bbq:
    alias: "Start BBQ Session"
    sequence:
      # Probe 1 - Steak (Medium Rare)
      - service: climate.set_temperature
        target:
          entity_id: climate.thermomaven_grill_probe_1_control
        data:
          temperature: 135
      - service: climate.turn_on
        target:
          entity_id: climate.thermomaven_grill_probe_1_control
      
      # Probe 2 - Chicken (Well Done)
      - service: climate.set_temperature
        target:
          entity_id: climate.thermomaven_grill_probe_2_control
        data:
          temperature: 165
      - service: climate.turn_on
        target:
          entity_id: climate.thermomaven_grill_probe_2_control
```

## 🔍 Troubleshooting

### Climate Entity Not Appearing

1. **Restart Home Assistant** after updating to v1.4.0
2. **Check MQTT connection** - Climate control requires MQTT
3. **Verify device is online** - Device must be connected to WiFi
4. **Check logs** for errors:
   ```
   Settings → System → Logs
   Filter: "thermomaven"
   ```

### Temperature Not Updating

1. **Check MQTT status** in logs
2. **Verify device connection** to WiFi
3. **Check device battery** - Low battery may affect connectivity
4. **Manually refresh** the integration

### Commands Not Working

1. **Check MQTT publish topics**:
   - Commands are sent via MQTT
   - Device must be subscribed to its publish topic
   
2. **Verify device permissions**:
   - Make sure you're the device owner
   - Shared devices may have limited control
   
3. **Check device model**:
   - Some features may vary by model
   - Verify your model supports temperature control

### Debug Logging

Enable debug logging for detailed information:

```yaml
logger:
  default: info
  logs:
    custom_components.thermomaven: debug
```

## 📊 Technical Details

### MQTT Command Structure

Commands are sent to: `app/device/{deviceId}/pub`

**Message Format:**
```json
{
  "cmdType": "WT:probe:control",
  "cmdData": {
    "probeColor": "bright",
    "cookingAction": 1,
    "setParams": [
      {
        "setTemperature": 1650
      }
    ],
    "cookUuid": "...",
    "startClient": "android",
    "cookingState": "cooking"
  },
  "cmdId": "...",
  "deviceId": "...",
  "deviceType": "WT02",
  "userId": "...",
  "appVersion": "1804"
}
```

### Cooking Actions

| Action | Value | Description |
|--------|-------|-------------|
| Start | 1 | Start cooking session |
| Stop | 2 | Stop/pause cooking |
| Modify | 3 | Change settings only |

### Probe Colors

- **Probe 1, 3:** `bright`
- **Probe 2, 4:** `dark`

### Temperature Encoding

Temperatures are sent in **tenths of degrees Fahrenheit**:
- 165°F → `1650`
- 72.5°F → `725`
- 200°F → `2000`

## 💡 Tips & Best Practices

1. **Set realistic targets** - Different meats have different safe temperatures
2. **Use preset modes** - They reflect the actual cooking state
3. **Combine with sensors** - Use temperature sensors for more detailed monitoring
4. **Create scenes** - Save common cooking configurations
5. **Test first** - Try controls manually before automating

## 🍖 Temperature Reference

Common target temperatures:

| Food | Temperature | Doneness |
|------|-------------|----------|
| Beef Steak | 125°F | Rare |
| Beef Steak | 135°F | Medium Rare |
| Beef Steak | 145°F | Medium |
| Beef Steak | 155°F | Medium Well |
| Beef Steak | 165°F | Well Done |
| Chicken | 165°F | Safe Minimum |
| Pork | 145°F | Safe Minimum |
| Fish | 145°F | Safe Minimum |
| Ground Beef | 160°F | Safe Minimum |

## 🔗 Related Documentation

- [Installation Guide](HOMEASSISTANT_INSTALLATION.md)
- [Architecture](ARCHITECTURE.md)
- [Release Notes v1.4.0](RELEASE_NOTES_1.4.0.md)
- [API Documentation](api/)

---

**Happy Cooking!** 🍳🔥

