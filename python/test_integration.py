#!/usr/bin/env python3
"""Quick test to start app and verify OpenAPI endpoint"""

import uvicorn
import requests
import yaml
import json
import time
import threading
from pathlib import Path

def run_server():
    """Run the FastAPI server in a thread"""
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="error")

def test_openapi():
    """Test the OpenAPI endpoint"""
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test 1: Check if API is accessible
        print("\n1. Testing API accessibility...")
        response = requests.get("http://localhost:8000/api/posts", timeout=5)
        print(f"   ✓ API is accessible (Status: {response.status_code})")
        
        # Test 2: Fetch OpenAPI schema
        print("\n2. Fetching OpenAPI schema from /openapi.json...")
        response = requests.get("http://localhost:8000/openapi.json", timeout=5)
        api_schema = response.json()
        print(f"   ✓ OpenAPI schema fetched (Status: {response.status_code})")
        
        # Test 3: Load original yaml
        print("\n3. Loading original openapi.yaml...")
        with open("../openapi.yaml", 'r', encoding='utf-8') as f:
            yaml_schema = yaml.safe_load(f)
        print("   ✓ Original openapi.yaml loaded")
        
        # Test 4: Compare
        print("\n4. Comparing schemas...")
        
        # Check critical fields
        checks = {
            "openapi": api_schema.get('openapi') == yaml_schema.get('openapi'),
            "info.title": api_schema.get('info', {}).get('title') == yaml_schema.get('info', {}).get('title'),
            "info.version": api_schema.get('info', {}).get('version') == yaml_schema.get('info', {}).get('version'),
            "servers": api_schema.get('servers') == yaml_schema.get('servers'),
            "tags": api_schema.get('tags') == yaml_schema.get('tags'),
            "paths": api_schema.get('paths') == yaml_schema.get('paths'),
            "components": api_schema.get('components') == yaml_schema.get('components'),
        }
        
        all_passed = True
        for field, passed in checks.items():
            status = "✓" if passed else "✗"
            print(f"   {status} {field}: {'MATCH' if passed else 'DIFFERENT'}")
            if not passed:
                all_passed = False
                if field == "servers":
                    print(f"      API: {api_schema.get('servers')}")
                    print(f"      YAML: {yaml_schema.get('servers')}")
        
        if all_passed:
            print("\n✅ SUCCESS: OpenAPI endpoint renders exactly the same content as openapi.yaml!")
        else:
            print("\n❌ FAILURE: Schemas are different!")
            
        return all_passed
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_openapi()
    # Give some time before exiting
    time.sleep(2)
    exit(0 if result else 1)
