from flask_restx import Resource, Namespace, fields, marshal
from flask import request
from ..utils import db
from ..models.sales import Sale
from ..models.products import Product  # Assuming you have a products module with the Product model

sales_namespace = Namespace("sales", description="sales apis")

sale_model = sales_namespace.model(
    'Sale',
    { 
        'sale_amount': fields.Float(),
        'quantity': fields.Integer(),
        'product_id': fields.Integer(),
    }
)

list_sale_model = sales_namespace.model(
    'Sale',
    { 
        'id': fields.Integer(),
        'product_name': fields.String(),
        'sale_amount': fields.Float(),
        'quantity': fields.Integer(),
        'product_id': fields.Integer(),
        'created_at': fields.DateTime(),
        'updated_at': fields.DateTime(),
    }
)


@sales_namespace.route("/makesale")
class SaleViews(Resource):

    def get(self):
        """
        Get all sales
        """
        sales = Sale.query.all()
        return marshal(sales, list_sale_model), 200

    @sales_namespace.expect(sale_model)
    def post(self):
        data = request.get_json()

        id = data.get("product_id")
        quantity = data.get("quantity")

        # Check if the product exists
        product = Product.query.get_or_404(id)

        if product.quantity < quantity:
            return {"message": "Not enough quantity available for sale"}, 400

        new_sale = Sale(**data, product_name=product.name)
        new_sale.save()

        # Reduce the product quantity
        product.quantity -= quantity
        db.session.commit()

        return marshal(new_sale, list_sale_model), 201
