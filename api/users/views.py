from flask_restx import Resource, Namespace, fields, marshal
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from ..utils import db
from ..models.users import User  # Assuming you have a users module with the User model


user_namespace = Namespace("users", "users apis")


user_model = user_namespace.model(
    'User',
    {
        'id': fields.Integer(),
        'username': fields.String(),
        'password': fields.String(),
        'role_id': fields.Integer(),
    }
)


@user_namespace.route("/users")
class UserViews(Resource):

    def get(self):
        """
        Get all users
        """
        users = User.query.all()
        return marshal(users, user_model), 200


    @user_namespace.expect(user_model)
    def post(self):
        """
        Register a new user
        """
        data = request.get_json()
        if(data.get("user")):
            data = data["user"]
    

        # Check if the username is already taken
        if User.query.filter_by(username=data['username']).first():
            return {"message": "Username already taken"}, 409

        # Hash the password before saving
        hashed_password = generate_password_hash(data['password'])

        new_user = User(
            username=data['username'],
            password=hashed_password,
        )

        new_user.save()

        return marshal(new_user, user_model), 201



@user_namespace.route("/users/<int:id>/")
class UserDetails(Resource):

    def get(self, id):
        """
        Get user details by ID
        """
        user = User.query.get_or_404(id)
        return marshal(user, user_model), 200

    @user_namespace.expect(user_model)
    def patch(self, id):
        """
        Update user details by ID
        """
        user = User.query.filter_by(id=id).first()
        if not User:

            return {"error": "user not found"}, 404

        data = request.get_json()
        if(data.get("user")):
            data = data["user"]

        try:

            for field in data:
                if hasattr(user, field):
                    setattr(user, field, data[field])

            db.session.commit()

            return marshal(user, user_model), 200
        except:
            return {"error": "cant update"}, 400


    def delete(self, id):
        """
        Delete a user by ID
        """
        user = User.query.filter_by(id=id).first()
        if user:
            user.delete()
            return {"message": "User deleted successfully"}, 204
        else:
            return {"message": "User not found"}, 404
