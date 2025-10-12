# Quick Start Guide

Get up and running with ThermoMaven API Client in 5 minutes!

## Prerequisites

- Python 3.7 or higher
- ThermoMaven account (email and password)
- Internet connection

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/djiesr/ThermoMaven-ha.git
cd ThermoMaven-ha
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install requests python-dotenv
```

## Configuration

### 3. Create Environment File

Copy the example configuration:

```bash
cp env.example .env
```

### 4. Edit Your Credentials

Open `.env` in your favorite editor and add **only** your email and password:

```env
THERMOMAVEN_EMAIL=your-email@example.com
THERMOMAVEN_PASSWORD=your-password
THERMOMAVEN_APP_KEY=bcd4596f1bb8419a92669c8017bf25e8
THERMOMAVEN_APP_ID=ap4060eff28137181bd
```

**Note**: The `APP_KEY` and `APP_ID` are already correct for US region!

## Test It!

### 5. Run the Client

```bash
python thermomaven_client.py
```

### Expected Output

If everything works, you should see:

```
Starting ThermoMaven Client...
DEBUG body_str: {"accountName":"your-email@example.com","accountPassword":"...","deviceInfo":"google sdk_gphone_x86_64 11"}

=== SIGNATURE DEBUG ===
Sign string: bcd4596f1bb8419a92669c8017bf25e8|x-appId=...
MD5: ...
=== END DEBUG ===

=== LOGIN ===
AppId: ap4060eff28137181bd
AppKey: bcd4596f1bb8419a92669c8017bf25e8
DeviceSn: 3d053c363f7b23b5
x-token: none
Status: 200
Response: {
  "code": "0",
  "msg": "Your request has been successful.",
  "data": {
    "token": "...",
    "userId": ...,
    "user": {
      "userName": "...",
      "userEmail": "...",
      "passwordExists": true
    },
    ...
  }
}

✓ Login successful!
Token: ...
User ID: ...

🎉 SUCCESS! Logged in!
```

## Troubleshooting

### Error: "Missing environment variables"

Make sure your `.env` file exists and contains all required variables:
```env
THERMOMAVEN_EMAIL=your-email@example.com
THERMOMAVEN_PASSWORD=your-password
THERMOMAVEN_APP_KEY=bcd4596f1bb8419a92669c8017bf25e8
THERMOMAVEN_APP_ID=ap4060eff28137181bd
```

### Error: "Sign error" (Code 40000)

Check that:
- `app_key` and `app_id` match the values in `env.example`
- You're using the correct region (`US` vs `DE`)

### Error: "Invalid credentials" (Code 4xxxx)

- Verify your email and password are correct
- Make sure you can login to the official ThermoMaven app

### Wrong Region?

If you're in Europe, you might need to change the `base_url`:

In `thermomaven_client.py`, line 15:
```python
self.base_url = "https://api.iot.thermomaven.de"  # Change from .com to .de
```

And update your `.env`:
```env
# Note: EU keys might be different - to be determined
THERMOMAVEN_APP_KEY=bcd4596f1bb8419a92669c8017bf25e8
THERMOMAVEN_APP_ID=ap4060eff28137181bd
```

## What's Next?

Now that you can authenticate, you can:

1. **Explore the API** - Check out `whatweknow/part2.txt` for available endpoints
2. **List devices** - Implement `/app/device/list` endpoint
3. **Control devices** - Send commands to your ThermoMaven devices
4. **Get history** - Retrieve cooking history
5. **Contribute** - Help implement more features!

## Using in Your Code

```python
import os
from thermomaven_client import ThermoMavenClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize client
client = ThermoMavenClient(
    email=os.getenv('THERMOMAVEN_EMAIL'),
    password=os.getenv('THERMOMAVEN_PASSWORD')
)

# Set credentials
client.app_key = os.getenv('THERMOMAVEN_APP_KEY')
client.app_id = os.getenv('THERMOMAVEN_APP_ID')

# Login
result = client.login()

if result and result.get("code") == "0":
    print(f"Logged in! Token: {client.token}")
    
    # Now you can make authenticated API calls
    # TODO: Implement more endpoints!
else:
    print("Login failed")
```

## Security Reminder

- ✅ `.env` is in `.gitignore` - your credentials won't be committed
- ✅ `app_key` and `app_id` are safe to share (client secrets)
- ⚠️ Never commit your email/password to git
- ⚠️ Never share your authentication token publicly

## Need Help?

- 📖 Read the full [README.md](README.md)
- 🔍 Check [FINDING_APPKEY.md](FINDING_APPKEY.md) for technical details
- 🐛 Open an issue: https://github.com/djiesr/ThermoMaven-ha/issues

## Success? 🎉

If you successfully logged in, you're ready to start exploring the ThermoMaven API!

Consider contributing to the project by implementing additional endpoints or features.
