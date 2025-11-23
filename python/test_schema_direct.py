#!/usr/bin/env python3
"""Direct test of FastAPI app's OpenAPI schema without running server"""

import yaml
import json

# Import the FastAPI app
from main import app

print("Testing FastAPI app's OpenAPI schema generation...\n")

# Get the OpenAPI schema from the app
print("1. Getting OpenAPI schema from app.openapi()...")
api_schema = app.openapi()
print("   ✓ Schema generated successfully")

# Load original openapi.yaml
print("\n2. Loading original openapi.yaml...")
with open("../openapi.yaml", 'r', encoding='utf-8') as f:
    yaml_schema = yaml.safe_load(f)
print("   ✓ Original openapi.yaml loaded")

# Compare schemas
print("\n3. Comparing schemas...")

def compare_dicts(d1, d2, path=""):
    """Recursively compare two dictionaries"""
    differences = []
    
    # Check keys
    keys1 = set(d1.keys())
    keys2 = set(d2.keys())
    
    if keys1 != keys2:
        missing_in_d1 = keys2 - keys1
        missing_in_d2 = keys1 - keys2
        if missing_in_d1:
            differences.append(f"{path}: Missing keys in API schema: {missing_in_d1}")
        if missing_in_d2:
            differences.append(f"{path}: Extra keys in API schema: {missing_in_d2}")
    
    # Compare values for common keys
    for key in keys1 & keys2:
        new_path = f"{path}.{key}" if path else key
        v1 = d1[key]
        v2 = d2[key]
        
        if isinstance(v1, dict) and isinstance(v2, dict):
            differences.extend(compare_dicts(v1, v2, new_path))
        elif isinstance(v1, list) and isinstance(v2, list):
            if len(v1) != len(v2):
                differences.append(f"{new_path}: Different list lengths ({len(v1)} vs {len(v2)})")
            else:
                for i, (item1, item2) in enumerate(zip(v1, v2)):
                    if isinstance(item1, dict) and isinstance(item2, dict):
                        differences.extend(compare_dicts(item1, item2, f"{new_path}[{i}]"))
                    elif item1 != item2:
                        differences.append(f"{new_path}[{i}]: {item1} != {item2}")
        elif v1 != v2:
            differences.append(f"{new_path}: {v1} != {v2}")
    
    return differences

differences = compare_dicts(api_schema, yaml_schema)

if not differences:
    print("   ✅ PERFECT MATCH! OpenAPI schemas are identical!")
    print("\n4. Schema details:")
    print(f"   - OpenAPI Version: {api_schema.get('openapi')}")
    print(f"   - API Title: {api_schema.get('info', {}).get('title')}")
    print(f"   - Server URL: {api_schema.get('servers', [{}])[0].get('url')}")
    print(f"   - Number of endpoints: {len(api_schema.get('paths', {}))}")
    print(f"   - Number of schemas: {len(api_schema.get('components', {}).get('schemas', {}))}")
else:
    print(f"   ❌ Found {len(differences)} difference(s):")
    for i, diff in enumerate(differences[:10], 1):  # Show first 10
        print(f"   {i}. {diff}")
    if len(differences) > 10:
        print(f"   ... and {len(differences) - 10} more differences")

print("\n" + "="*70)
if not differences:
    print("✅ SUCCESS: FastAPI app renders exactly the same OpenAPI content!")
else:
    print("❌ FAILURE: Schemas have differences!")

exit(0 if not differences else 1)
