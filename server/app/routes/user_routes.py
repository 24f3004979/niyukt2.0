from flask import Blueprint, request, jsonify

from app.services.user_service import (
    get_all_users,
    create_user
)


user_bp = Blueprint(
    "users",
    __name__
)



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
