# ThermoMaven API Client

An unofficial Python client for interacting with the ThermoMaven IoT API.

✅ **Status: Working!** - Authentication is functional. Device management and other features are in development.

## Description

This project provides a Python client to communicate with the ThermoMaven API, allowing control and monitoring of ThermoMaven connected kitchen devices.

## Features

- ✅ Secure authentication with ThermoMaven API
- ✅ Automatic MD5 signature generation
- ✅ Multi-region support (US, EU)
- ✅ Environment-based configuration
- 🚧 Device management (coming soon)
- 🚧 MQTT integration (coming soon)
- 🚧 Historical data retrieval (coming soon)

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
THERMOMAVEN_APP_KEY=bcd4596f1bb8419a92669c8017bf25e8
THERMOMAVEN_APP_ID=ap4060eff28137181bd
```

**Note**: The `app_key` and `app_id` shown above are the actual values needed for the US region.

## Usage

### Basic Login

```python
from thermomaven_client import ThermoMavenClient
import os

# Initialize the client
client = ThermoMavenClient(
    email=os.getenv('THERMOMAVEN_EMAIL'),
    password=os.getenv('THERMOMAVEN_PASSWORD')
)

# Set the credentials
client.app_key = os.getenv('THERMOMAVEN_APP_KEY')
client.app_id = os.getenv('THERMOMAVEN_APP_ID')

# Login
result = client.login()

if result and result.get("code") == "0":
    print(f"✓ Login successful!")
    print(f"Token: {client.token}")
    print(f"User ID: {client.user_id}")
else:
    print("✗ Login failed")
```

### Quick Test

```bash
# Copy the example configuration
cp env.example .env

# Edit .env with your email and password
nano .env

# Run the client
python thermomaven_client.py
```

Expected output:
```
Starting ThermoMaven Client...
=== LOGIN ===
Status: 200
✓ Login successful!
Token: [your-token]
User ID: [your-user-id]
🎉 SUCCESS! Logged in!
```

## Authentication Details

### Signature Algorithm

The API uses MD5 signature for request validation:

```
MD5(app_key|params_str|body_str)
```

Where:
- `app_key` = `bcd4596f1bb8419a92669c8017bf25e8`
- `params_str` = Sorted headers like `x-appId=...;x-appVersion=...;x-deviceSn=...`
- `body_str` = JSON body (if any)

### Required Headers

- `x-appId`: App identifier (`ap4060eff28137181bd` for US region)
- `x-appVersion`: App version (`1804`)
- `x-deviceSn`: Random device serial number (16 hex chars)
- `x-lang`: Language (`en_US`)
- `x-nonce`: UUID without dashes (lowercase)
- `x-region`: Region code (`US` or `DE`)
- `x-timestamp`: Current timestamp in milliseconds
- `x-token`: Auth token (or `"none"` before login)
- `x-sign`: MD5 signature

### Password Handling

Password must be MD5 hashed before sending to the API.

## API Documentation

The `whatweknow/` folder contains extracted API information:

- `part1.txt`: API configuration (MQTT endpoints, regions, versions)
- `part2.txt`: Available endpoints list

### Main Endpoints

- `/app/account/login` - Authentication ✅ Working
- `/app/device/*` - Device management 🚧 To implement
- `/app/user/*` - User management 🚧 To implement
- `/app/history/*` - Historical data 🚧 To implement
- `/app/recipe/*` - Recipes 🚧 To implement
- `/app/mqtt/cert/apply` - MQTT certificates 🚧 To implement

### Supported Regions

The service uses two data centers:
- **US**: `https://api.iot.thermomaven.com` (USA, Canada, Australia, etc.)
  - App ID: `ap4060eff28137181bd`
  - App Key: `bcd4596f1bb8419a92669c8017bf25e8`
- **DE**: `https://api.iot.thermomaven.de` (Europe, UK, etc.)
  - App ID & Key: To be determined

## Project Structure

```
ThermoMaven-ha/
├── thermomaven_client.py    # Main API client ✅
├── whatweknow/              # API documentation
│   ├── part1.txt           # Configuration and regions
│   └── part2.txt           # Available endpoints
├── requirements.txt         # Python dependencies
├── env.example             # Configuration template
├── .gitignore              # Files to ignore
├── LICENSE                 # MIT License
├── QUICKSTART.md           # Quick start guide
├── FINDING_APPKEY.md       # How the key was found
└── README.md               # This file
```

## Security

⚠️ **Important**: 
- Never commit your email/password to the code
- Always use environment variables or a `.env` file
- The `.env` file must be in `.gitignore`
- The `app_key` and `app_id` are safe to share (they're client secrets, not user secrets)

## Known Information

From reverse engineering the Android APK:
- Project ID: `thermomavencom`
- App Version: `1804`
- App ID (US): `ap4060eff28137181bd`
- App Key (US): `bcd4596f1bb8419a92669c8017bf25e8`
- Google API Key: `AIzaSyDt1OT_Vmmy8Am61ViPRdiGNMeOjw8lsmE`
- Facebook App ID: `625697601818899`

## Disclaimer

This project is unofficial and not affiliated with ThermoMaven. Use at your own risk. Using this client may violate ThermoMaven's Terms of Service.

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or pull request.

## TODO

- [x] ~~Find the valid `app_key`~~ ✅ Done!
- [x] ~~Implement login~~ ✅ Done!
- [ ] Implement device listing
- [ ] Implement device control methods
- [ ] Add MQTT support
- [ ] Add historical data retrieval
- [ ] Add recipe browsing/management
- [ ] Create Home Assistant integration
- [ ] Create unit tests
- [ ] Add data models documentation

## Troubleshooting

### "Sign error" (Code 40000)

Make sure:
- `app_key` and `app_id` are correct
- Headers are properly sorted
- Body JSON has no spaces: `{"key":"value"}` not `{"key": "value"}`
- Using `data=` not `json=` when sending the request

### "Region mismatch"

Change the `base_url` in the client:
- US: `https://api.iot.thermomaven.com`
- EU: `https://api.iot.thermomaven.de`

## Support

Found a bug? Have a question? Open an issue at: https://github.com/djiesr/ThermoMaven-ha/issues
