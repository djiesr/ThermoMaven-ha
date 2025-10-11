# ThermoMaven API Client

An unofficial Python client for interacting with the ThermoMaven IoT API.

## ⚠️ CRITICAL: App Key Required

**This client is not yet functional.** The ThermoMaven API requires an `app_key` for authentication that has not been found. All API calls currently fail with "Sign error".

**See [FINDING_APPKEY.md](FINDING_APPKEY.md) for details on how to help find it.**

---

## Description

This project provides a Python client to communicate with the ThermoMaven API, allowing control and monitoring of ThermoMaven connected kitchen devices.

## Features

- Secure authentication with ThermoMaven API
- Automatic signature generation
- Multi-region support (US, EU, etc.)
- Configurable HTTP client

## Installation

1. Clone this repository:
```bash
git clone https://github.com/djiesr/ThermoMaven-ha.git
cd ThermoMaven-ha
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file at the project root with your credentials:

```env
THERMOMAVEN_EMAIL=your-email@example.com
THERMOMAVEN_PASSWORD=your-password
THERMOMAVEN_APP_KEY=your-app-key
```

## Usage

```python
from thermomaven_client import ThermoMavenClient
import os

# Initialize the client
client = ThermoMavenClient(
    email=os.getenv('THERMOMAVEN_EMAIL'),
    password=os.getenv('THERMOMAVEN_PASSWORD')
)

# Set the app key
client.app_key = os.getenv('THERMOMAVEN_APP_KEY', '')

# Login
result = client.login()

if result:
    print("Login successful!")
    # Your code here...
else:
    print("Login failed")
```

## Missing Components

### ⚠️ Critical: App Key Required

The authentication requires an `app_key` that has not yet been found. The API signature is calculated as:

```
MD5(app_key|params_str|body_str)
```

Without the correct `app_key`, the API returns:
- Status 200
- Code: `40000`
- Message: "Sign error"

**How to find it:**
- Decompile the ThermoMaven Android/iOS app
- Look in configuration files or hardcoded strings
- Possible locations: `strings.xml`, ProGuard obfuscated code, native libraries

### What Works
- ✅ API endpoint structure
- ✅ Request signature algorithm
- ✅ Header construction
- ✅ Region configuration

### What's Missing
- ❌ Valid `app_key` value
- ❌ Device management endpoints implementation
- ❌ MQTT integration
- ❌ Historical data retrieval
- ❌ Recipe management

## API Documentation

The `whatweknow/` folder contains extracted API information:

- `part1.txt`: API configuration (MQTT endpoints, regions, versions)
- `part2.txt`: Available endpoints list

### Main Endpoints

- `/app/account/login` - Authentication
- `/app/device/*` - Device management
- `/app/user/*` - User management
- `/app/history/*` - Historical data
- `/app/recipe/*` - Recipes
- `/app/mqtt/cert/apply` - MQTT certificates

### Supported Regions

The service uses two data centers:
- **US**: `https://api.iot.thermomaven.com` (USA, Canada, Australia, etc.)
- **DE**: `https://api.iot.thermomaven.de` (Europe, UK, etc.)

## Project Structure

```
ThermoMaven-ha/
├── thermomaven_client.py    # Main API client
├── whatweknow/              # API documentation
│   ├── part1.txt           # Configuration and regions
│   └── part2.txt           # Available endpoints
├── requirements.txt         # Python dependencies
├── env.example             # Configuration template
├── .gitignore              # Files to ignore
└── README.md               # This file
```

## Security

⚠️ **Important**: Never commit your credentials to the code. Always use environment variables or a `.env` file (which must be in `.gitignore`).

## Known Information

From decompiled APK:
- Project ID: `thermomavencom`
- App Version: `1804`
- Google API Key: `AIzaSyDt1OT_Vmmy8Am61ViPRdiGNMeOjw8lsmE`
- Facebook App ID: `625697601818899`

## Disclaimer

This project is unofficial and not affiliated with ThermoMaven. Use at your own risk. Using this client may violate ThermoMaven's Terms of Service.

## License

This project is provided "as is" for educational purposes only.

## Contributing

Contributions are welcome! Especially if you can find the `app_key` value. Feel free to open an issue or pull request.

## TODO

- [ ] Find the valid `app_key`
- [ ] Implement other endpoints (devices, history, etc.)
- [ ] Add MQTT support
- [ ] Create unit tests
- [ ] Add data models documentation
- [ ] Implement device control methods
- [ ] Add recipe browsing/management
- [ ] Create Home Assistant integration

## Help Wanted

**If you can help find the `app_key`**, please:
1. Check the decompiled APK in native libraries (`.so` files)
2. Look for network traffic captures
3. Search for obfuscated strings in the Java/Kotlin code
4. Check for any initialization code in the main Application class

The `app_key` is likely a string of 32-64 characters (possibly hex or base64).
