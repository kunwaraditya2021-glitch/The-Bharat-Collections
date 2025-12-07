"""
The Bharat Collections - Flask Backend with Mediator Admin Interface
Complete integration with Supabase, Qikink API, and Razorpay
ALL-IN-ONE FILE for easy deployment on free hosting
"""

from flask import Flask, render_template, request, jsonify, send_from_directory, g
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
import requests
import hashlib
import hmac
import base64
from functools import wraps
from typing import Optional, Dict, List, Any
import logging
from logging.handlers import RotatingFileHandler
import atexit
from typing import Any

# Try to import external dependencies (used in the original app.py's conditional logic)
# This keeps the spirit of the original file, checking if features are available.
SUPABASE_AVAILABLE = False
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    Client = Any  # Fallback type when Supabase not installed
    pass

RAZORPAY_AVAILABLE = False
try:
    import razorpay
    RAZORPAY_AVAILABLE = True
except ImportError:
    pass

JWT_AVAILABLE = False
try:
    import jwt as pyjwt
    import bcrypt
    JWT_AVAILABLE = True
except ImportError:
    pass

SCHEDULER_AVAILABLE = False
try:
    from apscheduler.schedulers.background import BackgroundScheduler
    from apscheduler.triggers.interval import IntervalTrigger
    SCHEDULER_AVAILABLE = True
except ImportError:
    pass

# Environment Variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# HTTP Retry Logic (from mediator_services.py)
try:
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    RETRY_AVAILABLE = True
except ImportError:
    HTTPAdapter = None
    Retry = None
    RETRY_AVAILABLE = False

# =====================================================
# FLASK APP INITIALIZATION
# =====================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, 
            static_folder=os.path.join(PROJECT_ROOT, 'static'),
            static_url_path='/static',
            template_folder=os.path.join(PROJECT_ROOT, 'templates'))

CORS(app, resources={r"/*": {"origins": "*"}})

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(PROJECT_ROOT, 'uploads')
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# =====================================================
# CONFIGURATION - API CREDENTIALS
# =====================================================

# Qikink API Configuration
QIKINK_CLIENT_ID = os.getenv('QIKINK_CLIENT_ID', '786702736653938')
QIKINK_CLIENT_SECRET = os.getenv('QIKINK_CLIENT_SECRET', 'bf043131d3e80f1d15b6d833f03e5cdf5a5e3a6fce0510b91e3e3aaebe1cabda')
QIKINK_API_BASE_URL = os.getenv('QIKINK_API_BASE_URL', 'https://sandbox-api.qikink.com/api/v1')
QIKINK_AUTH_URL = os.getenv('QIKINK_AUTH_URL', 'https://sandbox-api.qikink.com/oauth/token')

# Supabase Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_KEY', '')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', SUPABASE_KEY)

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')

# JWT Configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'dev-jwt-secret-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_HOURS = int(os.getenv('JWT_EXPIRATION_HOURS', 24))
JWT_REFRESH_TOKEN_EXPIRATION_DAYS = int(os.getenv('JWT_REFRESH_TOKEN_EXPIRATION_DAYS', 30))

# =====================================================
# LOGGING CONFIGURATION
# =====================================================

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/mediator.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Backend Mediator Startup')


# =====================================================
# MEDIATOR SERVICE CLASSES (from mediator_services.py)
# =====================================================

