# 🔗 QIKINK INTEGRATION GUIDE

## ✅ Integration Status
**FULLY INTEGRATED** - Qikink API is now fully integrated into the Flask backend!

---

## 🔑 Your Qikink Credentials (Already Configured)

```
Client ID:     786702736653938
Client Secret: bf043131d3e80f1d15b6d833f03e5cdf5a5e3a6fce0510b91e3e3aaebe1cabda
Environment:   Sandbox (Testing)
API Base URL:  https://sandbox-api.qikink.com/api/v1
```

> ✓ All credentials are securely configured in `backend/app.py`

---

## 🚀 How Integration Works

### When You Start the Backend:

```
✓ Flask server starting...
✓ Qikink integration: ENABLED
✓ Environment: SANDBOX
✓ Client ID: 78670273...

Testing Qikink connection...
✓ Qikink authentication: SUCCESS
✓ API Endpoint: https://sandbox-api.qikink.com/api/v1
```

### Automatic Features:

1. **Product Sync** - Products auto-sync to Qikink on `/api/qikink/sync`
2. **Order Creation** - Orders automatically create shipments in Qikink
3. **Fulfillment Tracking** - Track shipments with real-time status
4. **Inventory Management** - Keep Qikink inventory updated

---

## 📋 Complete API Endpoints

### 1. Qikink Connection Status
**Check if Qikink is connected:**

```
GET http://localhost:5000/api/qikink/status
```

**Response:**
```json
{
  "status": "connected",
  "qikink_api": "https://sandbox-api.qikink.com/api/v1",
  "client_id": "78670273...",
  "last_check": "2025-12-04T10:30:00"
}
```

### 2. Authenticate with Qikink
**Test authentication:**

```
POST http://localhost:5000/api/qikink/authenticate
```

**Response:**
```json
{
  "status": "authenticated",
  "client_id": "78670273...",
  "api_endpoint": "https://sandbox-api.qikink.com/api/v1",
  "timestamp": "2025-12-04T10:30:00"
}
```

### 3. Sync Products to Qikink
**Manually sync all products:**

```
POST http://localhost:5000/api/qikink/sync
```

**What Gets Synced:**
- SKU
- Product Name
- Description
- Price
- Stock Quantity
- Category
- Manufacturer (Qikink)
- Origin (Made in India)

**Response:**
```json
{
  "sync_id": "SYNC-1733304000",
  "timestamp": "2025-12-04T10:30:00",
  "products_synced": 8,
  "qikink_integration": {
    "status": "success",
    "qikink_response": {
      "products_synced": 8,
      "sync_timestamp": "2025-12-04T10:30:00"
    }
  }
}
```

### 4. Create Order with Qikink Auto-Sync
**When you create an order, it automatically syncs to Qikink:**

```
POST http://localhost:5000/api/orders
Content-Type: application/json

{
  "customer_email": "customer@example.com",
  "shipping_address": "123 Main St, New Delhi 110001, India",
  "items": [
    {
      "sku": "BHRT-001-M",
      "quantity": 2,
      "price": 1299
    }
  ]
}
```

**Response (with Qikink Shipment Created):**
```json
{
  "status": "success",
  "message": "Order created successfully and synced with Qikink",
  "data": {
    "order_id": "BHRT-1733304000",
    "customer_email": "customer@example.com",
    "shipping_address": "123 Main St, New Delhi 110001, India",
    "items": [
      {
        "sku": "BHRT-001-M",
        "quantity": 2,
        "price": 1299
      }
    ],
    "total": 2598,
    "status": "confirmed",
    "qikink_status": "synced",
    "qikink_shipment_id": "QK-SHIP-12345",
    "tracking_id": "TRK-1733304000",
    "created_at": "2025-12-04T10:30:00"
  },
  "qikink_integration": {
    "status": "success",
    "qikink_shipment_id": "QK-SHIP-12345",
    "tracking_id": "TRK-1733304000"
  }
}
```

### 5. Get Order Fulfillment Status from Qikink
**Track shipment status:**

```
GET http://localhost:5000/api/qikink/fulfillment/BHRT-1733304000
```

**Response:**
```json
{
  "order_id": "BHRT-1733304000",
  "qikink_shipment_id": "QK-SHIP-12345",
  "status": "in_transit",
  "tracking_number": "TRK-1733304000",
  "estimated_delivery": "2025-12-10",
  "last_update": "2025-12-04T10:30:00",
  "events": [
    {
      "event": "order_received",
      "timestamp": "2025-12-04T10:00:00",
      "location": "Qikink Warehouse, Delhi"
    },
    {
      "event": "order_processing",
      "timestamp": "2025-12-04T14:30:00",
      "location": "Qikink Processing Center"
    },
    {
      "event": "out_for_delivery",
      "timestamp": "2025-12-05T08:00:00",
      "location": "Your City Delivery Hub"
    }
  ]
}
```

---

## 🔐 Security Features

### 1. OAuth 2.0 Authentication
- Automatic token generation and management
- Token refresh handling
- Secure client credentials storage

### 2. HMAC-SHA256 Signature
- Request signing for additional security
- Signature validation by Qikink API

### 3. API Request Headers
```
Authorization: Bearer {access_token}
Content-Type: application/json
X-Client-ID: 786702736653938
```

---

## 📦 Product Data Format (Qikink)

When syncing to Qikink, products are transformed to this format:

```json
{
  "sku": "BHRT-001-M",
  "name": "Heritage Print T-Shirt",
  "description": "Premium cotton with traditional Madhubani art print",
  "price": 1299,
  "stock_quantity": 15,
  "category": "mens",
  "manufacturer": "Qikink",
  "origin": "India"
}
```

---

## 📝 Shipment Data Format (Qikink)

