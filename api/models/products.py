from ..utils import db
from datetime import datetime, date

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)  # Integer ID instead of UUID
    name = db.Column(db.String(255), unique=True, nullable=False)
    category = db.Column(db.String(255), default="Alcohol")
    quantity = db.Column(db.Integer, default=0)
    buying_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    price = db.Column(db.DECIMAL(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.Date, default=date.today)  # Use datetime.date.today() for date-only value
    updated_at = db.Column(db.Date, onupdate=date.today)

    def __repr__(self):

        
        return f"<Product {self.name}>"


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
