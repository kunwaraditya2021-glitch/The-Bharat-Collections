# API Quick Reference & Testing Guide

## ⚡ Quick Links (When Backend is Running)

| Function | URL |
|----------|-----|
| **Health Check** | http://localhost:5000/api/health |
| **API Docs** | http://localhost:5000/api/docs |
| **All Products** | http://localhost:5000/api/products |
| **Mens Products** | http://localhost:5000/api/products?category=mens |
| **Womens Products** | http://localhost:5000/api/products?category=womens |
| **Heritage Collection** | http://localhost:5000/api/products?collection=heritage |
| **Single Product** | http://localhost:5000/api/products/BHRT-001-M |

---

## 🧪 Testing with cURL or Postman

### Test Health Check
```bash
curl http://localhost:5000/api/health
```

### Get All Products
```bash
curl http://localhost:5000/api/products
```

### Get Product by Category
```bash
curl "http://localhost:5000/api/products?category=mens"
```

### Get Single Product
```bash
curl http://localhost:5000/api/products/BHRT-001-M
```

### Add to Cart (POST)
```bash
curl -X POST http://localhost:5000/api/cart/add \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "BHRT-001-M",
    "quantity": 2,
    "size": "M",
    "color": "cream"
  }'
```

### Create Order (POST)
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer_email": "user@example.com",
    "shipping_address": "123 Main St, City, State 12345",
    "items": [
      {
        "sku": "BHRT-001-M",
        "quantity": 1,
        "price": 1299
      }
    ]
  }'
```

### Submit Contact Form (POST)
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91-9876543210",
    "subject": "Product Inquiry",
    "category": "product_question",
    "message": "Do you have XL size available?"
  }'
```

### Get Order Status
```bash
curl http://localhost:5000/api/orders/BHRT-1733304000
```

### Get Qikink Fulfillment Status
```bash
curl http://localhost:5000/api/qikink/fulfillment/BHRT-1733304000
```

---

## 📱 Testing from Browser

### 1. Check Health
Open this in your browser:
```
http://localhost:5000/api/health
```

### 2. View All Products
```
http://localhost:5000/api/products
```

You'll see JSON with all products.

### 3. Filter Products
```
http://localhost:5000/api/products?category=womens
http://localhost:5000/api/products?collection=basics
http://localhost:5000/api/products?category=mens&collection=heritage
```

### 4. Get Single Product
```
http://localhost:5000/api/products/BHRT-001-M
```

---

## 🔍 JavaScript Console Testing

Open DevTools (F12) and run these in the Console:

### Test Product Fetch
```javascript
fetchProducts().then(data => console.log(data))
```

### Test Single Product
```javascript
fetchProductBySku('BHRT-001-M').then(data => console.log(data))
```

### Test Add to Cart
```javascript
addToCart('BHRT-001-M', 'Heritage Print T-Shirt', 1299, 'M', 'cream')
```

### Test Contact Form
```javascript
fetch('http://localhost:5000/api/contact', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Test User',
    email: 'test@example.com',
    message: 'Test message'
  })
}).then(r => r.json()).then(d => console.log(d))
```

### Check Cart
```javascript
console.log(cart)
```

### Check Saved Orders (from JSON file)
Check the project folder for `orders.json` file created after orders.

---

## 📊 Sample API Responses

### Products List Response
```json
{
  "status": "success",
  "count": 3,
  "data": [
    {
      "sku": "BHRT-001-M",
      "name": "Heritage Print T-Shirt",
      "category": "mens",
      "collection": "heritage",
      "price": 1299,
      "description": "Premium cotton with traditional Madhubani art print",
      "sizes": ["XS", "S", "M", "L", "XL", "XXL"],
      "colors": ["cream", "grey", "black"],
      "stock": 15,
      "image_url": "/images/product-001.jpg",
      "manufacturer": "Qikink",
      "made_in": "India"
    }
  ]
}
```

### Cart Add Response
```json
{
  "status": "success",
  "message": "1 item(s) added to cart",
  "product": {...},
  "cart_item": {
    "sku": "BHRT-001-M",
    "quantity": 2,
    "size": "M",
    "color": "cream",
    "total_price": 2598
  }
}
```

### Order Response
```json
{
  "status": "success",
  "message": "Order created successfully",
  "data": {
    "order_id": "BHRT-1733304000",
    "customer_email": "user@example.com",
    "shipping_address": "123 Main St, City",
    "items": [...],
    "total": 3897,
    "status": "pending",
    "created_at": "2025-12-04T10:30:00",
    "qikink_status": "order_received",
    "tracking_id": null
  }
}
```

---

## 🛠️ Postman Collection

You can import this collection into Postman for easy testing.

**Request 1: Get All Products**
- Method: GET
- URL: `http://localhost:5000/api/products`

**Request 2: Get Single Product**
- Method: GET
- URL: `http://localhost:5000/api/products/BHRT-001-M`

**Request 3: Add to Cart**
- Method: POST
- URL: `http://localhost:5000/api/cart/add`
- Body (JSON):
  ```json
  {
    "sku": "BHRT-001-M",
    "quantity": 1,
    "size": "M",
    "color": "cream"
  }
  ```

**Request 4: Create Order**
- Method: POST
- URL: `http://localhost:5000/api/orders`
- Body (JSON):
  ```json
  {
    "customer_email": "customer@example.com",
    "shipping_address": "Address here",
    "items": [
      {
        "sku": "BHRT-001-M",
        "quantity": 1,
        "price": 1299
      }
    ]
  }
  ```

---

## 🔑 SKU Reference

| SKU | Product | Price | Category | Collection |
|-----|---------|-------|----------|-----------|
| BHRT-001-M | Heritage Print T-Shirt | ₹1,299 | Men's | Heritage |
| BHRT-002-W | Indigo Block Print Kurti | ₹1,599 | Women's | Heritage |
| BHRT-003-U | Essential White Basics | ₹899 | Unisex | Basics |
| BHRT-004-M | Breathable Summer Shirt | ₹1,199 | Men's | Summer |
| BHRT-005-W | Flowy Summer Dress | ₹1,399 | Women's | Summer |
| BHRT-006-U | Charcoal Grey Essential | ₹1,099 | Unisex | Basics |
| BHRT-007-M | Paisley Pattern Shirt | ₹1,799 | Men's | Heritage |

---

## 🚨 Error Handling

### If backend is not running
```javascript
// Frontend automatically detects and logs:
"⚠ Backend not available. Using frontend-only mode."
```

### If product not found
```json
{
  "status": "error",
  "message": "Product not found"
}
```

### If missing required fields
```json
{
  "status": "error",
  "message": "Missing required fields"
}
```

---

## 💡 Pro Tips

1. **Monitor Console**: Open DevTools (F12) → Console to see backend connection logs
2. **Check Network Tab**: See actual API requests being made
3. **Test Offline**: Close backend and site still works in frontend-only mode
4. **JSON Files**: Check `orders.json` and `contact_submissions.json` in project root
5. **Scale Products**: Add more products to `PRODUCTS` dict in `backend/app.py`

---

**Ready to test? Start the backend and begin exploring! 🚀**
