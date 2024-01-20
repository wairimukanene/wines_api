from datetime import datetime, date
from ..utils import db 

class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Integer ID
    sale_amount = db.Column(db.DECIMAL(10, 2), nullable=False)
    product_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=True)  # Foreign key to product
    created_at = db.Column(db.Date, default=date.today())  # Use datetime.date.today() for date-only value
    updated_at = db.Column(db.Date, onupdate=date.today())

    # Relationship to Product model
    product = db.relationship("Product", backref="sales")

    def __repr__(self):
        return f"<Sale {self.id}: {self.product.name if self.product else None} - {self.sale_amount}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()