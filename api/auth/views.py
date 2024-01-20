from flask_restx import Namespace, marshal_with,  Resource, fields
from flask import request
from ..models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http  import HTTPStatus
from flask_jwt_extended import create_access_token , create_refresh_token, jwt_required, get_jwt_identity

auth_namespace= Namespace('auth',"authenitaication apis")


signup_model = auth_namespace.model(
    'User', {
        'id':fields.Integer(),
        'username':fields.String(required=True),
        'password':fields.String(required=True),
        'role':fields.String()
    }
)
login_model = auth_namespace.model(
    'User', {
        'username':fields.String(required=True),
        'password':fields.String(required=True)
    }
)

@auth_namespace.route("/login")
class AuthLogin(Resource):


    @auth_namespace.expect(login_model)
    def post(self):
        """
        Generate Jwt
        
        """
        data= request.get_json()

        username=data.get('username')
        user=User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, data.get('password')):
            access_token =create_access_token(identity=user.username)
            refresh_token =create_refresh_token(identity=user.username)


            response={
                "token": {
                    "access_token":access_token,
                    "refresh_token":refresh_token
                },
                "role": user.role_id
            }


            return response, 200
        return {"error":"user does not exist"}, 404


    

@auth_namespace.route("/signup")
class AuthLogin(Resource):


    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        data=request.get_json()


        new_user=User(
            username=data.get("username"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password")),
            # role=data.get("role")
        )

        new_user.save()
        print(new_user)

        return new_user,   HTTPStatus.CREATED



@auth_namespace.route("/refresh")
class RefreshView(Resource):


    jwt_required(refresh=True)
    def post(self):
        """
        refresh our token 
        """

        username = get_jwt_identity()

        access_token =create_access_token(identity=username)


        return {'access_token':access_token}