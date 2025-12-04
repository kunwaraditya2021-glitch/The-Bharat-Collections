// =====================================================
// THE BHARAT COLLECTIONS - Main JavaScript
// =====================================================

// =====================================================
// GLOBAL STATE
// =====================================================

const cart = [];
const wishlist = [];
const API_BASE_URL = 'http://localhost:5000/api';

// Check if backend is available
async function checkBackendConnection() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    if (response.ok) {
      console.log('✓ Backend connected successfully');
      return true;
    }
  } catch (error) {
    console.warn('⚠ Backend not available. Using frontend-only mode.');
    return false;
  }
}

// =====================================================
// INITIALIZE APP
// =====================================================

document.addEventListener('DOMContentLoaded', async function() {
  // Check backend connection first
  await checkBackendConnection();
  
  initializeNavigation();
  initializeFAQ();
  initializeProductFilters();
  updateCartDisplay();
  attachEventListeners();
  initializeLazyLoading();
});

// =====================================================
// NAVIGATION & HEADER
// =====================================================

function initializeNavigation() {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('nav');

  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      nav.classList.toggle('active');
    });
  }

  // Close menu when a link is clicked
  document.querySelectorAll('nav a').forEach(link => {
    link.addEventListener('click', function() {
      if (nav) nav.classList.remove('active');
    });
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
}

// =====================================================
// CART FUNCTIONALITY
// =====================================================

async function addToCart(productId, productName, price, size, color) {
  const quantity = parseInt(document.querySelector(`[data-product-id="${productId}"] .quantity-input`)?.value) || 1;

  const cartItem = {
    id: Date.now(),
    productId,
    productName,
    price,
    size,
    color,
    quantity
  };

  cart.push(cartItem);
  updateCartDisplay();

  // Try to sync with backend
  try {
    const response = await fetch(`${API_BASE_URL}/cart/add`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        sku: productId,
        quantity: quantity,
        size: size,
        color: color
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('✓ Item synced to backend cart');
    }
  } catch (error) {
    console.log('Using frontend cart only');
  }

  showNotification(`${productName} added to cart!`, 'success');
}

function removeFromCart(itemId) {
  const index = cart.findIndex(item => item.id === itemId);
  if (index > -1) {
    cart.splice(index, 1);
  }
  updateCartDisplay();
}

function updateCartDisplay() {
  const cartCount = document.querySelector('.cart-count');
  if (cartCount) {
    cartCount.textContent = cart.length;
  }

  // Store in localStorage
  localStorage.setItem('cart', JSON.stringify(cart));
}

function loadCartFromStorage() {
  const savedCart = localStorage.getItem('cart');
  if (savedCart) {
    return JSON.parse(savedCart);
  }
  return [];
}

// =====================================================
// WISHLIST FUNCTIONALITY
// =====================================================

function addToWishlist(productId, productName) {
  if (!wishlist.find(item => item.productId === productId)) {
    wishlist.push({ productId, productName });
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showNotification(`${productName} added to wishlist!`, 'success');
  } else {
    showNotification('Already in wishlist', 'info');
  }
}

function removeFromWishlist(productId) {
  const index = wishlist.findIndex(item => item.productId === productId);
  if (index > -1) {
    wishlist.splice(index, 1);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
  }
}

// =====================================================
// FAQ ACCORDION
// ===================================================== 

function initializeFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (question) {
      question.addEventListener('click', function() {
        // Close other items
        faqItems.forEach(otherItem => {
          if (otherItem !== item) {
            otherItem.classList.remove('active');
          }
        });

        // Toggle current item
        item.classList.toggle('active');
      });
    }
  });
}

// =====================================================
// PRODUCT FILTERS
// ===================================================== 

function initializeProductFilters() {
  const filterCheckboxes = document.querySelectorAll('.filter-checkbox input');

  filterCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function() {
      applyFilters();
    });
  });
}

function applyFilters() {
  const selectedCategories = Array.from(document.querySelectorAll('.filter-checkbox input:checked'))
    .map(checkbox => checkbox.value);

  const products = document.querySelectorAll('.product-card');

  products.forEach(product => {
    const category = product.getAttribute('data-category');
    if (selectedCategories.length === 0 || selectedCategories.includes(category)) {
      product.style.display = 'block';
      setTimeout(() => product.style.opacity = '1', 10);
    } else {
      product.style.opacity = '0';
      setTimeout(() => product.style.display = 'none', 300);
    }
  });
}

// =====================================================
// PRODUCT SELECTION
// ===================================================== 

function selectSize(element, productId) {
  const sizeGroup = element.parentElement;
  sizeGroup.querySelectorAll('.size-option').forEach(option => {
    option.classList.remove('selected');
  });
  element.classList.add('selected');
  document.querySelector(`[data-product-id="${productId}"]`).setAttribute('data-selected-size', element.textContent);
}

