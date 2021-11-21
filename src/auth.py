from flask import Blueprint,request,jsonify 
from werkzeug.security import check_password_hash,generate_password_hash
from src.static.http_status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT
import validators
from src.database import User

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password)<6:
        return jsonify({"error":"password is too short"}),HTTP_400_BAD_REQUEST
        
    if len(username)<6:
        return jsonify({"error":"username is too short"}),HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return jsonify({"error":"username must be alphanumeric and don't contain spaces"}),HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error":"email not valid"}),HTTP_400_BAD_REQUEST

    if User.objects.filter_by(email=email).first() is not None:
        return jsonify({"error":"email is taken"}),HTTP_409_CONFLICT

    if User.objects.filter_by(username=username).first() is not None:
        return jsonify({"error":"username is taken"}),HTTP_409_CONFLICT
            

    return 'User created'


@auth.get('/me')
def me():
    return {'user': 'me'}
