from functools import wraps
from flask import request, jsonify, current_app
from http import HTTPStatus
import jwt
from jwt.exceptions import InvalidTokenError

def get_user_id_from_token():
    """Extract user ID from JWT token in cookie."""
    token = request.cookies.get('auth_token')
    if not token:
        return None
        
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload['sub']  # user_id is stored in 'sub' claim
    except InvalidTokenError:
        return None

def jwt_required(f):
    """Decorator to protect routes with JWT authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_user_id_from_token()
        if not user_id:
            return jsonify({'error': 'Authentication required'}), HTTPStatus.UNAUTHORIZED
            
        # Store user_id in flask.g for use in the route
        from flask import g
        g.user_id = user_id
        return f(*args, **kwargs)
    return decorated 