function selectColor(element, productId) {
  const colorGroup = element.parentElement;
  colorGroup.querySelectorAll('.color-option').forEach(option => {
    option.classList.remove('selected');
  });
  element.classList.add('selected');
  document.querySelector(`[data-product-id="${productId}"]`).setAttribute('data-selected-color', element.getAttribute('data-color'));
}

// =====================================================
// PRODUCT FETCHING FROM BACKEND
// =====================================================

async function fetchProducts(category = null, collection = null) {
  try {
    let url = `${API_BASE_URL}/products`;
    const params = new URLSearchParams();
    
    if (category) params.append('category', category);
    if (collection) params.append('collection', collection);
    
    if (params.toString()) {
      url += '?' + params.toString();
    }

    const response = await fetch(url);
    if (response.ok) {
      const data = await response.json();
      console.log('✓ Products loaded from backend:', data.count);
      return data.data;
    }
  } catch (error) {
    console.log('Backend unavailable, using frontend products');
    return null;
  }
}

async function fetchProductBySku(sku) {
  try {
    const response = await fetch(`${API_BASE_URL}/products/${sku}`);
    if (response.ok) {
      const data = await response.json();
      console.log('✓ Product loaded:', data.data.name);
      return data.data;
    }
  } catch (error) {
    console.log('Could not fetch product from backend');
    return null;
  }
}

// =====================================================
// ORDER MANAGEMENT
// =====================================================

async function submitOrder(customerEmail, shippingAddress, items) {
  try {
    const response = await fetch(`${API_BASE_URL}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_email: customerEmail,
        shipping_address: shippingAddress,
        items: items
      })
    });

    if (response.ok) {
      const data = await response.json();
      console.log('✓ Order created:', data.data.order_id);
      return data.data;
    } else {
      throw new Error('Order creation failed');
    }
  } catch (error) {
    console.error('Error creating order:', error);
    return null;
  }
}

async function getOrderStatus(orderId) {
  try {
    const response = await fetch(`${API_BASE_URL}/orders/${orderId}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✓ Order status retrieved:', data.data.status);
      return data.data;
    }
  } catch (error) {
    console.error('Error fetching order:', error);
    return null;
  }
}

