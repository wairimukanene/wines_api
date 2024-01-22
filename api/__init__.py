from flask import Flask
from .auth.views import auth_namespace
from .products.views import product_namespace
from .sales.views import sales_namespace
from .users.views import user_namespace
from .common.views import summary_namespace
from .roles.views import roles_namespace
from flask_restx import Api
from .config.config import config_dict
from .utils import db
from .models.roles import Role
from .models.users import User
from .models.products import Product
from .models.sales import Sale
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS


def create_app(config=config_dict['dev']):
    app= Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)
    Migrate(app, db)

    jwt=JWTManager(app)

    CORS(app)



    api = Api(app)

    api.add_namespace(auth_namespace, path='/auth')
    api.add_namespace(user_namespace, path='/users')
    api.add_namespace(product_namespace, path='/product')
    api.add_namespace(sales_namespace, path='/sale')
    api.add_namespace(summary_namespace, path='/summary')
    api.add_namespace(roles_namespace)


    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'Role':Role,
            'User':User,
            'Product':Product,
            'Sale':Sale
        }
    return app