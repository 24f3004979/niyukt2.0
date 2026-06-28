from flask import Flask
from flask_cors import CORS
from controllers.auth_controller import AuthController

app = Flask(__name__)

# FIX 1: Allow both 'localhost' and '127.0.0.1' origins explicitly 
CORS(app, resources={r"/api/*": {
    "origins": ["http://localhost:8080", "http://127.0.0.1:8080"],
    "methods": ["POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

# Route mapping directly to Controller methods
app.add_url_rule('/api/register', view_func=AuthController.register, methods=['POST'])
app.add_url_rule('/api/login', view_func=AuthController.login, methods=['POST'])


if __name__ == '__main__':
    # FIX 2: Explicitly bind the host to 127.0.0.1 matching your Vue configuration
    app.run(host='127.0.0.1', port=5000, debug=True)

