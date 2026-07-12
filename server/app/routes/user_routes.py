from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity


from app.services.user_service import (
    get_all_users,
    create_user
)


user_bp = Blueprint(
    "users",
    __name__
)

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():

    print(f'API HIT for user identitty')
    user = User.query.get(get_jwt_identity())
    print(f"Working for fetching user information : {user}")
    if not user:
        return jsonify({"success": False, "error": {"message": "User not found"}}), 404
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
