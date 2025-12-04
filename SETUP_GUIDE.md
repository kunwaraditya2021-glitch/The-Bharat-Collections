# 🚀 Backend Integration Setup Guide

## Overview
Your Bharat Collections website is now **fully integrated with a Python Flask backend**! The frontend communicates seamlessly with the backend for:
- ✓ Product catalog management
- ✓ Shopping cart synchronization
- ✓ Order processing
- ✓ Contact form submissions
- ✓ Qikink fulfillment tracking

---

## 🎯 Step-by-Step Setup

### Option 1: Using the Batch File (Easiest for Windows)

1. **Open File Explorer** and navigate to:
   ```
   C:\Users\adity\Desktop\THE BHARAT COLLECTIONS
   ```

2. **Double-click `start-backend.bat`**
   - This will automatically:
     - Check if Python is installed
     - Install required dependencies
     - Start the Flask server

3. **You should see:**
   ```
   ✓ Python found: Python 3.x.x
   ✓ Dependencies installed
   ========================================
   Starting Flask Backend Server...
   ========================================
   
   * Running on http://0.0.0.0:5000
   ```

4. **The server is now running!** Leave this window open.

---

### Option 2: Using PowerShell

1. **Open PowerShell** as Administrator
   - Right-click on PowerShell → Select "Run as Administrator"

2. **Navigate to the project folder:**
   ```powershell
   cd "C:\Users\adity\Desktop\THE BHARAT COLLECTIONS"
   ```

3. **Run the startup script:**
   ```powershell
   .\start-backend.ps1
   ```

4. **If you get an execution policy error:**
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Then run the script again.

---

### Option 3: Manual Setup (Full Control)

1. **Open PowerShell or Command Prompt**

2. **Navigate to project folder:**
   ```powershell
   cd "C:\Users\adity\Desktop\THE BHARAT COLLECTIONS"
   ```

3. **Install Flask and dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```powershell
   python backend/app.py
   ```

5. **You should see:**
   ```
   * Serving Flask app 'app'
   * Debug mode: on
   * Running on http://0.0.0.0:5000
   ```

---

## 🌐 Accessing the Website

### With Backend Running:

1. **Open the website:**
   ```
   file:///C:/Users/adity/Desktop/THE%20BHARAT%20COLLECTIONS/index.html
   ```

2. **The console will show:**
   ```
   ✓ Backend connected successfully
   ✓ Products loaded from backend: 3
   ```

3. **All features are now enabled:**
   - Browse products (loads from backend)
   - Add to cart (syncs to backend)
   - Submit contact form (saves to backend)
   - Track orders (Qikink integration)

### Without Backend (Frontend-Only Mode):

- Just open `index.html` directly
- Cart works locally in browser storage
- Contact form uses frontend validation only
- All features work but data isn't persisted

---

## ✅ Testing the Integration

### Check Backend Health

Open in browser:
```
http://localhost:5000/api/health
```

You should see:
```json
{
  "status": "healthy",
  "service": "The Bharat Collections API",
  "version": "1.0.0",
  "timestamp": "2025-12-04T..."
}
```

### View API Documentation

Open in browser:
```
http://localhost:5000/api/docs
```

This shows all available API endpoints.

### Test Products API

```
http://localhost:5000/api/products
```

Returns all products in JSON format.

### Get Single Product

```
http://localhost:5000/api/products/BHRT-001-M
```

Returns Heritage Print T-Shirt details.

---

## 📊 File System

After running the backend, you'll see new files created:

```
THE BHARAT COLLECTIONS/
├── orders.json              # Saved customer orders
├── contact_submissions.json # Saved contact form messages
├── backend/
│   └── app.py               # Flask server (already exists)
└── start-backend.bat        # Startup script
```

---

## 🔌 API Endpoints Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/products` | GET | Get all products |
| `/api/products?category=mens` | GET | Filter by category |
| `/api/products/<sku>` | GET | Get specific product |
| `/api/cart/add` | POST | Add to cart |
| `/api/orders` | POST | Create order |
| `/api/orders/<id>` | GET | Check order status |
| `/api/contact` | POST | Submit contact form |
| `/api/qikink/sync` | POST | Sync with Qikink |
| `/api/qikink/fulfillment/<id>` | GET | Get shipping status |
| `/api/health` | GET | Health check |
| `/api/docs` | GET | API documentation |

---

## 🛠️ Troubleshooting

### Python not found
**Problem:** `'python' is not recognized as an internal or external command`

**Solution:**
1. Install Python from https://www.python.org/
2. **Important:** Check "Add Python to PATH" during installation
3. Restart PowerShell/Command Prompt
4. Try again

### Port 5000 already in use
**Problem:** `Address already in use`

**Solution:**
1. Close any other Flask instances running
2. Or edit `backend/app.py` and change the port:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
   ```
3. Update `script.js`:
   ```javascript
   const API_BASE_URL = 'http://localhost:5001/api';  // Match new port
   ```

### CORS Error (frontend can't reach backend)
**Solution:** The Flask backend has CORS enabled already. If you still get errors:
1. Make sure backend is running on `http://localhost:5000`
2. Check that website is opened from file:// URL
3. Check browser console for exact error message

### Contact form not saving
**Solution:** Backend creates `contact_submissions.json` file in the project root. Make sure the folder has write permissions.

---

## 💾 Data Storage

The backend uses JSON files for storage:

**Orders** (`orders.json`):
```json
[
  {
    "order_id": "BHRT-1733304000",
    "customer_email": "user@example.com",
    "items": [...],
    "total": 3897,
    "status": "pending",
    "created_at": "2025-12-04T10:00:00"
  }
]
```

**Contact Messages** (`contact_submissions.json`):
```json
[
  {
    "id": 1733304000,
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Great products!",
    "submitted_at": "2025-12-04T10:00:00"
  }
]
```

---

## 🚀 Production Deployment

When ready for production (hosting on real server):

1. **Use a proper database** instead of JSON files
   - MongoDB
   - PostgreSQL
   - MySQL

2. **Add authentication**
   - User registration/login
   - JWT tokens
   - Password hashing

3. **Enable HTTPS** for security

4. **Set up payment gateway**
   - Razorpay
   - Stripe
   - PayU

5. **Deploy backend to cloud**
   - Heroku
   - AWS
   - Google Cloud
   - DigitalOcean

6. **Use environment variables**
   - `.env` file
   - `python-dotenv` package

---

## 📞 Quick Commands

**Start backend (PowerShell):**
```powershell
cd "C:\Users\adity\Desktop\THE BHARAT COLLECTIONS"; python backend/app.py
```

**Stop backend:**
```
Press Ctrl+C in the terminal
```

**Check Python version:**
```powershell
python --version
```

**List installed packages:**
```powershell
pip list
```

**Reinstall all dependencies:**
```powershell
pip install --upgrade -r requirements.txt
```

---

## ✨ Next Steps

1. ✓ Backend is ready to run
2. Add more products to `PRODUCTS` in `backend/app.py`
3. Connect a real database instead of JSON
4. Add payment gateway integration
5. Deploy to production server

---

**Happy selling! 🛍️**

Made with ❤️ for The Bharat Collections
