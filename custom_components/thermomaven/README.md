# ThermoMaven Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Custom component for integrating ThermoMaven wireless thermometers with Home Assistant.

## Features

✅ **Real-time temperature monitoring** via MQTT  
✅ **Multiple probe support** (P1, P2, P4, G1, G2, G4)  
✅ **Battery level monitoring**  
✅ **Automatic device discovery**  
✅ **Cloud push updates** (no polling required)  

## Supported Devices

- **WT02** - ThermoMaven P2 (2 probes)
- **WT06** - ThermoMaven P4 (4 probes)
- **WT07** - ThermoMaven G2 (2 probes)
- **WT09** - ThermoMaven G4 (4 probes)
- **WT10** - ThermoMaven G1 (1 probe)
- **WT11** - ThermoMaven P1 (1 probe)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the 3 dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/yourusername/thermomaven-homeassistant`
6. Category: Integration
7. Click "Add"
8. Search for "ThermoMaven" and install

### Manual Installation

1. Copy the `custom_components/thermomaven` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Configuration** → **Integrations**
2. Click **+ Add Integration**
3. Search for **ThermoMaven**
4. Enter your ThermoMaven account credentials:
   - Email
   - Password

The integration will:
- Connect to the ThermoMaven API
- Retrieve your MQTT certificate
- Subscribe to device updates
- Create sensor entities for all your devices

## Entities

For each ThermoMaven device, the following entities are created:

### Temperature Sensors
- `sensor.thermomaven_DEVICE_probe_1` - Temperature from probe 1
- `sensor.thermomaven_DEVICE_probe_2` - Temperature from probe 2 (if available)
- `sensor.thermomaven_DEVICE_probe_3` - Temperature from probe 3 (if available)
- `sensor.thermomaven_DEVICE_probe_4` - Temperature from probe 4 (if available)

### Battery Sensor
- `sensor.thermomaven_DEVICE_battery` - Battery level (%)

## Usage Examples

### Automation: Alert when temperature reaches target

```yaml
automation:
  - alias: "Notify when steak is ready"
    trigger:
      - platform: numeric_state
        entity_id: sensor.thermomaven_grill_probe_1
        above: 55
    action:
      - service: notify.mobile_app
        data:
          title: "Steak is ready!"
          message: "Temperature reached {{ states('sensor.thermomaven_grill_probe_1') }}°C"
```

### Lovelace Card

```yaml
type: entities
title: BBQ Monitor
entities:
  - entity: sensor.thermomaven_grill_probe_1
    name: Steak Temperature
  - entity: sensor.thermomaven_grill_probe_2
    name: Chicken Temperature
  - entity: sensor.thermomaven_grill_battery
    name: Battery Level
```

### Graph Card

```yaml
type: history-graph
title: Temperature History
entities:
  - entity: sensor.thermomaven_grill_probe_1
  - entity: sensor.thermomaven_grill_probe_2
hours_to_show: 2
refresh_interval: 0
```

## Architecture

This integration uses:
- **REST API** for authentication and device management
- **AWS IoT Core MQTT** for real-time temperature updates
- **Client certificates** for secure MQTT authentication

## Troubleshooting

### Integration not loading

1. Check Home Assistant logs: **Settings** → **System** → **Logs**
2. Look for errors related to `thermomaven`
3. Make sure you have the required dependencies installed

### No devices showing up

1. Make sure your ThermoMaven devices are paired with your account in the mobile app
2. Check that devices are powered on and connected
3. Restart the integration: **Settings** → **Integrations** → **ThermoMaven** → **⋮** → **Reload**

### MQTT not connecting

1. Check your internet connection
2. Verify your ThermoMaven account credentials
3. Check logs for certificate-related errors

## Development

### Testing locally

1. Clone this repository
2. Copy `custom_components/thermomaven` to your Home Assistant's `config/custom_components/`
3. Restart Home Assistant
4. Check logs for any errors

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Credits

- Developed by reverse-engineering the ThermoMaven mobile app
- MQTT implementation based on AWS IoT Core SDK
- Thanks to the Home Assistant community

## License

MIT License

## Support

For issues and feature requests, please use the [GitHub Issues](https://github.com/yourusername/thermomaven-homeassistant/issues) page.

## Disclaimer

This is an unofficial integration and is not affiliated with or endorsed by ThermoMaven.

