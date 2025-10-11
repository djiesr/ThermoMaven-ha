# Finding the App Key

## Current Status

The ThermoMaven API requires an `app_key` for request signature validation. Without it, all API calls fail with:

```json
{
  "code": "40000",
  "msg": "Sign error"
}
```

## What We Know

### Signature Algorithm
```
MD5(app_key|params_str|body_str)
```

Where:
- `app_key` = Unknown secret string
- `params_str` = Sorted headers like `x-appId=thermomavencom;x-appVersion=1804;...`
- `body_str` = JSON body (if any)

### Known Values
- Project ID: `thermomavencom`
- App Version: `1804`
- Google API Key: `AIzaSyDt1OT_Vmmy8Am61ViPRdiGNMeOjw8lsmE`
- Facebook App ID: `625697601818899`

## Where to Look

### 1. Native Libraries (Most Likely)

The `app_key` is probably stored in native code to make reverse engineering harder.

```bash
# Extract .so files from APK
unzip thermomaven.apk "lib/*"

# Search for strings in native libraries
strings lib/arm64-v8a/*.so | grep -E "^[a-f0-9]{32,64}$"
strings lib/armeabi-v7a/*.so | grep -E "^[a-zA-Z0-9+/=]{32,}$"

# Look for key-related strings
strings lib/*/*.so | grep -i "key\|secret\|sign"
```

### 2. Obfuscated Java/Kotlin Code

Check decompiled code for:

```bash
# Search in decompiled code
cd thermomaven_decompiled/
grep -r "app_key\|appKey\|APP_KEY" .
grep -r "sign\|signature" . | grep -i "key"

# Look for MD5 usage
grep -r "md5\|MD5\|MessageDigest" .

# Check for base64 encoded values
grep -r "^[a-zA-Z0-9+/=]{40,}$" .
```

### 3. Network Traffic

Capture real API calls from the official app:

```bash
# Using adb and tcpdump
adb shell tcpdump -i any -s0 -w - | wireshark -k -i -

# Or using mitmproxy
mitmproxy --mode transparent --showhost
```

Look for the `x-sign` header and try to reverse engineer the signature.

### 4. ProGuard Mapping

If available, check for:
- Signature generation classes
- Key management utilities
- Network interceptors

### 5. Resources and Assets

```bash
# Check XML files
find thermomaven_decompiled/res -name "*.xml" -exec grep -l "key\|secret" {} \;

# Check assets
find thermomaven_decompiled/assets -type f -exec file {} \;
```

## Reverse Engineering Steps

### Step 1: Find Signature Generation Code

Look for:
```java
// Example pattern
public String generateSign(String params, String body) {
    String signStr = APP_KEY + "|" + params + "|" + body;
    return MD5.hash(signStr);
}
```

### Step 2: Trace APP_KEY Initialization

Find where `APP_KEY` is:
- Loaded from native library
- Decrypted from resources
- Hardcoded in obfuscated form

### Step 3: Extract the Value

Use:
- **Frida** - Hook the signature generation function
- **Xposed** - Intercept and log the key
- **Static analysis** - Decompile and trace the value

## Frida Script Example

```javascript
// Hook the signature generation
Java.perform(function() {
    var SignUtil = Java.use("com.thermomaven.util.SignUtil");
    
    SignUtil.generateSign.implementation = function(params, body) {
        console.log("[*] generateSign called");
        console.log("[*] Params: " + params);
        console.log("[*] Body: " + body);
        
        var result = this.generateSign(params, body);
        console.log("[*] Signature: " + result);
        
        return result;
    };
});
```

## Testing a Potential Key

Once you find a potential `app_key`, test it:

```python
# In thermomaven_client.py
client = ThermoMavenClient(email, password)
client.app_key = "YOUR_POTENTIAL_KEY"
result = client.login()

# Success: {"code":"0", "data": {...}}
# Failed: {"code":"40000", "msg":"Sign error"}
```

## Known App Key Patterns

Common patterns for API keys:
- 32-64 character hex string: `[a-f0-9]{32,64}`
- Base64 encoded: `[a-zA-Z0-9+/=]{32,}`
- UUID format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

## Help Needed

If you find the `app_key`:
1. **Don't commit it directly** to the public repository
2. Open an issue or discussion
3. We can add it as an environment variable example

## Resources

- APK Decompiler: jadx, apktool
- Network Analysis: mitmproxy, Wireshark
- Dynamic Analysis: Frida, Xposed
- String Extraction: binwalk, strings

## Status Updates

- ❌ **Not found yet** - 2025-01-11
- 🔍 Investigation in progress

## Contributing

Found a lead? Open an issue at: https://github.com/djiesr/ThermoMaven-ha/issues

