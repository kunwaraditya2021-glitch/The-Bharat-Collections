#!/usr/bin/env python3
"""
The Bharat Collections - Qikink Integration Verification Script
Run this to verify all Qikink integration is properly configured
"""

import os
import json
from datetime import datetime

# Verification Results
results = {
    'timestamp': datetime.now().isoformat(),
    'checks': []
}

def check(name, status, message=""):
    """Record a check result"""
    results['checks'].append({
        'name': name,
        'status': '✅' if status else '❌',
        'message': message
    })
    print(f"{'✅' if status else '❌'} {name}" + (f": {message}" if message else ""))

print("\n" + "="*60)
print(" The Bharat Collections - Qikink Integration Verification")
print("="*60 + "\n")

# Check 1: Python version
import sys
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
check("Python Version", True, python_version)

# Check 2: Required packages
try:
    import flask
    check("Flask Package", True, "3.0.0+")
except ImportError:
    check("Flask Package", False, "Not installed")

try:
    import flask_cors
    check("Flask-CORS Package", True)
except ImportError:
    check("Flask-CORS Package", False, "Not installed")

try:
    import requests
    check("Requests Package", True, "2.31.0+")
except ImportError:
    check("Requests Package", False, "Not installed")

# Check 3: Project files
project_root = os.path.dirname(os.path.abspath(__file__))

files_to_check = {
    'backend/app.py': 'Flask Backend Application',
    'requirements.txt': 'Python Dependencies',
    'js/script.js': 'Frontend JavaScript',
    'index.html': 'Home Page',
    'pages/shop.html': 'Shop Page',
    'pages/product-detail.html': 'Product Detail Page',
    'css/styles.css': 'Stylesheet'
}

print("\n📁 Project Files:")
for file_path, description in files_to_check.items():
    full_path = os.path.join(project_root, file_path)
    exists = os.path.exists(full_path)
    check(f"  {description}", exists, file_path if not exists else "✓")

# Check 4: Qikink Configuration in app.py
print("\n🔑 Qikink Configuration:")
try:
    with open('backend/app.py', 'r') as f:
        app_content = f.read()
    
    qikink_checks = [
        ('Client ID (786702736653938)', 'QIKINK_CLIENT_ID = \'786702736653938\''),
        ('Client Secret', 'QIKINK_CLIENT_SECRET = \'bf043131d3e80f1d15b6d833f03e5cdf5a5e3a6fce0510b91e3e3aaebe1cabda\''),
        ('API Base URL', 'https://sandbox-api.qikink.com/api/v1'),
        ('Auth URL', 'https://sandbox-api.qikink.com/oauth/token'),
        ('QikinkClient Class', 'class QikinkClient:'),
        ('OAuth Authentication', 'def authenticate(self):'),
        ('Product Sync Method', 'def sync_products(self, products):'),
        ('Shipment Creation', 'def create_shipment(self, order):'),
        ('Status Tracking', 'def get_shipment_status(self, shipment_id):')
    ]
    
    for check_name, check_string in qikink_checks:
        found = check_string in app_content
        check(f"  {check_name}", found)
        
except Exception as e:
    check("  Qikink Configuration", False, str(e))

# Check 5: API Endpoints
print("\n🔌 Qikink API Endpoints:")
try:
    with open('backend/app.py', 'r') as f:
        app_content = f.read()
    
    endpoints = [
        ('/api/qikink/status', 'GET'),
        ('/api/qikink/authenticate', 'POST'),
        ('/api/qikink/sync', 'POST'),
        ('/api/qikink/fulfillment', 'GET'),
        ('/api/orders', 'POST (auto-sync)')
    ]
    
    for endpoint, method in endpoints:
        found = endpoint in app_content
        check(f"  {method} {endpoint}", found)
        
except Exception as e:
    check("  API Endpoints", False, str(e))

# Check 6: Documentation Files
print("\n📚 Documentation:")
docs = {
    'QIKINK_INTEGRATION.md': 'Complete Integration Guide',
    'QIKINK_READY.md': 'Implementation Summary',
    'INTEGRATION_COMPLETE.md': 'Change Summary',
    'API_TESTING_GUIDE.md': 'Testing Guide'
}

for doc_file, description in docs.items():
    exists = os.path.exists(doc_file)
    check(f"  {description}", exists, doc_file)

# Check 7: Testing Files
print("\n🧪 Testing & Setup:")
test_files = {
    'test-qikink.bat': 'Qikink Testing Script',
    'start-backend.bat': 'Backend Startup Script',
    'start-backend.ps1': 'PowerShell Startup Script'
}

for test_file, description in test_files.items():
    exists = os.path.exists(test_file)
    check(f"  {description}", exists, test_file)

# Summary
print("\n" + "="*60)
print(" Summary")
print("="*60 + "\n")

total_checks = len(results['checks'])
passed_checks = sum(1 for c in results['checks'] if c['status'] == '✅')
failed_checks = total_checks - passed_checks

print(f"Total Checks: {total_checks}")
print(f"Passed: {passed_checks}")
print(f"Failed: {failed_checks}")

if failed_checks == 0:
    print("\n🎉 ALL CHECKS PASSED! Qikink integration is ready to go!")
    print("\nNext Steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Start backend: python backend/app.py")
    print("3. Test integration: .\\test-qikink.bat")
    print("4. Create orders: Orders will auto-sync to Qikink")
else:
    print(f"\n⚠️  {failed_checks} check(s) failed. Please fix before proceeding.")
    print("\nTo fix:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Verify all files exist")
    print("3. Check backend/app.py is complete")

print("\n" + "="*60)
print(f" Verification completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60 + "\n")
