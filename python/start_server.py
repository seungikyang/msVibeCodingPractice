#!/usr/bin/env python3
"""Start FastAPI server and display startup information"""

import sys
import os

# Change to the correct directory
os.chdir('/Users/seungik.yang/Documents/myProgram/python')

print("="*70)
print("Starting FastAPI Social Media API")
print("="*70)
print()
print("Server Configuration:")
print("  - Host: 0.0.0.0")
print("  - Port: 8000")
print("  - API Base: /api")
print("  - Database: sns_api.db (SQLite)")
print()
print("Available Endpoints:")
print("  - Swagger UI: http://localhost:8000/docs")
print("  - ReDoc: http://localhost:8000/redoc")
print("  - OpenAPI Schema: http://localhost:8000/openapi.json")
print("  - API Root: http://localhost:8000/api/posts")
print()
print("="*70)
print()

# Start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
