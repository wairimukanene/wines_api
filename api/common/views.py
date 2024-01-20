from flask import request
from ..models.sales import Sale 
from ..models.products import Product 
from datetime import datetime, timedelta, date
from flask_restx import Namespace, Resource, marshal, fields
from sqlalchemy import Date, func
from pytz import timezone
from ..utils import db

# Define namespaces for different endpoints
summary_namespace = Namespace('summary', description='Summary views')

product_model=summary_namespace.model(
    'Product',{
        'id':fields.Integer(),
        'name':fields.String(),
        'description':fields.String(),
        'price':fields.Integer(),
        'buying_price':fields.Float(),
        'quantity':fields.Integer()
    }
)

sale_model=summary_namespace.model(
    'catgory',{
        
    'category': fields.String(),
    'product_count': fields.Integer()
       
    }
)

weeklysale=summary_namespace.model(
    'weekly',{
        'date':fields.Date(),
        'total_sales': fields.Integer(),
        'total_amount':fields.Float()
    }
)
revnue_model=summary_namespace.model(
    'revenue', {
        'total_sale_rev': fields.Float()
    }
)

summary_model=summary_namespace.model(
    'summary',
    {
        'date': fields.Date(),
        'total_sales': fields.String(),
        'total_amount': fields.Float(),
    }
)

@summary_namespace.route('/')
class SummaryView(Resource):
    
    def get(self):
            # Retrieve data using model-bound queries
            category_result = Product.query.with_entities(Product.category, func.count(Product.id).label('product_count')).group_by(Product.category).all()
            low_quantity_result = Product.query.filter(Product.quantity < 10).all()

            # print(category_result[0])

            category_objects = [{'category': category[0], 'product_count': category[1]} for category in category_result]
            print(category_objects)

            # Calculate weekly sales
            today = datetime.utcnow()
            # print(today)
            # print(today.weekday())
            start_of_week = today - timedelta(days=today.weekday())
            # print(start_of_week)
            end_of_week = start_of_week + timedelta(days=6)
            # print(Sale.query.filter_by(id=1).first().created_at)

            sales_by_day = Sale.query.with_entities(
                Sale.created_at.label('date'),
                func.count(Sale.id).label('total_sales'),
                func.sum(Sale.sale_amount).label('total_amount')
            ).filter(Sale.created_at >= start_of_week, Sale.created_at <= end_of_week).group_by('date').all()
            
            # print(sales_by_day)
            weekly_sales = []
            for date, total_sales, total_amount in sales_by_day:
                weekly_sales.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'total_sales': total_sales,
                    'total_amount': total_amount
                })
           
            total_sales_rev = db.session.query(func.sum(Sale.sale_amount)).scalar()

            # If you want to handle cases where there are no sales (result might be None)
            total_sales_rev = total_sales_rev or 0

            total_sales=Sale.query.count()

            print(total_sales_rev, total_sales)


            response_data = {
                
                'category_product_count': marshal(category_objects,sale_model),
                'low_quantity_products': marshal(low_quantity_result, product_model),
                'weekly_sales': marshal(weekly_sales, weeklysale),

                'total_sales_rev': marshal(total_sales_rev, revnue_model),
                'total_sales':total_sales
            }

            print(response_data)

        
            return response_data



   


@summary_namespace.route('/category-count')
class SummaryProductView(Resource):
    def get(self):
        """Get category count"""
        total_products = Product.query.count()
        category_count = (
            Product.query.with_entities(Product.category)
            .distinct()
            .count()
        )
        return {'total_products': total_products, 'category_count': category_count}




@summary_namespace.route('/weekly-sales')
class SummaryDetailsView(Resource):

    def get(self):
        """Get weekly sales summary"""
        today = date.today()        
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        sales_by_day = (
            Sale.query.with_entities(
                Sale.created_at.label('date'),
                func.count(Sale.id).label('total_sales'),
                func.sum(Sale.sale_amount).label('total_amount')
            )
            .filter(Sale.created_at >= start_of_week, Sale.created_at <= end_of_week)
            .group_by('date')
            .all()
        )

        print(sales_by_day)

        result = [
            {
                'date': entry.date.strftime('%Y-%m-%d'),
                'total_sales': entry.total_sales,
                'total_amount': entry.total_amount
            } for entry in sales_by_day
        ]

        print(result)
        return marshal(result, summary_model)
        
        
