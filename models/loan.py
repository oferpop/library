from database import db
from datetime import datetime

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    loan_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Loan {self.id}>'