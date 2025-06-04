from flask import Flask, request, jsonify, abort, g, redirect, url_for
from flask_cors import CORS
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from werkzeug.security import generate_password_hash, check_password_hash
import json
import secrets
import requests
from datetime import datetime, timezone, timedelta
from mailjet_rest import Client as MailjetClient

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Initialize Supabase client
try:
    supabase_url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_KEY")
    anon_key = os.getenv("ADMIN_KEY")  # This is actually the anon key
    
    print(f"Initializing Supabase with URL: {supabase_url}")
    print(f"Service key available: {'Yes' if service_key else 'No'}")
    print(f"Anon key available: {'Yes' if anon_key else 'No'}")
    
    # Initialize both clients - one with service role for DB operations
    # and one with anon role for auth operations
    supabase = create_client(supabase_url, service_key)
    supabase_auth = create_client(supabase_url, anon_key)
    
    # Store SMTP settings for reference
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_sender = os.getenv("SMTP_SENDER")
    site_url = os.getenv("SITE_URL")
    
    if smtp_host and smtp_port and smtp_user and smtp_pass and smtp_sender:
        print("SMTP configuration found for email confirmation")
        print(f"SMTP Sender Email: {smtp_sender}")
    else:
        print("Warning: SMTP configuration incomplete. Email confirmation may not work.")
    
    print("Supabase clients initialized successfully")
except Exception as e:
    print(f"Error initializing Supabase client: {str(e)}")
    supabase = None
    supabase_auth = None

# Helper functions
def format_response(data, error=None):
    if error:
        return jsonify({"success": False, "message": error}), 400
    return jsonify({"success": True, "data": data}), 200

# Email sending function using Mailjet
def send_verification_email(email, name, verification_url):
    try:
        # Get Mailjet credentials
        api_key = os.getenv('SMTP_USER')
        api_secret = os.getenv('SMTP_PASS')
        sender_email = os.getenv('SMTP_SENDER')
        
        if not api_key or not api_secret or not sender_email:
            print("Missing Mailjet credentials. Email not sent.")
            return False
        
        print(f"Sending verification email to {email} from {sender_email}")
        
        try:
            # Initialize Mailjet client
            mailjet = MailjetClient(auth=(api_key, api_secret))
            
            # Prepare email data with enhanced design
            data = {
                'Messages': [
                    {
                        'From': {
                            'Email': sender_email,
                            'Name': 'Pawfect Pet Adoption'
                        },
                        'To': [
                            {
                                'Email': email,
                                'Name': name
                            }
                        ],
                        'Subject': 'Welcome to Pawfect! Verify Your Email',
                        'TextPart': f"Welcome to Pawfect! Please verify your email by clicking this link: {verification_url}",
                        'HTMLPart': f'''
                        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <div style="background-color: #FF6B6B; padding: 20px; text-align: center;">
                                <img src="https://i.imgur.com/Designer.png" alt="Pawfect Logo" style="max-width: 150px; height: auto;">
                            </div>
                            <div style="padding: 30px;">
                                <h2 style="color: #333333; margin-bottom: 20px; text-align: center;">Welcome to Pawfect!</h2>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6;">Hi {name},</p>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6;">Thank you for joining our community of pet lovers! We're excited to help you find your perfect furry companion.</p>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6;">To get started, please verify your email address by clicking the button below:</p>
                                <div style="text-align: center; margin: 30px 0;">
                                    <a href="{verification_url}" style="background-color: #FF6B6B; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Verify Email Address</a>
                                </div>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">If the button above doesn't work, copy and paste this URL into your browser:</p>
                                <p style="color: #666666; font-size: 14px; word-break: break-all; background-color: #f5f5f5; padding: 10px; border-radius: 5px;">{verification_url}</p>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">This verification link will expire in 3 days.</p>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">If you didn't create an account with Pawfect, you can safely ignore this email.</p>
                            </div>
                            <div style="background-color: #f8f8f8; padding: 20px; text-align: center; border-top: 1px solid #eeeeee;">
                                <p style="color: #999999; font-size: 12px; margin: 0;">© 2024 Pawfect Pet Adoption. All rights reserved.</p>
                                <p style="color: #999999; font-size: 12px; margin: 5px 0 0 0;">Making pet adoption easier and more joyful.</p>
                            </div>
                        </div>
                        '''
                    }
                ]
            }
            
            # Send the email
            result = mailjet.send.create(data=data)
            print(f"Mailjet API response: {result.status_code}")
            
            if result.status_code != 200:
                try:
                    error_info = result.json()
                    print(f"Detailed error: {error_info}")
                except Exception as json_err:
                    print(f"Could not parse error response: {str(json_err)}")
                    try:
                        print(f"Raw response: {result.text}")
                    except:
                        pass
                        
                # If Mailjet client fails, try direct HTTP request as fallback
                print("Trying fallback direct HTTP request...")
                mailjet_api_url = "https://api.mailjet.com/v3.1/send"
                headers = {"Content-Type": "application/json"}
                auth = (api_key, api_secret)
                
                response = requests.post(mailjet_api_url, auth=auth, json=data, headers=headers)
                print(f"Fallback HTTP response: {response.status_code}")
                
                if response.status_code == 200:
                    print("Fallback email sending succeeded!")
                    return True
                else:
                    try:
                        error_details = response.json()
                        print(f"Fallback error details: {error_details}")
                    except:
                        print(f"Raw fallback response: {response.text}")
            
            return result.status_code == 200
            
        except Exception as api_error:
            print(f"Mailjet API error: {str(api_error)}")
            return False
        
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return False

# Root route for basic testing
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "message": "Welcome to the Pawffect API",
        "status": "running",
        "available_endpoints": [
            "/api/login",
            "/api/register",
            "/api/signup",
            "/api/create-admin",
            "/api/pet",
            "/api/user",
            "/api/application",
            "/api/appointment",
            "/api/upload"
        ]
    })

# Authentication Routes