async function getQikinkFulfillmentStatus(orderId) {
  try {
    const response = await fetch(`${API_BASE_URL}/qikink/fulfillment/${orderId}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✓ Fulfillment status retrieved');
      return data;
    }
  } catch (error) {
    console.error('Error fetching fulfillment:', error);
    return null;
  }
}

// =====================================================
// FORM HANDLING
// ===================================================== 

async function handleContactForm(event) {
  event.preventDefault();

  const form = event.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData);

  // Validation
  if (!data.name || !data.email || !data.message) {
    showNotification('Please fill all required fields', 'error');
    return;
  }

  if (!isValidEmail(data.email)) {
    showNotification('Please enter a valid email address', 'error');
    return;
  }

  try {
    // Send to backend
    const response = await fetch(`${API_BASE_URL}/contact`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      showNotification('Thank you! We will get back to you soon.', 'success');
      form.reset();
    } else {
      throw new Error('Backend error');
    }
  } catch (error) {
    // Fallback if backend is not available
    console.log('Using frontend-only mode for contact form');
    showNotification('Thank you! We will get back to you soon.', 'success');
    form.reset();
  }
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// =====================================================
// NOTIFICATIONS
// ===================================================== 

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.textContent = message;
  notification.style.cssText = `
    position: fixed;
    top: 80px;
    right: 20px;
    padding: 16px 24px;
    background-color: ${type === 'success' ? '#27AE60' : type === 'error' ? '#E74C3C' : '#7BA395'};
    color: white;
    border-radius: 6px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    z-index: 10000;
    animation: slideInRight 0.3s ease;
  `;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.style.animation = 'slideOutRight 0.3s ease';
    setTimeout(() => notification.remove(), 300);
  }, 3000);
}

// =====================================================
// UTILITY FUNCTIONS
// ===================================================== 

function formatPrice(price) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR'
  }).format(price);
}

function slugify(text) {
  if (typeof text !== 'string') {
    return '';
  }
  return text
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, '')
    .replace(/[\s_]+/g, '-')
    .replace(/^-+|-+$/g, '');
}

// =====================================================
// ANIMATION OBSERVER
// ===================================================== 

function initializeAnimationObserver() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'slideInUp 0.6s ease forwards';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.collection-card, .product-card, .testimonial-card').forEach(card => {
    observer.observe(card);
  });
}

// =====================================================
// EVENT LISTENERS SETUP
// ===================================================== 

function attachEventListeners() {
  // Contact form
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', handleContactForm);
  }

  // Initialize animations
  initializeAnimationObserver();

  // Setup cart icon click
  const cartIcon = document.querySelector('.cart-icon');
  if (cartIcon) {
    cartIcon.addEventListener('click', function() {
      // Could open a cart modal or navigate to cart page
      window.location.href = '#cart';
    });
  }
}

// =====================================================
// SEARCH FUNCTIONALITY
// ===================================================== 

function searchProducts(query) {
  const products = document.querySelectorAll('.product-card');
  const lowerQuery = query.toLowerCase();

  products.forEach(product => {
    const name = product.querySelector('.product-name')?.textContent.toLowerCase() || '';
    const category = product.querySelector('.product-category')?.textContent.toLowerCase() || '';
    const description = product.querySelector('.product-description')?.textContent.toLowerCase() || '';

    if (name.includes(lowerQuery) || category.includes(lowerQuery) || description.includes(lowerQuery)) {
      product.style.display = 'block';
    } else {
      product.style.display = 'none';
    }
  });
}

// =====================================================
// SORT FUNCTIONALITY
// ===================================================== 

function sortProducts(sortBy) {
  const productsContainer = document.querySelector('.products-grid');
  if (!productsContainer) return;

  const products = Array.from(document.querySelectorAll('.product-card'));

  products.sort((a, b) => {
    const priceA = parseFloat(a.getAttribute('data-price') || 0);
    const priceB = parseFloat(b.getAttribute('data-price') || 0);

    switch(sortBy) {
      case 'price-low':
        return priceA - priceB;
      case 'price-high':
        return priceB - priceA;
      case 'name-asc':
        const nameA = a.querySelector('.product-name')?.textContent || '';
        const nameB = b.querySelector('.product-name')?.textContent || '';
        return nameA.localeCompare(nameB);
      case 'newest':
        return 0; // Assuming order in DOM is newest
      default:
        return 0;
    }
  });

  products.forEach(product => {
    productsContainer.appendChild(product);
  });
}

// =====================================================
// LAZY LOADING IMAGES
// ===================================================== 

function initializeLazyLoading() {
  const images = document.querySelectorAll('img[data-lazy]');

  if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.getAttribute('data-lazy');
          img.removeAttribute('data-lazy');
          imageObserver.unobserve(img);
        }
      });
    });

    images.forEach(img => imageObserver.observe(img));
  } else {
    // Fallback for older browsers
    images.forEach(img => {
      img.src = img.getAttribute('data-lazy');
      img.removeAttribute('data-lazy');
    });
  }
}

// =====================================================
// ANIMATIONS CSS
// ===================================================== 

const style = document.createElement('style');
style.textContent = `
  @keyframes slideInRight {
    from {
      opacity: 0;
      transform: translateX(100px);
    }
    to {
      opacity: 1;
      transform: translateX(0);
    }
  }

  @keyframes slideOutRight {
    from {
      opacity: 1;
      transform: translateX(0);
    }
    to {
      opacity: 0;
      transform: translateX(100px);
    }
  }

  @keyframes slideInUp {
    from {
      opacity: 0;
      transform: translateY(30px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }
`;
document.head.appendChild(style);

// =====================================================
// DYNAMIC PRODUCT LOADING
// =====================================================

async function loadDynamicProducts() {
  // Load products from backend on shop page
  if (document.querySelector('.products-grid')) {
    const products = await fetchProducts();
    
    if (products && products.length > 0) {
      populateProductsGrid(products);
      console.log('✓ Products dynamically loaded');
    }
  }
}

function populateProductsGrid(products) {
  const grid = document.querySelector('.products-grid');
  if (!grid) return;

  grid.innerHTML = '';

  products.forEach(product => {
    const productCard = document.createElement('div');
    productCard.className = 'product-card';
    productCard.setAttribute('data-category', product.category);
    productCard.setAttribute('data-price', product.price);
    productCard.setAttribute('data-product-id', product.sku);

    productCard.innerHTML = `
      <div class="product-image">
        <img src="${product.image_url}" alt="${product.name}" onerror="this.textContent='👕'">
        ${product.stock <= 5 ? '<span class="badge">LOW STOCK</span>' : '<span class="badge">IN STOCK</span>'}
      </div>
      <div class="product-info">
        <p class="product-category">${product.category}</p>
        <h4 class="product-name">${product.name}</h4>
        <p class="product-description">${product.description}</p>
        <p class="product-sku">SKU: ${product.sku}</p>
        <p class="product-price">₹${product.price.toLocaleString('en-IN')}</p>
        <div class="product-actions">
          <a href="product-detail.html?sku=${product.sku}" class="btn btn-outline" style="flex: 1;">View</a>
          <button class="btn btn-primary" onclick="addToCart('${product.sku}', '${product.name}', ${product.price})" style="flex: 1;">Add</button>
        </div>
      </div>
    `;

    grid.appendChild(productCard);
  });

  // Update product count
  const countSpan = document.querySelector('#product-count');
  if (countSpan) {
    countSpan.textContent = products.length;
  }
}

// Initialize lazy loading
initializeLazyLoading();

// Load dynamic products if on shop page
document.addEventListener('DOMContentLoaded', loadDynamicProducts);
