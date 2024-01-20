from flask_restx import Resource, Namespace, fields, marshal
from flask import request
from ..utils import db
from ..models.products import Product


product_namespace=Namespace("products", "products apis")

product_model=product_namespace.model(
    'Product',
    { 
        'name':fields.String(),
        'description':fields.String(),
        'category':fields.String(),
        'price':fields.Integer(),
        'buying_price':fields.Float(),
        'quantity':fields.Integer()
    }
)
list_product_model=product_namespace.model(
    'Product',
    { 
        'id': fields.Integer(),
        'name':fields.String(),
        'description':fields.String(),
        'category':fields.String(),
        'price':fields.Integer(),
        'buying_price':fields.Float(),
        'quantity':fields.Integer()
    }
)





@product_namespace.route("/products")
class ProductViews(Resource):

    def get(self):

        """
        get all products
        
        """

        products = Product.query.all()

        return marshal(products, list_product_model), 200

    @product_namespace.expect(product_model)
    def post(self):
        data= request.get_json()
       

        if(data.get("product")):
            data=data.get("product")


        product = Product.query.filter_by(name=data.get("name")).first()

        if product is not None:
            return {"message":"Product already exists"},409
        
        try:
            new_product=Product(
                **data

            )
            new_product.save()
            return marshal(new_product, list_product_model)
        except:
            return{"message": "Data validation failed"} ,400



@product_namespace.route("/products/<int:id>/")
class PatchProduct(Resource):


    @product_namespace.expect(product_model)
    def patch(self, id):
        '''
        partial update of a product by its id

        '''
        data = request.get_json()
        if data.get("product"):
            data=data.get("product")
        product = Product.query.filter_by(id=id).first()

        if product:
            for field in data:
                if hasattr(product, field):  # Check if attribute exists
                    setattr(product, field, data[field])

            db.session.commit()
            return marshal(product, product_model), 201

        return {"Error": "failed to update"}, 400


    
    def delete(self, id):
        """Delete a Product"""

        product=Product.query.filter_by(id=id).first()

        if product:
            db.session.delete(product)
            db.session.commit()
            # product.delete()
            return {"message":"successful deleted"}, 204

        return {"message":"product does not exists"}, 404




