"""Constants for the ThermoMaven integration."""

DOMAIN = "thermomaven"

# Default values
DEFAULT_APP_KEY = "bcd4596f1bb8419a92669c8017bf25e8"
DEFAULT_APP_ID = "ap4060eff28137181bd"

# API endpoints
API_BASE_URL_COM = "https://api.iot.thermomaven.com"
API_BASE_URL_DE = "https://api-de.iot.thermomaven.com"

# Supported countries
COUNTRIES = {
    "AT": "Austria",
    "AU": "Australia",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CA": "Canada",
    "CH": "Switzerland",
    "CZ": "Czech Republic",
    "DE": "Germany",
    "DK": "Denmark",
    "ES": "Spain",
    "FI": "Finland",
    "FR": "France",
    "HU": "Hungary",
    "IE": "Ireland",
    "IS": "Iceland",
    "IT": "Italy",
    "LU": "Luxembourg",
    "NL": "Netherlands",
    "NO": "Norway",
    "NZ": "New Zealand",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "RS": "Serbia",
    "SE": "Sweden",
    "SK": "Slovakia",
    "TR": "Turkey",
    "UK": "United Kingdom",
    "US": "United States",
    "ZA": "South Africa",
}

# European countries (use DE API)
EUROPEAN_COUNTRIES = {
    "AT", "BE", "BG", "CH", "CZ", "DE", "DK", "ES", "FI", "FR",
    "HU", "IE", "IS", "IT", "LU", "NL", "NO", "PL", "PT", "RO",
    "RS", "SE", "SK", "TR", "UK"
}

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

# Configuration keys
CONF_REGION = "region"