@app.route('/api/signup', methods=['POST'])
def register():
    try:
        # Debug logs
        print("Register endpoint called")
        
        # Check if Supabase client is initialized
        if not supabase_auth:
            print("Supabase auth client is not initialized")
            return jsonify({"success": False, "message": "Authentication service unavailable"}), 500
            
        data = request.json
        print(f"Received data: {data}")
        
        # Get user input
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'user')  # Default to 'user' if not specified
        
        print(f"Set role to: {role}")
        
        # Validate required fields
        if not all([name, email, password]):
            return jsonify({"success": False, "message": "Name, email and password are required"}), 400
        
        try:
            # First, check if user already exists in our users table
            print(f"Checking if user already exists: {email}")
            existing_user = supabase.table('users').select('*').eq('email', email).execute()
            if existing_user.data and len(existing_user.data) > 0:
                return jsonify({"success": False, "message": "Email already registered"}), 400
            
            # Generate verification token with expiry
            verification_token = secrets.token_urlsafe(32)
            verification_expiry = datetime.now(timezone.utc) + timedelta(days=3)
            
            # Hash password for our custom users table
            hashed_password = generate_password_hash(password)
                
            # Create user with verification token
            print(f"Creating user with verification token: {email}")
            user_data = {
                "name": name,
                "email": email,
                "password": hashed_password,
                "role": role,
                "is_verified": False,  # Initially not verified
                "verification_token": verification_token,
                "verification_expiry": verification_expiry.isoformat()
            }
            
            # Insert into our users table
            user_result = supabase.table('users').insert(user_data).execute()
            
            if not user_result.data or len(user_result.data) == 0:
                return jsonify({"success": False, "message": "Failed to create user"}), 500
                
            user = user_result.data[0]
            
            # Send verification email
            verification_url = f"{os.getenv('SITE_URL')}/confirm-email?token={verification_token}&type=signup"
            print(f"Sending verification email to {email} with URL: {verification_url}")
            
            # Call the send_verification_email function
            email_sent = send_verification_email(email, name, verification_url)
            
            if email_sent:
                print(f"Verification email sent successfully to {email}")
            else:
                print(f"Failed to send verification email to {email}, but user was created")
            
            # Return success response without token since email verification is required
            return jsonify({
                "success": True, 
                "message": "Registration successful. Please check your email to verify your account.",
                "email_verification_required": True,
                "verification_url": verification_url if not email_sent else None  # Only return URL if email failed (for testing)
            }), 200
            
        except Exception as auth_error:
            print(f"Auth error: {str(auth_error)}")
            return jsonify({"success": False, "message": f"Auth error: {str(auth_error)}"}), 500
    
    except Exception as e:
        print(f"Registration exception: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
        
# Email confirmation callback endpoint
@app.route('/api/auth/confirm', methods=['GET'])
def confirm_email():
    try:
        # Get token from query parameters
        token = request.args.get('token')
        type_param = request.args.get('type')
        
        if not token:
            return jsonify({"success": False, "message": "Confirmation token is missing"}), 400
            
        # Redirect to frontend with token for it to complete the confirmation
        redirect_url = f"{os.getenv('SITE_URL')}/confirm-email?token={token}&type={type_param}"
        return redirect(redirect_url)
        
    except Exception as e:
        print(f"Email confirmation error: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400

# Registration and login functions use the standard approach

# Admin Creation Route (protected with admin key)
@app.route('/api/create-admin', methods=['POST'])
def create_admin():
    try:
        data = request.json
        admin_key = request.headers.get('Admin-Key')
        
        # Check for admin key - this should match what you set in your .env file
        if not admin_key or admin_key != os.getenv('ADMIN_KEY', 'your-secret-admin-key'):
            return jsonify({"success": False, "message": "Unauthorized"}), 401
            
        required_fields = ['name', 'email', 'password']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return format_response(None, f"Missing required field: {field}")
                
        # Set role to 'admin'
        data['role'] = 'admin'
        
        # Hash the password
        hashed_password = generate_password_hash(data['password'])
        
        # Insert admin into Supabase
        user_data = {
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password,
            'role': data['role'],
            'phone': data.get('phone', None),
            'address': data.get('address', None),
            'profile_image': data.get('profile_image', None)
        }
        
        result = supabase.table('users').insert(user_data).execute()
        
        # Check if insert was successful
        if len(result.data) > 0:
            # Don't return the password in the response
            user = result.data[0]
            user.pop('password', None)
            
            return jsonify({
                "success": True,
                "message": "Admin created successfully",
                "user": user
            })
        else:
            return jsonify({"success": False, "message": "Failed to create admin"}), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    try:
        # Check if Supabase client is initialized
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        data = request.json
        print(f"Login attempt for email: {data.get('email')}")
        
        if 'email' not in data or 'password' not in data:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        email = data['email']
        password = data['password']
        
        try:
            # Query for the user with the given email
            print(f"Looking up user: {email}")
            result = supabase.table('users').select('*').eq('email', email).execute()
            
            if not result.data or len(result.data) == 0:
                print(f"User not found: {email}")
                return jsonify({"success": False, "message": "Invalid email or password"}), 401
            
            user = result.data[0]
            
            # Verify password
            print("Verifying password")
            if not check_password_hash(user['password'], password):
                print("Password verification failed")
                return jsonify({"success": False, "message": "Invalid email or password"}), 401
                
            # Check if email is verified
            if not user.get('is_verified', False):
                print(f"Email not verified for user: {email}")
                
                # If verification token exists and is not expired, return message
                verification_token = user.get('verification_token')
                verification_expiry = user.get('verification_expiry')
                
                # Generate a new verification token if needed
                if not verification_token or not verification_expiry:
                    verification_token = secrets.token_urlsafe(32)
                    verification_expiry = datetime.now(timezone.utc) + timedelta(days=3)
                    
                    # Update user with new token
                    supabase.table('users').update({
                        'verification_token': verification_token,
                        'verification_expiry': verification_expiry.isoformat()
                    }).eq('id', user['id']).execute()
                
                # Send verification email again
                verification_url = f"{os.getenv('SITE_URL')}/confirm-email?token={verification_token}&type=signup"
                send_verification_email(email, user['name'], verification_url)
                
                return jsonify({
                    "success": False, 
                    "message": "Please verify your email before logging in.",
                    "email_verification_required": True,
                    "verification_url": verification_url  # Include for testing purposes
                }), 401
            
            # Generate token for the user
            token = secrets.token_hex(16)
            
            # Remove sensitive data from response
            user_data = {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
                "profile_image": user.get("profile_image"),
                "phone": user.get("phone"),
                "address": user.get("address")
            }
            
            print(f"Login successful for: {email}")
            
            return jsonify({
                "success": True,
                "message": "Login successful",
                "token": token,
                "user": user_data
            })
        
        except Exception as auth_error:
            print(f"Login error: {str(auth_error)}")
            return jsonify({"success": False, "message": str(auth_error)}), 500
            
    except Exception as e:
        print(f"Login exception: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400
        
# Redirect endpoint for email verification links
@app.route('/confirm-email', methods=['GET'])
def redirect_verification():
    # Get the token from query parameters
    token = request.args.get('token')
    type_param = request.args.get('type', 'signup')
    
    if not token:
        return jsonify({"success": False, "message": "Verification token is required"}), 400
        
    # Redirect to the frontend confirm-email page with the token
    frontend_url = os.getenv('SITE_URL')
    redirect_url = f"{frontend_url}/#/confirm-email?token={token}&type={type_param}"
    print(f"Redirecting to: {redirect_url}")
    return redirect(redirect_url)

# Email verification endpoint for our custom system
@app.route('/api/verify-email', methods=['POST', 'GET'])
def verify_email():
    try:
        # Handle both GET and POST requests
        if request.method == 'GET':
            token = request.args.get('token')
        else:  # POST
            data = request.json
            token = data.get('token') if data else None
        
        if not token:
            return jsonify({"success": False, "message": "Verification token is required"}), 400
        
        try:
            # Find user with this verification token
            print(f"Verifying email with token: {token}")
            current_time = datetime.now(timezone.utc).isoformat()
            
            # Query user with this token and check if it's not expired
            result = supabase.table('users')\
                .select('*')\
                .eq('verification_token', token)\
                .execute()
                
            if not result.data or len(result.data) == 0:
                print("Invalid verification token")
                return jsonify({"success": False, "message": "Invalid verification token"}), 400
                
            user = result.data[0]
            
            # Check if token has expired
            expiry = datetime.fromisoformat(user['verification_expiry'])
            now = datetime.now(timezone.utc)
            
            if now > expiry:
                print("Verification token has expired")
                return jsonify({"success": False, "message": "Verification token has expired"}), 400
                
            # Update user verification status
            print(f"Verifying user: {user['email']}")
            update_result = supabase.table('users')\
                .update({
                    'is_verified': True,
                    'verification_token': None,  # Clear the token once used
                    'verification_expiry': None
                })\
                .eq('id', user['id'])\
                .execute()
            
            return jsonify({
                "success": True,
                "message": "Email verified successfully"
            })
                
        except Exception as verify_error:
            print(f"Email verification error: {str(verify_error)}")
            return jsonify({"success": False, "message": f"Verification error: {str(verify_error)}"}), 500
    
    except Exception as e:
        print(f"Verification exception: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 400

# Password Reset Routes
@app.route('/api/check-email', methods=['POST'])
def check_email():
    try:
        data = request.json
        email = data.get('email')
        
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400
            
        # Check if the email exists in the database
        result = supabase.table('users').select('id, name, email').eq('email', email).execute()
        
        if not result.data or len(result.data) == 0:
            return jsonify({"success": False, "message": "Email not found"}), 404
            
        # Generate reset token and expiry
        reset_token = secrets.token_urlsafe(32)
        reset_token_expiry = datetime.now(timezone.utc) + timedelta(hours=24)
        
        # Update user with reset token
        user_id = result.data[0]['id']
        name = result.data[0]['name']
        
        supabase.table('users').update({
            'reset_token': reset_token,
            'reset_token_expiry': reset_token_expiry.isoformat()
        }).eq('id', user_id).execute()
        
        # Send password reset email
        reset_url = f"{os.getenv('SITE_URL')}/reset-password?token={reset_token}"
        print(f"Reset URL: {reset_url}")
        
        email_sent = send_password_reset_email(email, name, reset_url)
        
        if email_sent:
            print(f"Password reset email sent to {email}")
            return jsonify({
                "success": True,
                "message": "Password reset email sent"
            }), 200
        else:
            print(f"Failed to send password reset email to {email}")
            return jsonify({
                "success": False, 
                "message": "Failed to send password reset email",
                "reset_url": reset_url  # Only for development/testing
            }), 500
            
    except Exception as e:
        print(f"Error in check_email: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/verify-reset-token', methods=['POST'])
def verify_reset_token():
    try:
        data = request.json
        token = data.get('token')
        
        if not token:
            return jsonify({"success": False, "message": "Token is required"}), 400
            
        # Find user with this reset token
        result = supabase.table('users').select('*').eq('reset_token', token).execute()
        
        if not result.data or len(result.data) == 0:
            return jsonify({"success": False, "message": "Invalid token"}), 400
            
        user = result.data[0]
        
        # Check if token is expired
        if user.get('reset_token_expiry'):
            expiry = datetime.fromisoformat(user['reset_token_expiry'].replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            if now > expiry:
                return jsonify({"success": False, "message": "Token expired"}), 400
                
        return jsonify({
            "success": True,
            "message": "Token valid"
        })
            
    except Exception as e:
        print(f"Error in verify_reset_token: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        token = data.get('token')
        password = data.get('password')
        
        if not token or not password:
            return jsonify({"success": False, "message": "Token and password are required"}), 400
            
        # Find user with this reset token
        result = supabase.table('users').select('*').eq('reset_token', token).execute()
        
        if not result.data or len(result.data) == 0:
            return jsonify({"success": False, "message": "Invalid token"}), 400
            
        user = result.data[0]
        user_id = user['id']
        
        # Check if token is expired
        if user.get('reset_token_expiry'):
            expiry = datetime.fromisoformat(user['reset_token_expiry'].replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            if now > expiry:
                return jsonify({"success": False, "message": "Token expired"}), 400
        
        # Hash the new password
        hashed_password = generate_password_hash(password)
        
        # Update user password and clear reset token
        supabase.table('users').update({
            'password': hashed_password,
            'reset_token': None,
            'reset_token_expiry': None,
            'updated_at': datetime.now(timezone.utc).isoformat()
        }).eq('id', user_id).execute()
        
        return jsonify({
            "success": True,
            "message": "Password reset successfully"
        })
            
    except Exception as e:
        print(f"Error in reset_password: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

# Email sending function for password reset
def send_password_reset_email(email, name, reset_url):
    try:
        # Get Mailjet credentials
        api_key = os.getenv('SMTP_USER')
        api_secret = os.getenv('SMTP_PASS')
        sender_email = os.getenv('SMTP_SENDER')
        
        if not api_key or not api_secret or not sender_email:
            print("Missing Mailjet credentials. Email not sent.")
            return False
        
        print(f"Sending password reset email to {email} from {sender_email}")
        
        try:
            # Initialize Mailjet client
            mailjet = MailjetClient(auth=(api_key, api_secret))
            
            # Prepare email data with enhanced design
            data = {
                'Messages': [
                    {
                        'From': {
                            'Email': sender_email,
                            'Name': 'Pawfect Pet Adoption'
                        },
                        'To': [
                            {
                                'Email': email,
                                'Name': name
                            }
                        ],
                        'Subject': 'Reset Your Pawfect Password',
                        'TextPart': f"Hello {name},\n\nWe received a request to reset your password. Click this link to reset your password: {reset_url}\n\nThis link will expire in 24 hours.\n\nIf you did not request a password reset, you can ignore this email.\n\nRegards,\nThe Pawfect Team",
                        'HTMLPart': f'''
                        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                            <div style="background-color: #FF6B6B; padding: 20px; text-align: center;">
                                <img src="https://i.imgur.com/Designer.png" alt="Pawfect Logo" style="max-width: 150px; height: auto;">
                            </div>
                            <div style="padding: 30px;">
                                <h2 style="color: #333333; margin-bottom: 20px; text-align: center;">Password Reset Request</h2>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6;">Hi {name},</p>
                                <p style="color: #666666; font-size: 16px; line-height: 1.6;">We received a request to reset your password for your Pawfect account. To proceed with the password reset, please click the button below:</p>
                                <div style="text-align: center; margin: 30px 0;">
                                    <a href="{reset_url}" style="background-color: #FF6B6B; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; font-weight: bold; display: inline-block;">Reset Password</a>
                                </div>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">If the button above doesn't work, copy and paste this URL into your browser:</p>
                                <p style="color: #666666; font-size: 14px; word-break: break-all; background-color: #f5f5f5; padding: 10px; border-radius: 5px;">{reset_url}</p>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">This password reset link will expire in 24 hours for security reasons.</p>
                                <p style="color: #666666; font-size: 14px; line-height: 1.6;">If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                            </div>
                            <div style="background-color: #f8f8f8; padding: 20px; text-align: center; border-top: 1px solid #eeeeee;">
                                <p style="color: #999999; font-size: 12px; margin: 0;">© 2024 Pawfect Pet Adoption. All rights reserved.</p>
                                <p style="color: #999999; font-size: 12px; margin: 5px 0 0 0;">Making pet adoption easier and more joyful.</p>
                            </div>
                        </div>
                        '''
                    }
                ]
            }
            
            # Send the email
            result = mailjet.send.create(data=data)
            print(f"Mailjet API response: {result.status_code}")
            
            if result.status_code != 200:
                try:
                    error_info = result.json()
                    print(f"Detailed error: {error_info}")
                except Exception as json_err:
                    print(f"Could not parse error response: {str(json_err)}")
                    
                # Try direct HTTP request as fallback
                print("Trying fallback direct HTTP request...")
                mailjet_api_url = "https://api.mailjet.com/v3.1/send"
                headers = {"Content-Type": "application/json"}
                auth = (api_key, api_secret)
                
                response = requests.post(mailjet_api_url, auth=auth, json=data, headers=headers)
                print(f"Fallback HTTP response: {response.status_code}")
                
                if response.status_code == 200:
                    print("Fallback email sending succeeded!")
                    return True
                else:
                    try:
                        error_details = response.json()
                        print(f"Fallback error details: {error_details}")
                    except:
                        print(f"Raw fallback response: {response.text}")
                        
                    # Fallback to SMTP method if HTTP request fails
                    return send_password_reset_email_smtp(email, name, reset_url)
            
            return result.status_code == 200
            
        except Exception as api_error:
            print(f"Mailjet API error: {str(api_error)}")
            
            # Fallback to SMTP method
            return send_password_reset_email_smtp(email, name, reset_url)
        
    except Exception as e:
        print(f"Error sending password reset email: {str(e)}")
        return False

def send_password_reset_email_smtp(email, name, reset_url):
    """Fallback method to send password reset email via SMTP"""
    try:
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Get SMTP settings
        smtp_host = os.getenv('SMTP_HOST')
        smtp_port = int(os.getenv('SMTP_PORT'))
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')
        sender_email = os.getenv('SMTP_SENDER')
        
        if not all([smtp_host, smtp_port, smtp_user, smtp_pass, sender_email]):
            print("Missing SMTP configuration")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset Your Pawfect Password'
        msg['From'] = sender_email
        msg['To'] = email
        
        # Add plain text and HTML parts
        text = f"Hello {name},\n\nWe received a request to reset your password. Click this link to reset your password: {reset_url}\n\nThis link will expire in 24 hours.\n\nIf you did not request a password reset, you can ignore this email.\n\nRegards,\nThe Pawfect Team"
        html = f'''
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #FF6B6B;">Password Reset Request</h2>
            <p>Hi {name},</p>
            <p>Please click to reset your password: <a href="{reset_url}">Reset Password</a></p>
            <p>This link will expire in 24 hours.</p>
        </div>
        '''
        
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')
        msg.attach(part1)
        msg.attach(part2)
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_pass)
        
        # Send email
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        print("SMTP password reset email sent successfully!")
        return True
        
    except Exception as smtp_error:
        print(f"SMTP error: {str(smtp_error)}")
        print("All email sending methods failed.")
        # Just return the reset URL for testing
        print(f"FOR TESTING: Use this reset URL manually: {reset_url}")
        return False

# User Routes
@app.route('/api/user', methods=['GET'])
def get_users():
    try:
        result = supabase.table('users').select('id, name, email, role, phone, address, profile_image, created_at, updated_at').execute()
        return format_response(result.data)
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        result = supabase.table('users').select('id, name, email, role, phone, address, profile_image, created_at, updated_at').eq('id', user_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "User not found")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        data = request.json
        update_data = {}
        
        # Only update fields that are provided
        allowed_fields = ['name', 'email', 'role', 'phone', 'address', 'profile_image']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        # Handle password update separately (if provided)
        if 'password' in data and data['password']:
            update_data['password'] = generate_password_hash(data['password'])
            
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
            
        result = supabase.table('users').update(update_data).eq('id', user_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "User not found or no changes made")
            
        # Don't return the password in the response
        user = result.data[0]
        user.pop('password', None)
        
        return format_response(user)
    except Exception as e:
        return format_response(None, str(e))

# Pet Routes
@app.route('/api/pet', methods=['GET'])
def get_pets():
    try:
        result = supabase.table('pets').select('*').execute()
        return format_response(result.data)
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/pet/<pet_id>', methods=['GET'])
def get_pet(pet_id):
    try:
        print(f"\n===== FETCHING PET WITH ID: {pet_id} =====")
        # Get the main pet data
        pet_result = supabase.table('pets').select('*').eq('id', pet_id).execute()
        
        if len(pet_result.data) == 0:
            print(f"Pet with ID {pet_id} not found")
            return format_response(None, "Pet not found")
            
        pet = pet_result.data[0]
        print(f"Found pet: {pet.get('name')}")
        print(f"Available fields: {list(pet.keys())}")
        
        # Handle image URLs properly
        if 'image_url' not in pet and 'photo_url' in pet:
            pet['image_url'] = pet['photo_url']
        elif 'image_url' not in pet:
            print("No image URL found for pet, using default")
            pet['image_url'] = '/Img/default-pet.jpg'
            
        print(f"Image URL: {pet.get('image_url')}")
        
        # Get additional photos for the pet
        photos_result = supabase.table('pet_photos').select('*').eq('pet_id', pet_id).execute()
        pet['additional_photos'] = photos_result.data
        
        print(f"Returning pet data with image URL: {pet.get('image_url')}")
        print("===== END OF PET FETCH =====\n")
        return format_response(pet)
    except Exception as e:
        print(f"Error fetching pet: {str(e)}")
        import traceback
        traceback.print_exc()
        return format_response(None, str(e))

@app.route('/api/pet', methods=['POST'])
def create_pet():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500

        data = request.json
        print(f"Received pet data: {data}")

        required_fields = ['name', 'species', 'breed', 'age', 'gender', 'status']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        # Validate photo URLs
        if not data.get('photo_url'):
            return jsonify({"success": False, "message": "At least one photo is required"}), 400
        
        # Create pet record
        pet_data = {
            'name': data['name'],
            'species': data['species'],
            'breed': data['breed'],
            'age': data['age'],
            'gender': data['gender'],
            'description': data.get('description', ''),
            'status': data['status'],
            'photo_url': data['photo_url'],
            'created_at': datetime.now(timezone.utc).isoformat()
        }

        print(f"Creating pet with data: {pet_data}")
        
        # Insert into pets table
        result = supabase.table('pets').insert(pet_data).execute()
        
        if len(result.data) == 0:
            print("Failed to create pet: No data returned")
            return jsonify({"success": False, "message": "Failed to create pet"}), 400

        pet_id = result.data[0]['id']

        # Store additional photos in pet_photos table
        if 'photos' in data and len(data['photos']) > 1:
            photo_records = [
                {
                    'pet_id': pet_id,
                    'photo_url': photo_url,
                    'is_main': photo_url == data['photo_url'],
                    'created_at': datetime.now(timezone.utc).isoformat()
                }
                for photo_url in data['photos']
            ]
            
            photos_result = supabase.table('pet_photos').insert(photo_records).execute()
            
            if len(photos_result.data) == 0:
                print("Warning: Failed to store additional photos")

        print(f"Pet created successfully: {pet_id}")
        return jsonify({
            "success": True,
            "message": "Pet created successfully",
            "data": result.data[0]
        })

    except Exception as e:
        print(f"Error creating pet: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/pet/<pet_id>', methods=['PUT'])
def update_pet(pet_id):
    try:
        data = request.json
        update_data = {}
        
        # Only update fields that are provided
        allowed_fields = ['name', 'species', 'breed', 'age', 'description', 'image_url', 'status']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
                
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = supabase.table('pets').update(update_data).eq('id', pet_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Pet not found or no changes made")
            
        pet = result.data[0]
        
        # Handle additional photos if provided
        if 'additional_photos' in data:
            # First, delete existing photos
            supabase.table('pet_photos').delete().eq('pet_id', pet_id).execute()
            
            # Then add new photos
            if data['additional_photos']:
                photo_data = [{'pet_id': pet_id, 'photo_url': photo} for photo in data['additional_photos']]
                photos_result = supabase.table('pet_photos').insert(photo_data).execute()
                pet['additional_photos'] = photos_result.data
            else:
                pet['additional_photos'] = []
        else:
            # Get current photos
            photos_result = supabase.table('pet_photos').select('*').eq('pet_id', pet_id).execute()
            pet['additional_photos'] = photos_result.data
        
        return format_response(pet)
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/pet/<pet_id>', methods=['DELETE'])
def delete_pet(pet_id):
    try:
        # This will automatically delete related pet_photos due to the ON DELETE CASCADE constraint
        result = supabase.table('pets').delete().eq('id', pet_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Pet not found")
            
        return format_response({"message": "Pet deleted successfully"})
    except Exception as e:
        return format_response(None, str(e))

# Application Routes
@app.route('/api/application', methods=['GET'])
def get_applications():
    try:
        result = supabase.table('applications').select('*').execute()
        return format_response(result.data)
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/application/user/<user_id>', methods=['GET'])
def get_user_applications(user_id):
    try:
        # First get all applications for the user
        applications = supabase.table('applications').select('*').eq('user_id', user_id).execute()
        
        if not applications.data:
            return format_response([])
            
        # Get all pet IDs from the applications
        pet_ids = [app['pet_id'] for app in applications.data]
        
        # Get pet information for all pets in the applications
        pets = supabase.table('pets').select('*').in_('id', pet_ids).execute()
        
        # Create a dictionary of pets for easy lookup
        pets_dict = {pet['id']: pet for pet in pets.data}
        
        # Combine application and pet data
        combined_data = []
        for app in applications.data:
            pet = pets_dict.get(app['pet_id'], {})
            combined_data.append({
                'id': app['id'],
                'user_id': app['user_id'],
                'pet_id': app['pet_id'],
                'status': app['status'],
                'reason': app['reason'],
                'application_date': app['application_date'],
                'updated_at': app.get('updated_at'),
                'admin_notes': app.get('admin_notes'),
                'pet_name': pet.get('name', 'Unknown Pet'),
                'pet_breed': pet.get('breed', 'Unknown Breed'),
                'pet_age': pet.get('age', 'Unknown Age'),
                'pet_photo': pet.get('photo_url', '/Img/default-pet.jpg')
            })
            
        return format_response(combined_data)
    except Exception as e:
        print(f"Error fetching user applications: {str(e)}")
        return format_response(None, str(e))

@app.route('/api/application/<application_id>', methods=['GET'])
def get_application(application_id):
    try:
        result = supabase.table('applications').select('*').eq('id', application_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Application not found")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/application', methods=['POST'])
def create_application():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return format_response(None, "Database connection error")
            
        data = request.json
        print(f"Received application data: {data}")
        
        required_fields = ['user_id', 'pet_id', 'status', 'reason']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return format_response(None, f"Missing required field: {field}")
        
        # Ensure living_situation is a JSON string containing file URLs
        living_situation = data.get('living_situation', {})
        if isinstance(living_situation, str):
            try:
                living_situation = json.loads(living_situation)
            except json.JSONDecodeError:
                print("Invalid living_situation JSON format")
                return format_response(None, "Invalid living_situation format")
        
        # Validate file URLs if present
        if 'validIdUrl' in living_situation:
            if not living_situation['validIdUrl'].startswith('http'):
                print("Invalid validIdUrl format")
                return format_response(None, "Invalid valid ID URL format")
                
        if 'houseImageUrl' in living_situation:
            if not living_situation['houseImageUrl'].startswith('http'):
                print("Invalid houseImageUrl format")
                return format_response(None, "Invalid house image URL format")
        
        # Create application record
        application_data = {
            'user_id': data['user_id'],
            'pet_id': data['pet_id'],
            'status': data['status'],
            'reason': data['reason'],
            'living_situation': json.dumps(living_situation),  # Store as JSON string
            'other_pets': data.get('other_pets'),
            'experience': data.get('experience'),
            'admin_notes': data.get('admin_notes'),
            'application_date': datetime.now(timezone.utc).isoformat()
        }
        
        print(f"Creating application with data: {application_data}")
        
        result = supabase.table('applications').insert(application_data).execute()
        
        if len(result.data) == 0:
            print("Failed to create application: No data returned")
            return format_response(None, "Failed to create application")
            
        print(f"Application created successfully: {result.data[0]['id']}")
        return format_response(result.data[0])
        
    except Exception as e:
        print(f"Error creating application: {str(e)}")
        return format_response(None, str(e))

@app.route('/api/application/<application_id>', methods=['PUT'])
def update_application(application_id):
    try:
        data = request.json
        update_data = {}
        
        # Only update fields that are provided
        allowed_fields = ['status', 'reason', 'living_situation', 'other_pets', 'experience', 'admin_notes']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
                
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = supabase.table('applications').update(update_data).eq('id', application_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Application not found or no changes made")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

# Appointment Routes
@app.route('/api/appointment', methods=['GET'])
def get_appointments():
    try:
        result = supabase.table('appointments').select('*').execute()
        return format_response(result.data)
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/appointment/<appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    try:
        result = supabase.table('appointments').select('*').eq('id', appointment_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Appointment not found")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/appointment', methods=['POST'])
def create_appointment():
    try:
        data = request.json
        required_fields = ['user_id', 'pet_id', 'appointment_date', 'status']
        
        # Validate required fields
        for field in required_fields:
            if field not in data:
                return format_response(None, f"Missing required field: {field}")
        
        # Create appointment record
        appointment_data = {
            'user_id': data['user_id'],
            'pet_id': data['pet_id'],
            'appointment_date': data['appointment_date'],
            'status': data['status'],
            'notes': data.get('notes')
        }
        
        result = supabase.table('appointments').insert(appointment_data).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Failed to create appointment")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/appointment/<appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    try:
        data = request.json
        update_data = {}
        
        # Only update fields that are provided
        allowed_fields = ['appointment_date', 'status', 'notes']
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
                
        # Add updated_at timestamp
        update_data['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = supabase.table('appointments').update(update_data).eq('id', appointment_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Appointment not found or no changes made")
            
        return format_response(result.data[0])
    except Exception as e:
        return format_response(None, str(e))

@app.route('/api/appointment/<appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):
    try:
        result = supabase.table('appointments').delete().eq('id', appointment_id).execute()
        
        if len(result.data) == 0:
            return format_response(None, "Appointment not found")
            
        return format_response({"message": "Appointment deleted successfully"})
    except Exception as e:
        return format_response(None, str(e))

# Storage Routes for file uploads
@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        print("Upload endpoint called")
        
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        if 'file' not in request.files:
            print("No file part in request")
            return jsonify({"success": False, "message": "No file part"}), 400
            
        file = request.files['file']
        print(f"Received file: {file.filename}")
        
        if file.filename == '':
            print("No selected file")
            return jsonify({"success": False, "message": "No selected file"}), 400
            
        # Get file extension
        ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        
        if ext not in allowed_extensions:
            print(f"Invalid file type: {ext}")
            return jsonify({"success": False, "message": f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"}), 400
            
        # Generate a unique filename
        from uuid import uuid4
        filename = f"{uuid4()}.{ext}"
        
        # Read file bytes
        file_bytes = file.read()
        
        # Check file size (limit to 5MB)
        if len(file_bytes) > 5 * 1024 * 1024:  # 5MB in bytes
            print(f"File too large: {len(file_bytes)} bytes")
            return jsonify({"success": False, "message": "File size exceeds 5MB limit"}), 400
        
        print(f"Attempting to upload file to Supabase storage: {filename}")
        
        try:
            # First check if bucket exists
            try:
                buckets = supabase.storage.list_buckets()
                bucket_exists = any(bucket['name'] == 'pet_images' for bucket in buckets)
                
                if not bucket_exists:
                    print("Creating 'pet_images' bucket")
                    try:
                        supabase.storage.create_bucket('pet_images', {'public': True})
                        print("Bucket created successfully")
                    except Exception as bucket_error:
                        print(f"Error creating bucket: {str(bucket_error)}")
                        # If bucket creation fails, try to continue anyway as it might already exist
                        pass
            except Exception as list_error:
                print(f"Error listing buckets: {str(list_error)}")
                # Continue anyway as the bucket might exist
            
            # Upload to Supabase Storage in the 'pet_images' bucket
            print("Uploading file to Supabase storage...")
            result = supabase.storage.from_('pet_images').upload(
                filename,
                file_bytes,
                file_options={
                    'content-type': f'image/{ext}'
                }
            )
            
            print(f"Upload result: {result}")
            
            if isinstance(result, dict) and 'error' in result:
                print(f"Supabase storage error: {result['error']}")
                return jsonify({"success": False, "message": result['error'].get('message', 'Upload failed')}), 400
            
            # Get public URL
            file_url = supabase.storage.from_('pet_images').get_public_url(filename)
            print(f"File uploaded successfully: {file_url}")
            
            return jsonify({
                "success": True,
                "message": "File uploaded successfully",
                "data": {
                    "url": file_url
                }
            })
            
        except Exception as upload_error:
            print(f"Error during file upload: {str(upload_error)}")
            print(f"Error type: {type(upload_error)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({"success": False, "message": f"Failed to upload file: {str(upload_error)}"}), 500
            
    except Exception as e:
        print(f"Unexpected error in upload_file: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"success": False, "message": str(e)}), 500

# Adoption Steps Routes
@app.route('/api/adoption-steps', methods=['GET'])
def get_adoption_steps():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        result = supabase.table('adoption_steps').select('*').order('step_number').execute()
        print(f"Adoption steps result: {result}")
        return jsonify({"success": True, "data": result.data})
    except Exception as e:
        print(f"Error fetching adoption steps: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

# Shelter Info Routes
@app.route('/api/shelter-info', methods=['GET'])
def get_shelter_info():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        result = supabase.table('shelter_info').select('*').limit(1).execute()
        print(f"Shelter info result: {result}")
        
        if result.data and len(result.data) > 0:
            return jsonify({"success": True, "data": result.data[0]})
        else:
            return jsonify({"success": False, "message": "No shelter information found"}), 404
    except Exception as e:
        print(f"Error fetching shelter info: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

# Admin Dashboard Routes
@app.route('/api/admin/stats', methods=['GET'])
def get_admin_stats():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        # Get total pets count
        pets_result = supabase.table('pets').select('id, status').execute()
        total_pets = len(pets_result.data) if pets_result.data else 0
        
        # Count available pets
        available_pets = sum(1 for pet in pets_result.data if pet['status'] == 'available')
        
        # Get pending applications count
        applications_result = supabase.table('applications').select('id, status').execute()
        pending_applications = sum(1 for app in applications_result.data if app['status'] == 'pending')
        
        # Count completed adoptions
        completed_adoptions = sum(1 for app in applications_result.data if app['status'] == 'approved')
        
        stats = {
            'totalPets': total_pets,
            'availablePets': available_pets,
            'pendingApplications': pending_applications,
            'completedAdoptions': completed_adoptions
        }
        
        return jsonify({"success": True, "data": stats})
    except Exception as e:
        print(f"Error fetching admin stats: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/admin/recent-activities', methods=['GET'])
def get_recent_activities():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
            
        # Get recent applications
        applications_query = supabase.table('applications')\
            .select('id, status, user_id, pet_id, application_date')\
            .order('application_date', desc=True)\
            .limit(5)\
            .execute()
            
        # Get recent pets added
        pets_query = supabase.table('pets')\
            .select('id, name, breed, created_at')\
            .order('created_at', desc=True)\
            .limit(5)\
            .execute()
            
        # Get recent appointments
        appointments_query = supabase.table('appointments')\
            .select('id, user_id, pet_id, appointment_date, status')\
            .order('created_at', desc=True)\
            .limit(5)\
            .execute()
            
        # Format the recent activities
        activities = []
        activity_id = 1
        
        # Process applications
        for app in applications_query.data:
            # Get pet details
            pet_result = supabase.table('pets').select('name, breed').eq('id', app['pet_id']).execute()
            pet_name = pet_result.data[0]['name'] if pet_result.data else 'Unknown Pet'
            pet_breed = pet_result.data[0]['breed'] if pet_result.data else ''
            
            activity_type = 'adoption' if app['status'] == 'approved' else 'application'
            icon = 'fas fa-home' if app['status'] == 'approved' else 'fas fa-file-alt'
            
            text = f"{'Adoption completed' if app['status'] == 'approved' else 'New application'} for {pet_name} ({pet_breed})"
            
            # Calculate time ago
            app_date = app['application_date']
            time_ago = calculate_time_ago(app_date)
            
            activities.append({
                'id': activity_id,
                'type': activity_type,
                'icon': icon,
                'text': text,
                'time': time_ago
            })
            activity_id += 1
        
        # Process new pets
        for pet in pets_query.data:
            activities.append({
                'id': activity_id,
                'type': 'pet',
                'icon': 'fas fa-paw',
                'text': f"New pet added: {pet['name']} ({pet['breed']})",
                'time': calculate_time_ago(pet['created_at'])
            })
            activity_id += 1
            
        # Process appointments
        for appt in appointments_query.data:
            # Get pet details
            pet_result = supabase.table('pets').select('name').eq('id', appt['pet_id']).execute()
            pet_name = pet_result.data[0]['name'] if pet_result.data else 'Unknown Pet'
            
            activities.append({
                'id': activity_id,
                'type': 'appointment',
                'icon': 'fas fa-calendar-check',
                'text': f"New appointment scheduled for {pet_name}",
                'time': calculate_time_ago(appt['appointment_date'])
            })
            activity_id += 1
        
        # Sort by time (most recent first) and limit to 10
        activities = sorted(activities, key=lambda x: parse_time_ago(x['time']))
        activities = activities[:10]
        
        return jsonify({"success": True, "data": activities})
    except Exception as e:
        print(f"Error fetching recent activities: {str(e)}")
        return jsonify({"success": False, "message": str(e)}), 500

def calculate_time_ago(timestamp_str):
    """Convert a timestamp string to a human-readable 'time ago' format"""
    try:
        # Parse the timestamp string
        if isinstance(timestamp_str, str):
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        else:
            timestamp = timestamp_str
            
        now = datetime.now(timezone.utc)
        diff = now - timestamp
        
        if diff.days > 30:
            return f"{diff.days // 30} months ago"
        elif diff.days > 0:
            return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            return f"{diff.seconds // 3600} hours ago"
        elif diff.seconds >= 60:
            return f"{diff.seconds // 60} minutes ago"
        else:
            return "Just now"
    except Exception as e:
        print(f"Error calculating time ago: {str(e)}")
        return "Recently"

def parse_time_ago(time_str):
    """Parse a 'time ago' string to determine recency for sorting"""
    try:
        if "just now" in time_str.lower():
            return 0
        elif "minute" in time_str:
            return int(time_str.split()[0]) * 60
        elif "hour" in time_str:
            return int(time_str.split()[0]) * 3600
        elif "day" in time_str:
            return int(time_str.split()[0]) * 86400
        elif "month" in time_str:
            return int(time_str.split()[0]) * 2592000
        else:
            return 999999  # Very old
    except:
        return 999999  # Default to very old if parsing fails

# Featured Pets Route
@app.route('/api/featured-pets', methods=['GET'])
def get_featured_pets():
    try:
        if not supabase:
            print("Supabase client is not initialized")
            return jsonify({"success": False, "message": "Database connection error"}), 500
        
        print("\n===== FETCHING FEATURED PETS FROM SUPABASE =====")
        # Get all pets regardless of status
        result = supabase.table('pets').select('*').execute()
        
        if not result.data:
            print("WARNING: No pets found in Supabase database")
            return jsonify({"success": True, "data": []})
            
        print(f"Total pets found in database: {len(result.data)}")
        
        # Display all pets and their data for debugging
        for i, pet in enumerate(result.data):
            status = pet.get('status', 'undefined')
            print(f"Pet {i+1}: ID={pet.get('id')}, Name={pet.get('name')}, Status={status}")
            print(f"  - Available fields: {list(pet.keys())}")
        
        # Get all pets, prioritizing those with 'available' status but not filtering out others
        # This ensures you'll see pets even if the status field is missing or has other values
        pets_to_show = sorted(result.data, key=lambda p: 0 if p.get('status') == 'available' else 1)[:4]
        print(f"Pets selected to display: {len(pets_to_show)}")
        
        # Format the response to match frontend expectations
        formatted_pets = []
        for pet in pets_to_show:  # Take up to 4 pets
            age_value = pet.get('age')
            if age_value is not None:
                if age_value >= 1:
                    age_str = f"{age_value} {'years' if age_value > 1 else 'year'}"
                else:
                    age_str = f"{int(age_value * 12)} months"
            else:
                age_str = "Unknown"
                
            pet_data = {
                'id': pet.get('id'),
                'name': pet.get('name', 'Unnamed Pet'),
                'breed': pet.get('breed', 'Unknown Breed'),
                'age': age_str,
                'gender': pet.get('gender', 'Unknown'),
                'image_url': pet.get('image_url') or pet.get('photo_url') or '/Img/default-pet.jpg',
                'description': pet.get('description', 'A wonderful companion waiting for a forever home.')
            }
            print(f"Formatted pet for frontend: {pet_data}")
            formatted_pets.append(pet_data)
            
        print(f"Returning {len(formatted_pets)} pets to frontend")
        print("===== END OF FEATURED PETS PROCESSING =====\n")
        return jsonify({"success": True, "data": formatted_pets})
    except Exception as e:
        print(f"ERROR fetching featured pets: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": str(e)}), 500

# Adoption History Route
@app.route('/api/adoption-history', methods=['GET'])
def get_adoption_history():
    try:
        # This endpoint retrieves adoption history (completed applications with status "approved")
        adoption_history = supabase.table('applications')\
            .select('*')\
            .eq('status', 'approved')\
            .execute()
            
        if not adoption_history.data:
            return format_response([])
            
        return format_response(adoption_history.data)
    except Exception as e:
        print(f"Error fetching adoption history: {str(e)}")
        return format_response(None, f"Failed to fetch adoption history: {str(e)}")

# Remove the direct run command and add Vercel handler
app.debug = False

# Vercel requires a handler
if __name__ == '__main__':
    if os.getenv('VERCEL_ENV') == 'development':
        app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
