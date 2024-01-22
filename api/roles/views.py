from flask_restx import Resource, Namespace, fields, marshal
from flask import request
from ..utils import db
from ..models.sales import Sale
from ..models.roles import Role  # Assuming you have a products module with the Product model

roles_namespace = Namespace("roles", description="roles apis")

role_model = roles_namespace.model(
    'Role',
    { 
        "name": fields.String()
    }
)

list_role_model = roles_namespace.model(
    'Role',
    { 
        "id":fields.Integer(),
        "name": fields.String()
    }
)

@roles_namespace.route("/roles")
class SaleViews(Resource):

    def get(self):
        """
        Get all roles
        """
        roles= Role.query.all()
        return marshal(roles, list_role_model), 200

    @roles_namespace.expect(role_model)
    def post(self):

        """create a new role"""
        data = request.get_json()

        name = data.get("name")

        # Check if the product exists
        role = Role.query.filter_by(name=name).first()


        if role:
            return {"message": "role exists"}, 400

        new_role = Role(**data)
        new_role.save()

       

        return marshal(new_role, list_role_model), 201





@roles_namespace.route("/role/<int:id>/")
class PatchProduct(Resource):


    @roles_namespace.expect(role_model)
    def patch(self, id):
        '''
        partial update of a role by its id

        '''
        data = request.get_json()
        
        role = Role.query.filter_by(id=id).first()

        if role:
            for field in data:
                if hasattr(role, field):  # Check if attribute exists
                    setattr(role, field, data[field])

            db.session.commit()
            return marshal(role, list_role_model), 201

        return {"Error": "failed to update"}, 400


    
    def delete(self, id):
        """Delete a Role"""

        role=Role.query.filter_by(id=id).first()

        if role:
            # db.session.delete(role)
            # db.session.commit()
            role.delete()
            return {"message":"successful deleted"}, 204

        return {"message":"role does not exists"}, 404