class DatabaseService:
    """Mediator service for all Supabase database operations"""
    
    def __init__(self, supabase_client: Any):
        self.db = supabase_client
    
    # ==================== PRODUCT OPERATIONS ====================
    
    def sync_products_to_db(self, products: List[Dict]) -> Dict:
        """Sync products to Supabase"""
        try:
            synced_count = 0
            for product in products:
                # Upsert product (insert or update if exists)
                self.db.table('products').upsert({
                    'sku': product['sku'],
                    'name': product['name'],
                    'description': product.get('description'),
                    'price': product['price'],
                    'category': product.get('category'),
                    'collection': product.get('collection'),
                    'manufacturer': product.get('manufacturer'),
                    'made_in': product.get('made_in'),
                    'image_url': product.get('image_url'),
                    'qikink_product_id': product.get('qikink_product_id'),
                    'updated_at': datetime.now().isoformat()
                }, on_conflict='sku').execute()
                synced_count += 1
            
            return {'status': 'success', 'synced': synced_count}
        except Exception as e:
            app.logger.error(f'[ERROR] Database sync failed: {str(e)}')
            return {'status': 'error', 'message': str(e)}
    
    def get_products_from_db(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get products from Supabase with optional filters"""
        try:
            query = self.db.table('products').select('*')
            
            if filters:
                if filters.get('category'):
                    query = query.eq('category', filters['category'])
                if filters.get('collection'):
                    query = query.eq('collection', filters['collection'])
            
            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to fetch products: {str(e)}')
            return []
    
    # ==================== ORDER OPERATIONS ====================
    
    def create_order_in_db(self, order_data: Dict) -> Optional[Dict]:
        """Create order in Supabase"""
        try:
            result = self.db.table('orders').insert({
                'order_id': order_data['order_id'],
                'customer_email': order_data['customer_email'],
                'customer_name': order_data.get('customer_name'),
                'customer_phone': order_data.get('customer_phone'),
                'shipping_address': order_data['shipping_address'],
                'shipping_city': order_data.get('shipping_city'),
                'shipping_state': order_data.get('shipping_state'),
                'shipping_pincode': order_data.get('shipping_pincode'),
                'items': json.dumps(order_data['items']),
                'total_amount': order_data['total_amount'],
                'status': order_data.get('status', 'pending'),
                'razorpay_order_id': order_data.get('razorpay_order_id'),
                'notes': order_data.get('notes')
            }).execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to create order: {str(e)}')
            return None
    
    def update_order_status(self, order_id: str, status: str, qikink_order_id: Optional[str] = None, 
                           qikink_shipment_id: Optional[str] = None, tracking_number: Optional[str] = None) -> bool:
        """Update order status"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            
            if qikink_order_id:
                update_data['qikink_order_id'] = qikink_order_id
            if qikink_shipment_id:
                update_data['qikink_shipment_id'] = qikink_shipment_id
            if tracking_number:
                update_data['tracking_number'] = tracking_number
            
            self.db.table('orders').update(update_data).eq('order_id', order_id).execute()
            return True
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to update order status: {str(e)}')
            return False
    
    def get_order_by_id(self, order_id: str) -> Optional[Dict]:
        """Get order details by order_id"""
        try:
            result = self.db.table('orders').select('*').eq('order_id', order_id).execute()
            if result.data:
                order = result.data[0]
                # Parse JSON items
                if isinstance(order.get('items'), str):
                    order['items'] = json.loads(order['items'])
                return order
            return None
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to get order: {str(e)}')
            return None

    def get_orders_by_status(self, statuses: List[str]) -> List[Dict]:
        """Get orders based on a list of statuses"""
        try:
            # Use `in_` for checking if status is in the list
            result = self.db.table('orders').select('*').in_('status', statuses).execute()
            return result.data if result.data else []
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to get orders by status: {str(e)}')
            return []

    # ==================== PAYMENT OPERATIONS ====================

    def create_payment_record(self, payment_data: Dict) -> Optional[Dict]:
        """Create a payment record after verification/capture"""
        try:
            result = self.db.table('payments').insert({
                'razorpay_payment_id': payment_data['razorpay_payment_id'],
                'razorpay_order_id': payment_data['razorpay_order_id'],
                'amount': payment_data['amount'],
                'currency': payment_data.get('currency', 'INR'),
                'status': payment_data.get('status', 'created'),
                'payment_method': payment_data.get('payment_method'),
                'idempotency_key': payment_data.get('idempotency_key'),
                'webhook_processed': payment_data.get('webhook_processed', False)
            }).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to create payment record: {str(e)}')
            return None

    def verify_payment_not_processed(self, idempotency_key: str) -> bool:
        """Check if payment already processed (prevent duplicates)"""
        try:
            result = self.db.table('payments').select('id').eq('idempotency_key', idempotency_key).execute()
            return len(result.data) == 0
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to check idempotency: {str(e)}')
            return False

    # ==================== FAILED JOB OPERATIONS (for retries) ====================

    def add_failed_job(self, job_type: str, order_id: str, payload: Dict, error_message: str) -> bool:
        """Log a failed background job for future retry"""
        try:
            self.db.table('failed_jobs').insert({
                'job_type': job_type,
                'order_id': order_id,
                'payload': json.dumps(payload),
                'error_message': error_message,
                'status': 'pending',
                'retry_count': 0,
                'created_at': datetime.now().isoformat()
            }).execute()
            return True
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to log failed job: {str(e)}')
            return False

    def get_pending_failed_jobs(self, job_type: Optional[str] = None) -> List[Dict]:
        """Retrieve all pending failed jobs, optionally filtered by type"""
        try:
            query = self.db.table('failed_jobs').select('*').eq('status', 'pending').lte('retry_count', 3)
            if job_type:
                query = query.eq('job_type', job_type)

            result = query.execute()
            return result.data if result.data else []
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to get pending failed jobs: {str(e)}')
            return []

    def update_failed_job(self, job_id: int, status: str, retry_count: Optional[int] = None) -> bool:
        """Update the status of a failed job"""
        try:
            update_data = {
                'status': status,
                'updated_at': datetime.now().isoformat()
            }
            if retry_count is not None:
                update_data['retry_count'] = retry_count

            self.db.table('failed_jobs').update(update_data).eq('id', job_id).execute()
            return True
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to update failed job: {str(e)}')
            return False

    # ==================== ADMIN/ANALYTICS OPERATIONS ====================

    def get_dashboard_stats(self) -> Dict:
        """Get dashboard statistics"""
        try:
            orders = self.get_all_orders()
            
            stats = {
                'total_orders': len(orders),
                'pending_orders': len([o for o in orders if o['status'] == 'pending']),
                'payment_verified': len([o for o in orders if o['status'] == 'payment_verified']),
                'qikink_submitted': len([o for o in orders if o['status'] == 'qikink_submitted']),
                'shipped': len([o for o in orders if o['status'] == 'shipped']),
                'delivered': len([o for o in orders if o['status'] == 'delivered']),
                'total_revenue': sum(float(o.get('total_amount', 0)) for o in orders),
                'average_order_value': sum(float(o.get('total_amount', 0)) for o in orders) / len(orders) if orders else 0
            }
            
            return stats
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to get dashboard stats: {str(e)}')
            return {}


class RazorpayMediatorService:
    """Razorpay integration with signature verification and idempotency"""
    
    def __init__(self, razorpay_client, db_service: DatabaseService):
        self.client = razorpay_client
        self.db = db_service
        self.key_secret = RAZORPAY_KEY_SECRET

    def create_order(self, amount: int, currency: str = 'INR', receipt: Optional[str] = None) -> Optional[Dict]:
        """Create Razorpay order"""
        if not self.client:
            app.logger.warning('[WARN] Razorpay client not initialized')
            return None
        try:
            order_data = {
                'amount': amount, # Amount in paise
                'currency': currency,
                'receipt': receipt or f'order_{int(datetime.now().timestamp())}'
            }
            order = self.client.order.create(data=order_data)
            return order
        except Exception as e:
            app.logger.error(f'[ERROR] Failed to create Razorpay order: {str(e)}')
            return None

    def verify_payment_signature(self, order_id: str, payment_id: str, signature: str) -> bool:
        """Verify Razorpay payment signature"""
        try:
            message = f'{order_id}|{payment_id}'
            expected_signature = hmac.new(
                self.key_secret.encode(),
                message.encode(),
                hashlib.sha256
            ).hexdigest()
            return expected_signature == signature
        except Exception as e:
            app.logger.error(f'[ERROR] Signature verification failed: {str(e)}')
            return False

    def process_webhook(self, payload: Dict, signature: str) -> Dict:
        """Process Razorpay webhook with idempotency"""
        try:
            event = payload.get('event')
            payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
            
            # Use the official verify webhook signature method
            self.client.utility.verify_webhook_signature(json.dumps(payload), signature, self.key_secret)
            
            if event == 'payment.captured':
                idempotency_key = f"{payment_entity.get('id')}_captured"
                if not self.db.verify_payment_not_processed(idempotency_key):
                    return {'status': 'duplicate', 'message': 'Already processed'}

                # 1. Create Payment Record
                payment_record = self.db.create_payment_record({
                    'razorpay_payment_id': payment_entity.get('id'),
                    'razorpay_order_id': payment_entity.get('order_id'),
                    'amount': payment_entity.get('amount', 0) / 100,
                    'status': 'captured',
                    'payment_method': payment_entity.get('method'),
                    'idempotency_key': idempotency_key
                })
                
                # 2. Update Order Status
                if payment_entity.get('order_id'):
                    order = self.db.get_order_by_razorpay_id(payment_entity.get('order_id'))
                    if order:
                        self.db.update_order_status(order['order_id'], 'payment_captured')
                        return {'status': 'success', 'order_id': order['order_id'], 'action': 'Order status updated'}

                return {'status': 'success', 'action': 'Payment recorded'}
            
            return {'status': 'ignored', 'message': f'Event {event} ignored'}
        
        except razorpay.errors.SignatureVerificationError:
            app.logger.error('[ERROR] Razorpay Webhook Signature Verification Failed')
            return {'status': 'error', 'message': 'Signature verification failed'}
        except Exception as e:
            app.logger.error(f'[ERROR] Razorpay Webhook Processing Failed: {str(e)}')
            return {'status': 'error', 'message': str(e)}

class QikinkMediatorService:
    """Enhanced Qikink service with retry logic and database integration"""
    
    def __init__(self, client_id: str, client_secret: str, api_base_url: str, auth_url: str, db_service: DatabaseService):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_base_url = api_base_url
        self.auth_url = auth_url
        self.db = db_service
        self.access_token = None
        self.token_expiry = datetime.min
        self.session = self._create_session()

    def _create_session(self):
        """Create a requests session with retry logic"""
        session = requests.Session()
        if RETRY_AVAILABLE:
            retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
        return session

    def authenticate(self) -> bool:
        """Fetch a new access token if expired or not set"""
        if self.access_token and self.token_expiry > datetime.now() + timedelta(minutes=5):
            return True

        try:
            response = self.session.post(
                self.auth_url,
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.client_id,
                    'client_secret': self.client_secret
                },
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data['access_token']
            # Set expiry time a bit before actual expiry (e.g., 1 hour less)
            expires_in = data.get('expires_in', 3600)
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in) - timedelta(hours=1)
            
            app.logger.info('[OK] Qikink token refreshed')
            return True
        except Exception as e:
            app.logger.error(f'[ERROR] Qikink authentication failed: {str(e)}')
            self.access_token = None
            return False

    def get_headers(self) -> Dict:
        """Get authenticated headers"""
        if not self.authenticate():
            raise requests.exceptions.HTTPError('Qikink authentication failed')
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }

    def sync_products(self) -> Dict:
        """Fetch products from Qikink and sync to database"""
        try:
            headers = self.get_headers()
            response = self.session.get(
                f'{self.api_base_url}/products',
                headers=headers,
                timeout=30,
                verify=False
            )
            response.raise_for_status()

            qikink_products = response.json().get('products', [])
            if self.db:
                sync_result = self.db.sync_products_to_db(qikink_products)
                return {
                    'status': 'success',
                    'fetched': len(qikink_products),
                    'synced': sync_result.get('synced', 0)
                }
            else:
                return {'status': 'error', 'message': 'Database not configured'}

        except requests.exceptions.RequestException as e:
            app.logger.error(f'[ERROR] Qikink product sync failed: {str(e)}')
            return {'status': 'error', 'message': f'Qikink API Error: {str(e)}'}
        except Exception as e:
            app.logger.error(f'[ERROR] Product sync failed: {str(e)}')
            return {'status': 'error', 'message': str(e)}

    def submit_order_to_qikink(self, order_id: str) -> Dict:
        """Submit order to Qikink after payment verification"""
        if not self.db:
            return {'status': 'error', 'message': 'Database not configured'}
        
        try:
            order = self.db.get_order_by_id(order_id)
            if not order:
                return {'status': 'error', 'message': 'Order not found'}

            headers = self.get_headers()
            
            # Prepare shipment payload (simplified for example)
            # In a real app, this mapping would be more complex
            shipment_payload = {
                'order_id': order['order_id'],
                'customer_email': order['customer_email'],
                'shipping_address': order['shipping_address'],
                'shipping_city': order['shipping_city'],
                'shipping_state': order['shipping_state'],
                'shipping_pincode': order['shipping_pincode'],
                'items': order['items'],
                'total_amount': float(order['total_amount'])
            }

            response = self.session.post(
                f'{self.api_base_url}/orders',
                headers=headers,
                json=shipment_payload,
                timeout=30,
                verify=False
            )
            
            response.raise_for_status()
            qikink_result = response.json()
            
            qikink_order_id = qikink_result.get('qikink_order_id')
            
            if qikink_result.get('status') == 'success' and qikink_order_id:
                # Update DB with Qikink Order ID and status
                self.db.update_order_status(order_id, 'qikink_submitted', qikink_order_id=qikink_order_id)
                return {
                    'status': 'success',
                    'qikink_order_id': qikink_order_id
                }
            else:
                error_msg = qikink_result.get('message', 'Unknown Qikink error')
                self.db.add_failed_job('qikink_order_submission', order_id, shipment_payload, error_msg)
                return {'status': 'error', 'message': error_msg}
        
        except requests.exceptions.RequestException as e:
            error_msg = f'Qikink API Error: {str(e)}'
            app.logger.error(f'[ERROR] Qikink order submission failed for {order_id}: {error_msg}')
            # Log for retry
            self.db.add_failed_job('qikink_order_submission', order_id, shipment_payload, error_msg)
            return {'status': 'error', 'message': error_msg}
        
        except Exception as e:
            app.logger.error(f'[ERROR] Qikink order submission failed for {order_id}: {str(e)}')
            return {'status': 'error', 'message': str(e)}

    def fetch_tracking_updates(self, qikink_order_id: str) -> Optional[Dict]:
        """Fetch tracking updates from Qikink"""
        try:
            headers = self.get_headers()
            
            response = self.session.get(
                f'{self.api_base_url}/shipments/{qikink_order_id}/status',
                headers=headers,
                timeout=15,
                verify=False
            )
            
            if response.status_code == 200:
                tracking_data = response.json()
                app.logger.info(f'[OK] Tracking fetched for: {qikink_order_id}')
                return tracking_data
            else:
                app.logger.warning(f'[WARN] Tracking fetch failed: {response.status_code}')
                return None
        except Exception as e:
            app.logger.error(f'[ERROR] Tracking fetch error: {str(e)}')
            return None

    def test_connection(self) -> Dict:
        """Test Qikink connectivity"""
        try:
            auth_success = self.authenticate()
            return {
                'status': 'connected' if auth_success else 'failed',
                'authenticated': auth_success
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

# =====================================================
# BACKGROUND JOB HELPERS (from background_jobs.py)
# =====================================================

def create_scheduler(qikink_service: QikinkMediatorService, db_service: DatabaseService):
    """Create and configure background scheduler"""
    
    scheduler = BackgroundScheduler()
    
    # ==================== TRACKING UPDATE JOB ====================
    
    def fetch_all_tracking_updates():
        """Background job: Fetch tracking for all active orders"""
        try:
            app.logger.info(f'[CRON] Fetching tracking updates at {datetime.now()}')
            
            # Get orders that are shipped or in transit
            active_orders = db_service.get_orders_by_status(['qikink_submitted', 'shipped', 'in_transit'])
            
            updated_count = 0
            for order in active_orders:
                if order.get('qikink_order_id'):
                    # Fetch tracking from Qikink
                    tracking = qikink_service.fetch_tracking_updates(order['qikink_order_id'])
                    
                    if tracking:
                        # Simple logic: assume latest status is last entry
                        latest_event = tracking.get('tracking_events', [{}])[-1]
                        new_status = latest_event.get('status')
                        tracking_number = tracking.get('tracking_number')
                        
                        if new_status and new_status != order['status']:
                            db_service.update_order_status(
                                order['order_id'], 
                                new_status.lower().replace(' ', '_'), 
                                tracking_number=tracking_number
                            )
                            # db_service.log_tracking_event(order['order_id'], latest_event) # Needs implementation in DB service
                            updated_count += 1
            
            app.logger.info(f'[CRON] Finished fetching tracking updates. {updated_count} orders updated.')
        except Exception as e:
            app.logger.error(f'[CRON ERROR] Tracking update job failed: {str(e)}')

    # ==================== FAILED ORDER RETRY JOB ====================

    def retry_failed_orders():
        """Background job: Retry failed Qikink order submissions"""
        try:
            app.logger.info(f'[CRON] Starting failed order retry job at {datetime.now()}')
            failed_jobs = db_service.get_pending_failed_jobs('qikink_order_submission')
            success_count = 0

            for job in failed_jobs:
                order_id = job.get('order_id')
                if order_id:
                    # Attempt to re-submit to Qikink
                    retry_result = qikink_service.submit_order_to_qikink(order_id)
                    
                    if retry_result['status'] == 'success':
                        db_service.update_failed_job(job['id'], 'completed')
                        success_count += 1
                    else:
                        # Update retry count
                        new_retry_count = job['retry_count'] + 1
                        MAX_RETRIES = 3 # Hardcoded limit, should be config
                        
                        if new_retry_count > MAX_RETRIES:
                            db_service.update_failed_job(job['id'], 'failed')
                            app.logger.warning(f'[CRON] Max retries reached for order {order_id}')
                        else:
                            db_service.update_failed_job(job['id'], 'pending', retry_count=new_retry_count)
            
            app.logger.info(f'[CRON] Successfully retried {success_count}/{len(failed_jobs)} failed orders')
        except Exception as e:
            app.logger.error(f'[CRON ERROR] Retry job failed: {str(e)}')
    
    # ==================== SCHEDULE JOBS ====================
    
    # Tracking updates every 3 hours
    tracking_interval = int(os.getenv('TRACKING_UPDATE_INTERVAL', 3))
    scheduler.add_job(
        func=fetch_all_tracking_updates,
        trigger=IntervalTrigger(hours=tracking_interval),
        id='fetch_tracking',
        name='Fetch tracking updates',
        replace_existing=True
    )
    
    # Retry failed orders every 30 minutes
    retry_interval = int(os.getenv('RETRY_INTERVAL', 30))
    scheduler.add_job(
        func=retry_failed_orders,
        trigger=IntervalTrigger(minutes=retry_interval),
        id='retry_failed',
        name='Retry failed orders',
        replace_existing=True
    )
    
    app.logger.info('[OK] Background scheduler configured')
    return scheduler

# =====================================================
# CLIENT AND SERVICE INITIALIZATION (from app_integration.py)
# =====================================================

# Initialize Supabase client
supabase_client = None
if SUPABASE_AVAILABLE and SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        app.logger.info('[OK] Supabase client initialized')
    except Exception as e:
        app.logger.warning(f'[WARN] Supabase connection failed: {str(e)}')

# Initialize Razorpay client
razorpay_client = None
if RAZORPAY_AVAILABLE and RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET:
    try:
        razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        app.logger.info('[OK] Razorpay client initialized')
    except Exception as e:
        app.logger.warning(f'[WARN] Razorpay initialization failed: {str(e)}')

# Initialize Database Service
db_service = DatabaseService(supabase_client) if supabase_client else None

# Initialize Razorpay Mediator Service
razorpay_mediator = RazorpayMediatorService(razorpay_client, db_service) if razorpay_client and db_service else None

# Initialize Enhanced Qikink Mediator Service
qikink_mediator = QikinkMediatorService(
    QIKINK_CLIENT_ID,
    QIKINK_CLIENT_SECRET,
    QIKINK_API_BASE_URL,
    QIKINK_AUTH_URL,
    db_service
) if db_service else None


# =====================================================
# JWT AUTHENTICATION HELPERS (from auth_helpers.py)
# =====================================================

def generate_jwt_token(user_id: str, role: str = 'user', is_refresh: bool = False) -> str:
    """Generate JWT token (access or refresh)"""
    if not JWT_AVAILABLE:
        return 'JWT_NOT_AVAILABLE'
    
    expiration = timedelta(hours=JWT_EXPIRATION_HOURS)
    if is_refresh:
        expiration = timedelta(days=JWT_REFRESH_TOKEN_EXPIRATION_DAYS)

    payload = {
        'user_id': user_id,
        'role': role,
        'type': 'refresh' if is_refresh else 'access',
        'exp': datetime.utcnow() + expiration,
        'iat': datetime.utcnow()
    }
    return pyjwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    if not JWT_AVAILABLE:
        return None
    
    try:
        payload = pyjwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except pyjwt.ExpiredSignatureError:
        return None
    except pyjwt.InvalidTokenError:
        return None

def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    if not JWT_AVAILABLE:
        return password
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash"""
    if not JWT_AVAILABLE:
        return password == hashed
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def require_auth(f):
    """Decorator to require any authentication (user or admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'status': 'error', 'message': 'No token provided'}), 401
        
        token = auth_header.replace('Bearer ', '')
        payload = verify_jwt_token(token)
        
        if not payload or payload.get('type') != 'access':
            return jsonify({'status': 'error', 'message': 'Invalid or expired access token'}), 401
        
        # Add user info to request context
        g.user_id = payload.get('user_id')
        g.user_role = payload.get('role')
        
        return f(*args, **kwargs)
    return decorated_function

