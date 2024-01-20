from ..utils import db
from datetime import datetime 


class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(), nullable=False, unique=True)
    email=db.Column(db.String(50), nullable=True)
    password=db.Column(db.String(50), nullable=False)
    is_staff=db.Column(db.Boolean(), default=True)

    datejoined = db.Column(db.DateTime, default=datetime.utcnow)  # Sets to current UTC time

    # Foreign key to roles table
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # Assuming 'roles' table exists


    def __repr__(self):
        return f"<User {self.username}>"


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



