from ..utils import db

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum('admin', 'clerk'), nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"
    

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()