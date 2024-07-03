from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    from routes import book_routes, customer_routes, loan_routes

    app.register_blueprint(book_routes.bp)
    app.register_blueprint(customer_routes.bp)
    app.register_blueprint(loan_routes.bp)

    return app

def setup_database(app):
    with app.app_context():
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    app = create_app()
    
    if not os.path.exists(Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')):
        setup_database(app)
    
    app.run(debug=True)