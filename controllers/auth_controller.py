import datetime
from flask import request, jsonify
from services.auth_service import register_user, authenticate_user
from database import SessionLocal
import jwt


    
JWT_SECRET = "ironman"

class AuthController:
    @staticmethod
    def register():
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400

        db = SessionLocal()
        try:
            # Structuring payload exactly as your register_user function expects
            registration_payload = {
                'username': username,
                'password': password,
                'role': data.get('role'),
                'profile_info': data.get('profile_info', {})
            }
            
            # Passing the db Session and data payload dictionary
            user = register_user(db, registration_payload)
            return jsonify({'message': f"User '{user.username}' registered successfully"}), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': "Internal Server Error during registration"}), 500

    @staticmethod
    def login():
        data = request.get_json() or {}
        print(f"Data Recieved into controller unit: {data}")
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400

        db = SessionLocal()
        print(f"Session object initiation : {db}")
        try:
            # Validates credentials via your service logic
            user = authenticate_user(db, username, password)

            print(f"Credential Matching controller component : {user}")
            
            # Generate the secure web token session
            session_token = jwt.encode({
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
            }, JWT_SECRET, algorithm='HS256')
            
            # Session Token being sent for the future communication
            return jsonify({
                'token': session_token, 
                'message': 'Login successful',
                'user': {'username': user.username, 'role': user.role}
            }), 200
            
        except (ValueError, PermissionError) as e:
            return jsonify({'error': str(e)}), 401
        except Exception as e:
            return jsonify({'error': f"Internal Server Error during authentication : {e}"}), 500
