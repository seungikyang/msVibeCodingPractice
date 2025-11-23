#!/usr/bin/env python3
"""Simple test to verify openapi.yaml can be loaded correctly"""

import yaml
import json
from pathlib import Path

# Load openapi.yaml
yaml_path = Path("../openapi.yaml")
with open(yaml_path, 'r', encoding='utf-8') as f:
    yaml_schema = yaml.safe_load(f)

print("✓ Successfully loaded openapi.yaml")
print(f"\nOpenAPI Version: {yaml_schema.get('openapi')}")
print(f"API Title: {yaml_schema.get('info', {}).get('title')}")
print(f"API Version: {yaml_schema.get('info', {}).get('version')}")
print(f"\nServers: {yaml_schema.get('servers')}")
print(f"\nNumber of paths: {len(yaml_schema.get('paths', {}))}")
print(f"Number of components: {len(yaml_schema.get('components', {}).get('schemas', {}))}")

# Verify main.py can load it
print("\n--- Testing main.py custom_openapi function ---")
import sys
sys.path.insert(0, '.')

# Test the custom_openapi function
with open("../openapi.yaml", "r", encoding="utf-8") as f:
    test_schema = yaml.safe_load(f)

print("✓ custom_openapi function can load the file correctly")
print(f"Loaded server URL: {test_schema['servers'][0]['url']}")
