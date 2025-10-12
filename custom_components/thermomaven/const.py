"""Constants for the ThermoMaven integration."""

DOMAIN = "thermomaven"

# Default values
DEFAULT_APP_KEY = "bcd4596f1bb8419a92669c8017bf25e8"
DEFAULT_APP_ID = "ap4060eff28137181bd"

# API endpoints
API_BASE_URL = "https://api.iot.thermomaven.com"

# MQTT brokers
MQTT_BROKERS = {
    "US": "a2ubmaqm3a642j-ats.iot.us-west-2.amazonaws.com",
    "EU": "a2ubmaqm3a642j-ats.iot.eu-central-1.amazonaws.com",
}
MQTT_PORT = 8883

# Device models
DEVICE_MODELS = {
    "WT02": "ThermoMaven P2",
    "WT06": "ThermoMaven P4", 
    "WT07": "ThermoMaven G2",
    "WT09": "ThermoMaven G4",
    "WT10": "ThermoMaven G1",
    "WT11": "ThermoMaven P1",
}

