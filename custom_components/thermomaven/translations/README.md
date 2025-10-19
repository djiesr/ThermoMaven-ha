# 🌍 ThermoMaven Translation Files

This directory contains translation files for the ThermoMaven Home Assistant integration.

## 📁 Available Languages

| Language | Code | File | Status |
|----------|------|------|--------|
| 🇬🇧 English | `en` | `en.json` | ✅ Complete (Default) |
| 🇫🇷 French | `fr` | `fr.json` | ✅ Complete |
| 🇪🇸 Spanish | `es` | `es.json` | ✅ Complete |
| 🇵🇹 Portuguese | `pt` | `pt.json` | ✅ Complete |
| 🇩🇪 German | `de` | `de.json` | ✅ Complete |
| 🇨🇳 Chinese (Simplified) | `zh-Hans` | `zh-Hans.json` | ✅ Complete |

## 📊 Translation Coverage

All languages include translations for:

### Configuration Flow
- Setup title and description
- Email, password, and region fields
- Error messages (connection, authentication)
- Already configured warning

### Sensor Entities (17 sensors)
- Temperature sensors (Probes 1-4)
- Area temperature sensors (5 zones: tip to handle)
- Battery sensors (device + probes)
- Ambient and target temperature
- Cooking time sensors (total, current, remaining)
- Cooking mode and state
- WiFi signal strength

### Cooking States
- Cooking / Cuisson / Cocinando / Cozinhando / Garen / 烹饪中
- Charged / Chargé / Cargado / Carregado / Geladen / 已充电
- Charging / En Charge / Cargando / Carregando / Laden / 充电中
- Idle / Inactif / Inactivo / Inativo / Inaktiv / 空闲
- Standby / En Attente / En Espera / Em Espera / Bereitschaft / 待机

## 🔧 File Structure

Each translation file follows this structure:

```json
{
  "config": {
    "step": { ... },
    "error": { ... },
    "abort": { ... }
  },
  "entity": {
    "sensor": {
      "sensor_key": {
        "name": "Translated Name",
        "state": {
          "state_key": "Translated State"
        }
      }
    }
  }
}
```

## 🛠️ Adding a New Language

1. Create a new file: `XX.json` (where XX is the language code)
2. Copy the structure from `en.json`
3. Translate all values (keep keys unchanged)
4. Validate JSON syntax
5. Test in Home Assistant

## 📝 Notes

- Translation keys must match exactly between all files
- Only translate the `values`, never the `keys`
- Special characters (é, ñ, ü, etc.) are supported in UTF-8
- Chinese uses simplified characters (zh-Hans)
- File must be valid JSON (use a validator)

## 🔄 How Translations Work

1. Home Assistant detects your system language
2. Loads the corresponding `XX.json` file
3. Applies translations to entity names and states
4. Falls back to English if translation is missing

## 🌐 Language Codes Reference

- `en` - English
- `fr` - French (Français)
- `es` - Spanish (Español)
- `pt` - Portuguese (Português)
- `de` - German (Deutsch)
- `zh-Hans` - Chinese Simplified (简体中文)
- `zh-Hant` - Chinese Traditional (繁體中文)
- `it` - Italian (Italiano)
- `nl` - Dutch (Nederlands)
- `ru` - Russian (Русский)
- `ja` - Japanese (日本語)
- `ko` - Korean (한국어)

## 📖 More Information

For detailed translation documentation, see:
- [TRANSLATIONS.md](../TRANSLATIONS.md) in the root directory
- [Home Assistant Translation Documentation](https://developers.home-assistant.io/docs/internationalization/)