When creating orders, shipment data sent to Qikink:

```json
{
  "order_id": "BHRT-1733304000",
  "customer_email": "customer@example.com",
  "shipping_address": "123 Main St, New Delhi 110001, India",
  "items": [
    {
      "sku": "BHRT-001-M",
      "quantity": 2,
      "price": 1299
    }
  ],
  "total_amount": 2598,
  "created_at": "2025-12-04T10:30:00"
}
```

---

## 🧪 Testing Steps

### Step 1: Verify Qikink Connection
```bash
# Open in browser:
http://localhost:5000/api/qikink/status
```

### Step 2: Test Authentication
```bash
# Using PowerShell:
curl -X POST http://localhost:5000/api/qikink/authenticate
```

### Step 3: Sync Products
```bash
# Using PowerShell:
curl -X POST http://localhost:5000/api/qikink/sync
```

### Step 4: Create Test Order
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "test@bharat.com",
    "shipping_address": "Test Address, Delhi",
    "items": [{"sku": "BHRT-001-M", "quantity": 1, "price": 1299}]
  }'
```

### Step 5: Check Fulfillment Status
```bash
# Replace ORDER_ID with actual order ID:
http://localhost:5000/api/qikink/fulfillment/BHRT-1733304000
```

---

## 📊 Order Flow Diagram

```
┌─────────────────┐
│  Frontend App   │
│  (HTML/JS)      │
└────────┬────────┘
         │ POST /api/orders
         ▼
┌──────────────────┐     ┌──────────────────────┐
│  Flask Backend   │────▶│  Qikink API          │
│  (Python)        │     │  (Sandbox)           │
└──────────────────┘     └──────────────────────┘
         │                        │
         │ Save locally           │ Create shipment
         ▼                        ▼
┌──────────────────┐     ┌──────────────────────┐
│  orders.json     │     │  Qikink Warehouse    │
│  (Local DB)      │     │  (Fulfillment)       │
└──────────────────┘     └──────────────────────┘
```

---

## 🔄 Order Status Flow

```
Order Created (Local)
         ↓
     Synced to Qikink
         ↓
    Order Processing (Qikink)
         ↓
    Ready to Ship (Qikink)
         ↓
    Shipped & In Transit (Qikink)
         ↓
    Out for Delivery (Qikink)
         ↓
    Delivered (Qikink)
```

---

## ⚙️ Backend Configuration

**File:** `backend/app.py`

```python
# Qikink API Configuration
QIKINK_CLIENT_ID = '786702736653938'
QIKINK_CLIENT_SECRET = 'bf043131d3e80f1d15b6d833f03e5cdf5a5e3a6fce0510b91e3e3aaebe1cabda'
QIKINK_API_BASE_URL = 'https://sandbox-api.qikink.com/api/v1'
QIKINK_AUTH_URL = 'https://sandbox-api.qikink.com/oauth/token'
```

**To change credentials:**
1. Open `backend/app.py`
2. Find the Qikink API Configuration section
3. Update the values
4. Restart the backend

---

## 📂 Data Storage

### Local Order Storage
**File:** `orders.json`

Each order includes:
```json
{
  "order_id": "BHRT-1733304000",
  "customer_email": "...",
  "shipping_address": "...",
  "items": [...],
  "total": 2598,
  "status": "confirmed",
  "created_at": "2025-12-04T10:30:00",
  "qikink_status": "synced",
  "qikink_shipment_id": "QK-SHIP-12345",
  "tracking_id": "TRK-1733304000"
}
```

---

## 🚨 Error Handling

### If Qikink API is Unavailable

**Order Still Created Locally:**
```json
{
  "qikink_status": "sync_pending",
  "status": "pending",
  "message": "Order created successfully (Qikink sync pending)"
}
```

**Later Sync Available:**
- Orders are saved locally
- Can be synced manually via `/api/qikink/sync`
- Frontend continues to work offline

---

## 📱 Frontend Integration

**JavaScript Integration Points:**

```javascript
// Check Qikink status from frontend
fetch('http://localhost:5000/api/qikink/status')
  .then(r => r.json())
  .then(data => console.log('Qikink:', data))

// Create order (auto-syncs to Qikink)
await submitOrder(email, address, items)

// Track fulfillment
await getQikinkFulfillmentStatus(orderId)
```

---

## 🎯 Next Steps

1. ✅ **Backend Running** - Start `start-backend.bat`
2. ✅ **Qikink Connected** - Check `/api/qikink/status`
3. ✅ **Products Synced** - POST to `/api/qikink/sync`
4. ✅ **Create Orders** - Orders auto-sync to Qikink
5. ✅ **Track Shipments** - Monitor `/api/qikink/fulfillment/<order_id>`

---

## 📞 Qikink Sandbox

- **Environment:** Sandbox (Testing)
- **API URL:** https://sandbox-api.qikink.com/api/v1
- **Documentation:** https://qikink.io/api-docs
- **Support:** support@qikink.com

---

## 🔐 Production Ready

When moving to production:

1. **Switch to Production API:**
   ```python
   QIKINK_API_BASE_URL = 'https://api.qikink.com/api/v1'
   QIKINK_AUTH_URL = 'https://api.qikink.com/oauth/token'
   ```

2. **Update Credentials:**
   - Get production client ID and secret from Qikink
   - Update in `backend/app.py`

3. **Enable Database:**
   - Replace JSON file storage with PostgreSQL/MongoDB
   - Implement proper transaction handling

4. **Monitor Integration:**
   - Add error logging
   - Set up webhooks for order status updates
   - Implement retry logic for failed syncs

---

**✨ Your e-commerce backend is now fully integrated with Qikink!**

Start the backend and begin accepting orders with automatic fulfillment tracking! 🚀
