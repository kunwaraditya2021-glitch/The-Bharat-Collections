@echo off
REM The Bharat Collections - Qikink Integration Test Script
REM This script tests all Qikink API endpoints

setlocal enabledelayedexpansion

cls
echo.
echo ========================================
echo  Qikink Integration Test Suite
echo ========================================
echo.
echo Make sure the backend is running first!
echo Start it with: start-backend.bat
echo.
pause

set API_URL=http://localhost:5000

echo.
echo ========================================
echo 1. Testing Qikink Connection Status
echo ========================================
echo.
curl -X GET %API_URL%/api/qikink/status
echo.
pause

echo.
echo ========================================
echo 2. Testing Qikink Authentication
echo ========================================
echo.
curl -X POST %API_URL%/api/qikink/authenticate
echo.
pause

echo.
echo ========================================
echo 3. Getting API Documentation
echo ========================================
echo.
curl -X GET %API_URL%/api/docs
echo.
pause

echo.
echo ========================================
echo 4. Fetching All Products
echo ========================================
echo.
curl -X GET %API_URL%/api/products
echo.
pause

echo.
echo ========================================
echo 5. Syncing Products with Qikink
echo ========================================
echo.
curl -X POST %API_URL%/api/qikink/sync
echo.
pause

echo.
echo ========================================
echo 6. Creating Test Order
echo ========================================
echo.
echo Creating order with BHRT-001-M (Heritage Print T-Shirt)...
echo.
curl -X POST %API_URL%/api/orders ^
  -H "Content-Type: application/json" ^
  -d "{\"customer_email\":\"test@bharat.com\",\"shipping_address\":\"Test Address, Delhi, India\",\"items\":[{\"sku\":\"BHRT-001-M\",\"quantity\":1,\"price\":1299}]}"
echo.
echo.
echo Copy the order_id from above response for testing fulfillment status...
pause

echo.
echo ========================================
echo 7. Checking Order Status
echo ========================================
echo.
set /p ORDER_ID="Enter the order_id (e.g., BHRT-1733304000): "
echo.
echo Checking fulfillment status for order: %ORDER_ID%
echo.
curl -X GET %API_URL%/api/qikink/fulfillment/%ORDER_ID%
echo.
pause

echo.
echo ========================================
echo All Tests Completed!
echo ========================================
echo.
echo Next Steps:
echo 1. Check orders.json for saved orders
echo 2. Monitor Qikink dashboard for synced products
echo 3. Track shipments using fulfillment endpoint
echo.
pause
