# The Bharat Collections - E-Commerce Website

A professional, responsive e-commerce website for premium Indian casual wear featuring modern minimal design with earthy, culturally rooted aesthetics.

## 🎨 Design Features

- **Primary Color**: #7BA395 (Sage Green)
- **Secondary Accent**: #E38C52 (Warm Orange)
- **Background**: #F7FFF6 (Soft Fresh White)
- **Theme**: Elegant, earthy, culturally rooted with youthful contemporary vibe
- **Responsive**: Mobile-first approach, fully optimized for all devices
- **Performance**: Lightweight, SEO-friendly, fast-loading pages

## 📁 Project Structure

```
THE BHARAT COLLECTIONS/
├── index.html                 # Home page
├── css/
│   └── styles.css            # Main stylesheet with brand colors
├── js/
│   └── script.js             # Frontend JavaScript with API integration
├── pages/
│   ├── about.html            # About Us page
│   ├── contact.html          # Contact page
│   ├── faq.html              # FAQ page
│   ├── product-detail.html   # Product detail page
│   └── shop.html             # Shop with filters
├── backend/
│   ├── app.py                # Flask backend server
│   └── orders.json           # Orders database (auto-created)
├── images/                   # Product images and assets
└── README.md                 # This file
```

## 🚀 Quick Start

### Frontend Only (No Backend)

1. Open `index.html` in your web browser
2. Browse products, shop, and explore all pages
3. Cart functionality works locally using browser storage

### With Backend Integration (Recommended)

#### Prerequisites
- Python 3.8+
- pip (Python package manager)

#### Setup Steps

1. **Navigate to project folder:**
   ```powershell
   cd "C:\Users\adity\Desktop\THE BHARAT COLLECTIONS"
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Start the Flask backend:**
   ```powershell
   python backend/app.py
   ```

   You should see:
   ```
   ✓ Backend connected successfully
   * Running on http://0.0.0.0:5000
   ```

4. **Open website in browser:**
   ```
   file:///C:/Users/adity/Desktop/THE BHARAT COLLECTIONS/index.html
   ```

The website will automatically detect the backend and sync:
- ✓ Product catalog
- ✓ Cart operations
- ✓ Contact form submissions
- ✓ Order management
- ✓ Qikink fulfillment integration

## 📋 Pages Overview

### Home (`index.html`)
- Hero banner with brand story
- Collections showcase
- USP sections: "Made for Modern Bharat", "Premium Fabric", "Pan-India Delivery"
- Customer testimonials
- Call-to-action sections

### Shop (`pages/shop.html`)
- Responsive product grid
- Category filters (Men's, Women's, Unisex)
- Collection filters (Heritage Prints, Basics, Summer)
- Price range filters
- Sort options (Price, Name, Newest)
- Dynamic product loading from backend

### Product Detail (`pages/product-detail.html`)
- Product images and information
- Size and color selection
- Stock availability
- Quantity selector
- Add to cart & wishlist
- Product metadata (SKU, manufacturer, origin)

### About Us (`pages/about.html`)
- Brand story and mission
- Values and vision
- Team section (with placeholders)
- Manufacturing & sustainability info

### Contact (`pages/contact.html`)
- Contact form with validation
- Customer support information
- Qikink partnership details
- Pan-India delivery coverage

### FAQs (`pages/faq.html`)
- Comprehensive Q&A sections
- Accordion interface
- Product care, shipping, returns
- Expandable answers

## 🔌 Backend API Endpoints

### Products
- `GET /api/products` - Get all products with optional filters
- `GET /api/products/<sku>` - Get specific product by SKU

### Cart
- `POST /api/cart/add` - Add item to cart

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<order_id>` - Get order details

### Contact
- `POST /api/contact` - Submit contact form

### Qikink Integration
- `POST /api/qikink/sync` - Sync inventory with Qikink
- `GET /api/qikink/fulfillment/<order_id>` - Get fulfillment status

### Utility
- `GET /api/health` - Health check
- `GET /api/docs` - API documentation

## 📦 Sample Product Data

The backend includes sample products with SKUs:
- **BHRT-001-M**: Heritage Print T-Shirt (₹1,299)
- **BHRT-002-W**: Indigo Block Print Kurti (₹1,599)
- **BHRT-003-U**: Essential White Basics (₹899)

All products are ready for Qikink integration with:
- Size matrix (XS to XXL)
- Color variants (cream, grey, black, indigo, white)
- Stock tracking
- Image URLs

## 🎯 Key Features

### ✨ Frontend Features
- Responsive grid layouts
- Smooth animations and transitions
- Cart management (localStorage)
- Wishlist functionality
- Product filtering and sorting
- Form validation
- Notification system
- Lazy loading images
- Mobile menu toggle
- Breadcrumb navigation

### 🔧 Backend Features
- RESTful API architecture
- CORS enabled for frontend communication
- Product catalog management
- Order processing
- Contact form handling
- Qikink integration hooks
- Error handling
- Health check endpoints
- JSON data persistence

## 🛠️ Customization

### Update Brand Colors
Edit in `css/styles.css`:
```css
:root {
  --color-primary: #7BA395;      /* Sage Green */
  --color-secondary: #E38C52;    /* Warm Orange */
  --color-background: #F7FFF6;   /* Fresh White */
  /* ... other colors ... */
}
```

### Add Products
Update `backend/app.py` in the `PRODUCTS` dictionary with new SKUs and details.

### Customize API Base URL
In `js/script.js`, change:
```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## 📱 Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## 🔐 Notes for Production

Before deploying to production:

1. **Environment Variables**: Use `.env` file for API URLs
2. **Database**: Replace JSON storage with proper database (MongoDB, PostgreSQL)
3. **Authentication**: Add user registration and login
4. **Payments**: Integrate with Razorpay/Stripe
5. **Security**: Enable HTTPS, add API authentication tokens
6. **Performance**: Enable caching, CDN for static assets
7. **Monitoring**: Add error tracking and analytics

## 📞 Support

For issues or questions about the Qikink integration, refer to:
- `backend/app.py` - Contains detailed API documentation
- `/api/docs` - Live API documentation endpoint

## 📄 License

This project is created for The Bharat Collections brand.

---

**Made with ❤️ for Modern Bharat**
