from flask import Flask
from models import init_db
from routes import views
from config import Config
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(views)
    
    # Add error handlers
    @app.errorhandler(500)
    def handle_500(error):
        logging.error(f"Internal Server Error: {error}")
        return "Internal Server Error", 500
    
    @app.errorhandler(404)
    def handle_404(error):
        return "Page Not Found", 404
    
    return app

app = create_app()

# Only enable debug mode when running locally
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=Config.DEBUG) 