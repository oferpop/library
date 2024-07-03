from database import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Customer {self.name}>'