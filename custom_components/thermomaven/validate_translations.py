#!/usr/bin/env python3
"""Validate ThermoMaven translation files."""
import json
import os
from pathlib import Path

def validate_translations():
    """Validate all translation files."""
    translations_dir = Path("translations")
    
    if not translations_dir.exists():
        print("❌ translations directory not found")
        return False
    
    # Get all JSON files
    json_files = list(translations_dir.glob("*.json"))
    
    if "README.md" in [f.name for f in translations_dir.iterdir()]:
        print("Found README.md")
    
    print(f"\nFound {len(json_files)} translation files:")
    
    all_valid = True
    
    for json_file in sorted(json_files):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure
            has_config = 'config' in data
            has_entity = 'entity' in data
            has_sensor = has_entity and 'sensor' in data.get('entity', {})
            
            # Count sensors
            sensor_count = 0
            if has_sensor:
                sensor_count = len(data['entity']['sensor'])
            
            status = "OK" if has_config and has_entity else "WARN"
            lang_name = json_file.stem
            
            print(f"  {status} {lang_name:10} - {sensor_count:2} sensors - {json_file.stat().st_size:4} bytes")
            
            if not (has_config and has_entity):
                print(f"     WARN  Missing sections: config={has_config}, entity={has_entity}")
                all_valid = False
                
        except json.JSONDecodeError as e:
            print(f"  ERROR {json_file.name} - Invalid JSON: {e}")
            all_valid = False
        except Exception as e:
            print(f"  ERROR {json_file.name} - Error: {e}")
            all_valid = False
    
    print(f"\n{'All translations valid!' if all_valid else 'Some translations have issues'}")
    return all_valid

if __name__ == "__main__":
    validate_translations()

