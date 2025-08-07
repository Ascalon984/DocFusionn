#!/usr/bin/env python3
"""
DocMaster Admin Backend
Backend service untuk monitoring dan analytics admin panel
"""

import json
import sqlite3
import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Admin configuration
ADMIN_EMAIL = 'adityatriprasetyo5@gmail.com'
DATABASE_PATH = 'docmaster_admin.db'

class AdminDatabase:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT,
                status TEXT DEFAULT 'active',
                subscription_type TEXT DEFAULT 'free',
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_sessions INTEGER DEFAULT 0,
                total_documents_processed INTEGER DEFAULT 0
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id TEXT UNIQUE NOT NULL,
                user_email TEXT NOT NULL,
                user_name TEXT,
                amount DECIMAL(10,2) NOT NULL,
                plan_type TEXT,
                plan_duration TEXT,
                status TEXT DEFAULT 'pending',
                payment_method TEXT,
                transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (email)
            )
        ''')
        
        # Usage analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT,
                feature_name TEXT NOT NULL,
                action_type TEXT NOT NULL,
                session_duration INTEGER,
                document_size INTEGER,
                success BOOLEAN DEFAULT 1,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT
            )
        ''')
        
        # System metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_unit TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Revenue tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS revenue_tracking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                daily_revenue DECIMAL(10,2) DEFAULT 0,
                total_transactions INTEGER DEFAULT 0,
                new_subscriptions INTEGER DEFAULT 0,
                cancellations INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Insert sample data if tables are empty
        self.insert_sample_data()
        logger.info("Database initialized successfully")
    
    def insert_sample_data(self):
        """Insert sample data for demo purposes"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if users table is empty
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            sample_users = [
                (ADMIN_EMAIL, 'Aditya Tri Prasetyo', 'active', 'premium', '2024-12-01', datetime.datetime.now(), 45, 127),
                ('john.doe@example.com', 'John Doe', 'active', 'premium', '2024-12-15', datetime.datetime.now(), 23, 67),
                ('jane.smith@example.com', 'Jane Smith', 'active', 'basic', '2024-12-20', datetime.datetime.now(), 15, 34),
                ('bob.wilson@example.com', 'Bob Wilson', 'inactive', 'free', '2024-11-30', datetime.datetime.now(), 8, 12),
                ('alice.johnson@example.com', 'Alice Johnson', 'active', 'premium', '2024-12-10', datetime.datetime.now(), 31, 89)
            ]
            
            cursor.executemany('''
                INSERT INTO users (email, name, status, subscription_type, join_date, last_active, total_sessions, total_documents_processed)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_users)
            
            # Sample transactions
            sample_transactions = [
                ('TXN001', ADMIN_EMAIL, 'Aditya Tri Prasetyo', 199000.00, 'premium', '12 bulan', 'completed', 'credit_card', '2024-12-01'),
                ('TXN002', 'john.doe@example.com', 'John Doe', 89000.00, 'premium', '3 bulan', 'completed', 'bank_transfer', '2024-12-15'),
                ('TXN003', 'jane.smith@example.com', 'Jane Smith', 49000.00, 'basic', '1 bulan', 'completed', 'e_wallet', '2024-12-20'),
                ('TXN004', 'alice.johnson@example.com', 'Alice Johnson', 199000.00, 'premium', '12 bulan', 'pending', 'credit_card', '2024-12-10')
            ]
            
            cursor.executemany('''
                INSERT INTO transactions (transaction_id, user_email, user_name, amount, plan_type, plan_duration, status, payment_method, transaction_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', sample_transactions)
            
            conn.commit()
            logger.info("Sample data inserted successfully")
        
        conn.close()
    
    def get_user_metrics(self):
        """Get user-related metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Active users (logged in within last 30 days)
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE last_active > datetime('now', '-30 days')
        """)
        active_users = cursor.fetchone()[0]
        
        # Premium users
        cursor.execute("SELECT COUNT(*) FROM users WHERE subscription_type = 'premium'")
        premium_users = cursor.fetchone()[0]
        
        # New users this month
        cursor.execute("""
            SELECT COUNT(*) FROM users 
            WHERE date(join_date) >= date('now', 'start of month')
        """)
        new_users_month = cursor.fetchone()[0]
        
        # Average session duration (mock data for now)
        avg_session_duration = 24.5
        
        conn.close()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'premium_users': premium_users,
            'new_users_month': new_users_month,
            'avg_session_duration': avg_session_duration
        }
    
    def get_transaction_metrics(self):
        """Get transaction-related metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total transactions
        cursor.execute("SELECT COUNT(*) FROM transactions")
        total_transactions = cursor.fetchone()[0]
        
        # Completed transactions
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'completed'")
        completed_transactions = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute("SELECT SUM(amount) FROM transactions WHERE status = 'completed'")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Revenue this month
        cursor.execute("""
            SELECT SUM(amount) FROM transactions 
            WHERE status = 'completed' AND date(transaction_date) >= date('now', 'start of month')
        """)
        revenue_month = cursor.fetchone()[0] or 0
        
        # Pending transactions
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE status = 'pending'")
        pending_transactions = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_transactions': total_transactions,
            'completed_transactions': completed_transactions,
            'total_revenue': total_revenue,
            'revenue_month': revenue_month,
            'pending_transactions': pending_transactions
        }
    
    def get_recent_users(self, limit=10):
        """Get recent users"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT email, name, status, subscription_type, join_date, last_active, total_sessions, total_documents_processed
            FROM users 
            ORDER BY join_date DESC 
            LIMIT ?
        """, (limit,))
        
        users = []
        for row in cursor.fetchall():
            users.append({
                'email': row[0],
                'name': row[1],
                'status': row[2],
                'subscription_type': row[3],
                'join_date': row[4],
                'last_active': row[5],
                'total_sessions': row[6],
                'total_documents_processed': row[7]
            })
        
        conn.close()
        return users
    
    def get_recent_transactions(self, limit=10):
        """Get recent transactions"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT transaction_id, user_email, user_name, amount, plan_type, plan_duration, status, payment_method, transaction_date
            FROM transactions 
            ORDER BY transaction_date DESC 
            LIMIT ?
        """, (limit,))
        
        transactions = []
        for row in cursor.fetchall():
            transactions.append({
                'transaction_id': row[0],
                'user_email': row[1],
                'user_name': row[2],
                'amount': row[3],
                'plan_type': row[4],
                'plan_duration': row[5],
                'status': row[6],
                'payment_method': row[7],
                'transaction_date': row[8]
            })
        
        conn.close()
        return transactions
    
    def track_user_activity(self, email, feature, action_type, session_duration=None, document_size=None, success=True, ip_address=None, user_agent=None):
        """Track user activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO usage_analytics (user_email, feature_name, action_type, session_duration, document_size, success, ip_address, user_agent)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (email, feature, action_type, session_duration, document_size, success, ip_address, user_agent))
        
        # Update user's last active time
        cursor.execute("""
            UPDATE users 
            SET last_active = CURRENT_TIMESTAMP,
                total_sessions = total_sessions + 1
            WHERE email = ?
        """, (email,))
        
        conn.commit()
        conn.close()
    
    def add_transaction(self, transaction_data):
        """Add new transaction"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO transactions (transaction_id, user_email, user_name, amount, plan_type, plan_duration, status, payment_method)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction_data['transaction_id'],
            transaction_data['user_email'],
            transaction_data['user_name'],
            transaction_data['amount'],
            transaction_data['plan_type'],
            transaction_data['plan_duration'],
            transaction_data.get('status', 'pending'),
            transaction_data.get('payment_method', 'unknown')
        ))
        
        conn.commit()
        conn.close()

