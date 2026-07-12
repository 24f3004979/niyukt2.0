from flask import Blueprint,request,jsonify

from flask_jwt_extended import (
    create_access_token
)

from app.services.auth_service import (
    register_user,
    authenticate
)


auth_bp = Blueprint(
    "auth",
    __name__
)



@auth_bp.route(
"/register",
methods=["POST"]
)
def register():

    user = register_user(
        request.json
    )

    return jsonify(
        user.serialize()
    )




@auth_bp.route(
"/login",
methods=["POST"]
)
def login():

    data=request.json


    user = authenticate(
        data["username"],
        data["password"]
    )


    if not user:
        return {
            "error":"Invalid credentials"
        },401


    token=create_access_token(
        identity={
            "id":user.id,
            "role":user.role
        }
    )


    return {
        "token":token
    }
