from functools import wraps

from flask import jsonify

from flask_jwt_extended import (
    verify_jwt_in_request,
    get_jwt
)



def role_required(required_role):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            # Check JWT exists
            verify_jwt_in_request()


            # Extract claims
            claims = get_jwt()


            user_role = claims.get(
                "role"
            )


            if user_role != required_role:

                return jsonify({

                    "success":False,

                    "message":
                    "Access forbidden"

                }),403


            return function(
                *args,
                **kwargs
            )


        return wrapper


    return decorator
