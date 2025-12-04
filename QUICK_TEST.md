# Quick Test Commands

## Browser Testing
Just paste these URLs in your browser:

```
http://localhost:5000/
http://localhost:5000/api/health
http://localhost:5000/api/qikink/status
http://localhost:5000/api/products
http://localhost:5000/api/products/BHRT-001-M
http://localhost:5000/api/docs
```

## PowerShell Testing

### Check Qikink Status
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/qikink/status" -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Get All Products
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/products" -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Get Single Product
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/products/BHRT-001-M" -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

### Health Check
```powershell
$response = Invoke-WebRequest -Uri "http://localhost:5000/api/health" -UseBasicParsing
$response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

## Expected Responses

### Status Response (Sandbox Mode)
```json
{
  "status": "sandbox-mode",
  "mode": "sandbox-fallback",
  "authenticated": true,
  "using_mock_token": true,
  "qikink_api": "https://sandbox-api.qikink.com/api/v1",
  "client_id": "78670273...",
  "last_check": "2025-12-04T14:30:45.123456",
  "message": "Using mock token for sandbox testing"
}
```

### Products Response
```json
{
  "status": "success",
  "count": 3,
  "data": [
    {
      "sku": "BHRT-001-M",
      "name": "Heritage Print T-Shirt",
      "price": 1299,
      "stock": 15,
      ...
    }
  ]
}
```

## Troubleshooting

### Server won't start
- Check Python is installed: `python --version`
- Check requirements installed: `pip list | findstr Flask`
- Check port 5000 is free: `netstat -ano | findstr :5000`

### Encoding errors (fixed)
- Error message like: `UnicodeEncodeError: 'charmap' codec`
- **Solution:** Already fixed in backend/app.py
- Restart server: `python backend/app.py`

### Connection refused
- Error: `Unable to connect to the remote server`
- **Check:** Is server running? Look for "Running on http://127.0.0.1:5000"
- **Fix:** Start server in new terminal: `python backend/app.py`

### Qikink status shows "error"
- This is normal if Qikink sandbox is offline
- System automatically uses mock token
- Check `using_mock_token: true` in response
- All features still work locally

## Next Steps

1. ✓ Server is running
2. ✓ All endpoints respond
3. → Test from frontend (index.html)
4. → Create test orders
5. → Verify orders saved to orders.json
6. → Check cart functionality
7. → Test contact form submission

---

**Test Date:** December 4, 2025  
**Server:** http://localhost:5000  
**Status:** All systems operational
