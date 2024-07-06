from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy globally
db = SQLAlchemy()

def create_app():
    """
    Application factory function to create and configure the Flask application.
    """
    app = Flask(__name__)
    
    # Application configurationz

    # config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:sqlpass#4@localhost/blog_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    # Initialize database with the app
    db.init_app(app)
    migrate = Migrate(app, db)  # Initialize migrate with the app

    # Import routes here to avoid circular import
    from . import routes

    # Register routes with the app
    routes.init_app(app)

    # Define custom error handlers
    @app.errorhandler(404)
    def not_found(error):
        """
        Handle 404 Not Found error.
        """
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(400)
    def bad_request(error):
        """
        Handle 400 Bad Request error.
        """
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(500)
    def internal_error(error):
        """
        Handle 500 Internal Server Error.
        """
        return jsonify({"error": "Internal server error"}), 500

    return app
