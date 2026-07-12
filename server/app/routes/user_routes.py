from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models.user import User

from app.services.user_service import (
    get_all_users,
    create_user
)


user_bp = Blueprint(
    "users",
    __name__
)

# BUG : get identity part is broken for now not working to fetch details
@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    print('Full JWT')
    print(get_jwt())
    identity = get_jwt_identity()
    user_id = identity
    print(user_id)

    user = User.query.get(user_id)
    if not user:
        return jsonify({"success": False, "error": {"message": "User not found"}}), 404
    
    if user.account_status == "blocked":
        return jsonify({
            "success":False,
            "error":{
            "code":"ACCOUNT_BLOCKED",
            "message":"Your account has been blocked"
            }
            }),403
    
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "account_status": user.account_status,
    })



@user_bp.route(
    "/users",
    methods=["GET"]
)
def users():

    users = get_all_users()

    return jsonify([
        u.serialize()
        for u in users
    ])
