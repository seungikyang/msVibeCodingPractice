#!/usr/bin/env python3
"""Test script to verify FastAPI app and OpenAPI endpoint"""

import sys
import time
import json
import yaml
import subprocess
from pathlib import Path

def main():
    # Start the FastAPI app
    print("Starting FastAPI application...")
    process = subprocess.Popen(
        [sys.executable, "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait for server to start
    time.sleep(3)
    
    # Test API endpoint
    print("\n1. Testing API endpoint...")
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8000/api/posts"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("   ✓ API endpoint is accessible")
        print(f"   Response: {result.stdout[:100]}")
    else:
        print("   ✗ API endpoint failed")
        process.kill()
        return 1
    
    # Get OpenAPI schema from the endpoint
    print("\n2. Fetching OpenAPI schema from /openapi.json...")
    result = subprocess.run(
        ["curl", "-s", "http://localhost:8000/openapi.json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("   ✗ Failed to fetch OpenAPI schema")
        process.kill()
        return 1
    
    try:
        api_schema = json.loads(result.stdout)
        print("   ✓ OpenAPI schema fetched successfully")
    except json.JSONDecodeError as e:
        print(f"   ✗ Invalid JSON response: {e}")
        process.kill()
        return 1
    
    # Load original openapi.yaml
    print("\n3. Loading original openapi.yaml...")
    yaml_path = Path("../openapi.yaml")
    with open(yaml_path, 'r', encoding='utf-8') as f:
        yaml_schema = yaml.safe_load(f)
    print("   ✓ Original openapi.yaml loaded")
    
    # Compare schemas
    print("\n4. Comparing schemas...")
    differences = []
    
    # Compare basic structure
    for key in ['openapi', 'info', 'servers', 'tags', 'paths', 'components']:
        if key not in api_schema:
            differences.append(f"Missing key in API schema: {key}")
        elif api_schema[key] != yaml_schema[key]:
            differences.append(f"Difference in '{key}'")
    
    if differences:
        print("   ✗ Schemas are different:")
        for diff in differences:
            print(f"     - {diff}")
        
        # Show detailed comparison
        print("\n   API servers:", api_schema.get('servers'))
        print("   YAML servers:", yaml_schema.get('servers'))
    else:
        print("   ✓ Schemas match perfectly!")
    
    # Cleanup
    print("\n5. Stopping server...")
    process.kill()
    process.wait()
    print("   ✓ Server stopped")
    
    return 0 if not differences else 1

if __name__ == "__main__":
    sys.exit(main())