def require_admin(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        # require_auth already ran and set g.user_role
        if g.user_role != 'admin':
            return jsonify({'status': 'error', 'message': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


# =====================================================
# SAMPLE PRODUCT DATA (FALLBACK)
# =====================================================

PRODUCTS = {
    'BHRT-001-M': {
        'sku': 'BHRT-001-M',
        'name': 'Heritage Print T-Shirt',
        'category': 'mens',
        'collection': 'heritage',
        'price': 1299,
        'description': 'Premium cotton with traditional Madhubani art print',
        'sizes': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        'colors': ['cream', 'grey', 'black'],
        'stock': 15,
        'image_url': '/images/product-001.jpg',
        'manufacturer': 'Qikink',
        'made_in': 'India'
    },
    'BHRT-002-W': {
        'sku': 'BHRT-002-W',
        'name': 'Indigo Block Print Kurti',
        'category': 'womens',
        'collection': 'heritage',
        'price': 1599,
        'description': 'Hand block printed indigo cotton kurti',
        'sizes': ['S', 'M', 'L', 'XL'],
        'colors': ['indigo'],
        'stock': 8,
        'image_url': '/images/product-002.jpg',
        'manufacturer': 'Local Artisan',
        'made_in': 'India'
    }
}

# =====================================================
# BACKGROUND SCHEDULER MANAGEMENT
# =====================================================

# Initialize background scheduler
scheduler = None
if SCHEDULER_AVAILABLE and qikink_mediator and db_service:
    try:
        scheduler = create_scheduler(qikink_mediator, db_service)
        scheduler.start()
        app.logger.info('[OK] Background scheduler started')
    except Exception as e:
        app.logger.warning(f'[WARN] Failed to start scheduler: {str(e)}')

# Shutdown handler
def shutdown_scheduler():
    """Shutdown scheduler on app exit"""
    if scheduler:
        scheduler.shutdown()
        app.logger.info('[OK] Background scheduler stopped')

atexit.register(shutdown_scheduler)

# =====================================================
# FLASK ROUTES / API ENDPOINTS
# =====================================================

@app.route('/', methods=['GET'])
def index():
    """Serve the homepage"""
    return render_template('index.html')

@app.route('/index.html', methods=['GET'])
def index_alt():
    """Alternative route for index.html"""
    return render_template('index.html')

@app.route('/shop', methods=['GET'])
@app.route('/shop.html', methods=['GET'])
def shop():
    """Serve the shop page"""
    return render_template('shop.html')

@app.route('/product-detail', methods=['GET'])
@app.route('/product-detail.html', methods=['GET'])
def product_detail():
    """Serve the product detail page"""
    return render_template('product-detail.html')

@app.route('/about', methods=['GET'])
@app.route('/about.html', methods=['GET'])
def about():
    """Serve the about page"""
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
@app.route('/contact.html', methods=['GET'])
def contact_page():
    """Serve the contact page"""
    return render_template('contact.html')

@app.route('/faq', methods=['GET'])
@app.route('/faq.html', methods=['GET'])
def faq():
    """Serve the FAQ page"""
    return render_template('faq.html')

@app.route('/admin', methods=['GET'])
def admin_panel():
    """Serve admin panel with URL security key"""
    security_key = request.args.get('key')
    admin_secret = os.getenv('ADMIN_SECRET_KEY', 'bharat_admin_2905')
    
    # Check if security key matches
    if security_key != admin_secret:
        return jsonify({'status': 'error', 'message': 'Invalid or missing security key'}), 403
    
    return render_template('admin.html', security_key=admin_secret)

@app.route('/api', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'service': 'The Bharat Collections API',
        'status': 'running',
        'version': '2.0',
        'mediator': 'enabled',
        'features': {
            'supabase': supabase_client is not None,
            'razorpay': razorpay_client is not None,
            'qikink': qikink_mediator is not None,
            'jwt_auth': JWT_AVAILABLE,
            'background_jobs': SCHEDULER_AVAILABLE
        }
    }), 200

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check the health of integrated services"""
    qikink_status = qikink_mediator.test_connection() if qikink_mediator else {'status': 'not_configured'}
    razorpay_status = {'status': 'connected'} # Simplified check since there's no official test method
    supabase_status = {'status': 'connected' if supabase_client else 'not_configured'}
    
    return jsonify({
        'status': 'healthy',
        'service': 'The Bharat Collections API',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'dependencies': {
            'qikink': qikink_status,
            'razorpay': razorpay_status,
            'supabase': supabase_status
        }
    }), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    """Fetch products from DB, fallback to local data"""
    products = db_service.get_products_from_db() if db_service else []
    
    if not products:
        products = list(PRODUCTS.values()) # Fallback to sample data

    return jsonify({
        'status': 'success',
        'count': len(products),
        'products': products
    }), 200

@app.route('/api/admin/sync-products', methods=['POST'])
@require_admin
def sync_products():
    """Admin endpoint to force product sync from Qikink"""
    if not qikink_mediator:
        return jsonify({'status': 'error', 'message': 'Qikink service not configured'}), 503
    
    result = qikink_mediator.sync_products()
    return jsonify(result), 200

# =====================================================
# API ENDPOINTS - AUTHENTICATION
# =====================================================

@app.route('/api/auth/login', methods=['POST'])
def admin_login():
    """User login endpoint - requires Supabase"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing credentials'}), 400

    if not db_service:
        return jsonify({'status': 'error', 'message': 'Database service not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env'}), 503

    try:
        # Query Supabase for user
        existing_user = db_service.db.table('app_users').select('password, role, name').eq('email', email).execute()
        if not existing_user.data or len(existing_user.data) == 0:
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        user = existing_user.data[0]
        if not verify_password(password, user['password']):
            return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401
        
        # Generate JWT tokens
        access_token = generate_jwt_token(email, user.get('role', 'user'), is_refresh=False)
        refresh_token = generate_jwt_token(email, user.get('role', 'user'), is_refresh=True)
        
        return jsonify({
            'status': 'success',
            'token': access_token,
            'refresh_token': refresh_token,
            'user': {'email': email, 'role': user.get('role', 'user'), 'name': user.get('name', '')}
        }), 200
        
    except Exception as e:
        app.logger.error(f'Login error: {str(e)}')
        return jsonify({'status': 'error', 'message': 'Login failed. Please check your database configuration.'}), 500

@app.route('/api/auth/signup', methods=['POST'])
def user_signup():
    """User signup endpoint - requires Supabase"""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    
    if not name or not email or not password:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    if not db_service or not JWT_AVAILABLE:
        return jsonify({'status': 'error', 'message': 'Database service not configured. Please set SUPABASE_URL and SUPABASE_KEY in .env'}), 503
    
    try:
        # Check if user already exists
        existing_user = db_service.db.table('app_users').select('email').eq('email', email).execute()
        if existing_user.data:
            return jsonify({'status': 'error', 'message': 'Email already registered'}), 400
        
        # Hash password
        hashed_password = hash_password(password)
        
        # Create user in Supabase
        result = db_service.db.table('app_users').insert({
            'name': name,
            'email': email,
            'password': hashed_password,
            'role': 'user',
            'created_at': datetime.now().isoformat()
        }).execute()
        
        if result.data:
            # Generate JWT token
            access_token = generate_jwt_token(email, 'user', is_refresh=False)
            refresh_token = generate_jwt_token(email, 'user', is_refresh=True)
            
            return jsonify({
                'status': 'success',
                'message': 'Account created successfully',
                'token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'name': name,
                    'email': email,
                    'role': 'user'
                }
            }), 201
        else:
            return jsonify({'status': 'error', 'message': 'Failed to create account'}), 500
            
    except Exception as e:
        app.logger.error(f'Signup error: {str(e)}')
        return jsonify({'status': 'error', 'message': f'Signup failed: {str(e)}'}), 500

@app.route('/api/auth/refresh', methods=['POST'])
def refresh_token():
    """Token refresh endpoint"""
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({'status': 'error', 'message': 'Missing refresh token'}), 400
    
    payload = verify_jwt_token(refresh_token)
    
    if not payload or payload.get('type') != 'refresh':
        return jsonify({'status': 'error', 'message': 'Invalid or expired refresh token'}), 401
    
    # Generate new access token
    new_access_token = generate_jwt_token(payload['user_id'], payload['role'], is_refresh=False)
    
    return jsonify({
        'status': 'success',
        'token': new_access_token,
    }), 200

# =====================================================
# API ENDPOINTS - ORDERS & PAYMENTS
# =====================================================

@app.route('/api/create-order', methods=['POST'])
def create_razorpay_order():
    """MEDIATOR: Create Razorpay order and store in Supabase"""
    data = request.get_json()
    required_fields = ['customer_email', 'shipping_address', 'items']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400
    
    if not razorpay_mediator or not db_service:
        return jsonify({'status': 'error', 'message': 'Payment system not configured'}), 503

    # Calculate total
    total = sum(item.get('price', 0) * item.get('quantity', 1) for item in data['items'])
    
    # Generate unique order ID
    order_id = f"BHRT-{int(datetime.now().timestamp())}-{os.urandom(4).hex()}"
    
    # Create Razorpay order (amount is in paise)
    razorpay_order = razorpay_mediator.create_order(
        amount=int(total * 100),
        currency='INR',
        receipt=order_id
    )

    if not razorpay_order:
        return jsonify({'status': 'error', 'message': 'Failed to create payment order'}), 500

    # Store order in DB with pending status
    order_data_for_db = {
        **data,
        'order_id': order_id,
        'total_amount': total,
        'status': 'pending',
        'razorpay_order_id': razorpay_order['id']
    }
    db_order = db_service.create_order_in_db(order_data_for_db)

    if not db_order:
        # NOTE: In a production scenario, you would need to cancel the Razorpay order here
        return jsonify({'status': 'error', 'message': 'Failed to record order in database'}), 500

    return jsonify({
        'status': 'success',
        'order_id': order_id,
        'razorpay_order_id': razorpay_order['id'],
        'amount': total,
        'currency': razorpay_order['currency'],
        'key_id': RAZORPAY_KEY_ID # Sent to frontend for payment
    }), 200

@app.route('/api/verify-payment', methods=['POST'])
def verify_payment_and_submit():
    """MEDIATOR: Verify Razorpay signature, record payment, and submit to Qikink"""
    data = request.get_json()
    required_fields = ['order_id', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature']
    
    if not all(field in data for field in required_fields):
        return jsonify({'status': 'error', 'message': 'Missing required verification fields'}), 400

    if not razorpay_mediator or not db_service or not qikink_mediator:
        return jsonify({'status': 'error', 'message': 'Payment/Order system not fully configured'}), 503

    # 1. Retrieve Order
    order = db_service.get_order_by_id(data['order_id'])
    if not order or order.get('razorpay_order_id') != data['razorpay_order_id']:
        return jsonify({'status': 'error', 'message': 'Order not found or ID mismatch'}), 404

    # 2. Verify Signature
    is_valid_signature = razorpay_mediator.verify_payment_signature(
        data['razorpay_order_id'],
        data['razorpay_payment_id'],
        data['razorpay_signature']
    )

    if not is_valid_signature:
        return jsonify({'status': 'error', 'message': 'Payment signature verification failed'}), 400

    # 3. Record Payment & Update Order Status
    payment_record = db_service.create_payment_record({
        'razorpay_payment_id': data['razorpay_payment_id'],
        'razorpay_order_id': data['razorpay_order_id'],
        'amount': order['total_amount'],
        'status': 'verified',
        'payment_method': 'online',
        'idempotency_key': f"{data['razorpay_payment_id']}_verified"
    })
    
    # Update order status
    db_service.update_order_status(order['order_id'], 'payment_verified')

    # 4. Submit to Qikink
    qikink_result = qikink_mediator.submit_order_to_qikink(order['order_id'])
    
    app.logger.info(f'Payment verified for order {order["order_id"]}, Qikink status: {qikink_result["status"]}')

    return jsonify({
        'status': 'success',
        'payment_verified': True,
        'order_id': order['order_id'],
        'qikink_submitted': qikink_result['status'] == 'success',
        'qikink_order_id': qikink_result.get('qikink_order_id')
    }), 200

@app.route('/api/webhooks/razorpay', methods=['POST'])
def razorpay_webhook_handler():
    """MEDIATOR: Handle Razorpay webhooks with idempotency"""
    signature = request.headers.get('X-Razorpay-Signature')
    payload = request.get_data(as_text=True) # Get raw payload string for verification

    if not razorpay_mediator or not signature:
        return jsonify({'status': 'error'}), 503

    # Process webhook
    result = razorpay_mediator.process_webhook(json.loads(payload), signature)

    if result['status'] in ['success', 'duplicate']:
        app.logger.info(f'Webhook processed: {result}')
        return jsonify({'status': 'ok'}), 200
    else:
        app.logger.error(f'Webhook processing failed: {result}')
        return jsonify({'status': 'error'}), 400

@app.route('/api/order-status/<order_id>', methods=['GET'])
def get_order_status_endpoint(order_id):
    """Get order status and tracking information"""
    if not db_service:
        return jsonify({'status': 'error', 'message': 'Database not configured'}), 503
    
    order = db_service.get_order_by_id(order_id)
    
    if not order:
        return jsonify({'status': 'error', 'message': 'Order not found'}), 404
    
    return jsonify({
        'status': 'success',
        'order': order
    }), 200

# =====================================================
# API ENDPOINTS - ADMIN
# =====================================================

@app.route('/api/admin/sync-products', methods=['POST'])
@require_admin
def admin_sync_products_endpoint():
    """Admin: Sync products from Qikink to Supabase"""
    if not qikink_mediator:
        return jsonify({'status': 'error', 'message': 'Qikink service not configured'}), 503
    
    result = qikink_mediator.sync_products()
    app.logger.info(f'Admin product sync: {result}')
    
    return jsonify(result), 200 if result['status'] == 'success' else 500

@app.route('/api/admin/dashboard', methods=['GET'])
@require_admin
def admin_dashboard_endpoint():
    """Admin: Get dashboard statistics"""
    if not db_service:
        return jsonify({'status': 'error', 'message': 'Database not configured'}), 503
    
    stats = db_service.get_dashboard_stats()
    return jsonify(stats), 200

@app.route('/api/admin/orders', methods=['GET'])
@require_admin
def admin_get_orders_endpoint():
    """Admin: Get all orders with filters"""
    if not db_service:
        return jsonify({'status': 'error', 'message': 'Database not configured'}), 503
    
    status_filter = request.args.get('status')
    orders = db_service.get_all_orders(status_filter=status_filter)
    
    return jsonify({'status': 'success', 'orders': orders}), 200

@app.route('/api/admin/retry-order/<order_id>', methods=['POST'])
@require_admin
def admin_retry_order_endpoint(order_id):
    """Admin: Manually retry failed Qikink submission"""
    if not qikink_mediator:
        return jsonify({'status': 'error', 'message': 'Qikink service not configured'}), 503
    
    result = qikink_mediator.submit_order_to_qikink(order_id)
    app.logger.info(f'Admin retry order {order_id}: {result}')
    
    return jsonify(result), 200 if result['status'] == 'success' else 500

@app.route('/api/admin/test-connectivity', methods=['GET'])
@require_admin
def admin_test_connectivity_endpoint():
    """Admin: Test Qikink and Razorpay connectivity"""
    qikink_status = qikink_mediator.test_connection() if qikink_mediator else {'status': 'not_configured'}
    razorpay_status = {'status': 'connected'} if razorpay_client else {'status': 'not_configured'}
    supabase_status = {'status': 'connected' if supabase_client else 'not_configured'}
    
    return jsonify({
        'qikink': qikink_status,
        'razorpay': razorpay_status,
        'supabase': supabase_status
    }), 200

# =====================================================
# ERROR HANDLERS
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler"""
    app.logger.error(f'Unhandled exception: {str(e)}', exc_info=True)
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

# =====================================================
# MAIN
# =====================================================

if __name__ == '__main__':
    print('\n' + '='*60)
    print('THE BHARAT COLLECTIONS - BACKEND MEDIATOR')
    print('='*60)
    print(f'Supabase: {"[OK] Connected" if supabase_client else "[X] Not configured"}')
    print(f'Razorpay: {"[OK] Connected" if razorpay_client else "[X] Not configured"}')
    print(f'Qikink: {"[OK] Connected" if qikink_mediator else "[X] Not configured"}')
    print(f'JWT Auth: {"[OK] Enabled" if JWT_AVAILABLE else "[X] Disabled"}')
    print(f'Scheduler: {"[OK] Running" if scheduler else "[X] Disabled"}')
    print('='*60 + '\n')
    
    # Production deployment might use a WSGI server (like Gunicorn), 
    # but for local dev/testing:
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) # use_reloader=False stops double scheduler start