# Initialize database
admin_db = AdminDatabase()

# API Routes
@app.route('/api/admin/check-access', methods=['POST'])
def check_admin_access():
    """Check if user has admin access"""
    data = request.get_json()
    user_email = data.get('email', '')
    
    is_admin = user_email == ADMIN_EMAIL
    
    return jsonify({
        'is_admin': is_admin,
        'email': user_email
    })

@app.route('/api/admin/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get dashboard metrics and data"""
    try:
        user_metrics = admin_db.get_user_metrics()
        transaction_metrics = admin_db.get_transaction_metrics()
        recent_users = admin_db.get_recent_users()
        recent_transactions = admin_db.get_recent_transactions()
        
        return jsonify({
            'success': True,
            'data': {
                'metrics': {
                    'users': user_metrics,
                    'transactions': transaction_metrics
                },
                'recent_users': recent_users,
                'recent_transactions': recent_transactions,
                'last_updated': datetime.datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"Error getting dashboard data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/track-activity', methods=['POST'])
def track_activity():
    """Track user activity"""
    try:
        data = request.get_json()
        admin_db.track_user_activity(
            email=data.get('email'),
            feature=data.get('feature'),
            action_type=data.get('action_type'),
            session_duration=data.get('session_duration'),
            document_size=data.get('document_size'),
            success=data.get('success', True),
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error tracking activity: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/add-transaction', methods=['POST'])
def add_transaction():
    """Add new transaction"""
    try:
        data = request.get_json()
        admin_db.add_transaction(data)
        
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error adding transaction: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/export-data', methods=['GET'])
def export_data():
    """Export all admin data"""
    try:
        # Get all data
        user_metrics = admin_db.get_user_metrics()
        transaction_metrics = admin_db.get_transaction_metrics()
        all_users = admin_db.get_recent_users(limit=1000)  # Get all users
        all_transactions = admin_db.get_recent_transactions(limit=1000)  # Get all transactions
        
        export_data = {
            'export_info': {
                'timestamp': datetime.datetime.now().isoformat(),
                'version': '1.0',
                'admin_email': ADMIN_EMAIL
            },
            'metrics': {
                'users': user_metrics,
                'transactions': transaction_metrics
            },
            'users': all_users,
            'transactions': all_transactions
        }
        
        return jsonify({
            'success': True,
            'data': export_data
        })
    except Exception as e:
        logger.error(f"Error exporting data: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/')
def serve_main():
    """Serve main DocMaster application"""
    return send_from_directory('.', 'DocMaster.html')

@app.route('/admin')
def serve_admin():
    """Serve admin interface"""
    return send_from_directory('.', 'DocMaster.html')

if __name__ == '__main__':
    # Create database if it doesn't exist
    if not os.path.exists(DATABASE_PATH):
        admin_db.init_database()
        logger.info("Database created and initialized")
    
    # Run the server
    print(f"""
    
DocMaster Admin Backend Server
=============================
Admin Email: {ADMIN_EMAIL}
Database: {DATABASE_PATH}

Access URLs:
- Main App: http://localhost:5001/
- Admin Panel: http://localhost:5001/admin
- API Docs: http://localhost:5001/api/admin/dashboard

Server starting...
    """)
    
    app.run(host='127.0.0.1', port=5001, debug=True)
