from flask import Flask, jsonify
from flask_cors import CORS
import os
from core.logging_config import setup_logging
from api.routes import api
from api.error_handlers import errors
from config.settings import Config
import json

# App Factory
def create_app():
    app = Flask(__name__, 
                static_folder='static',
                template_folder='templates')
    
    # Setup logging
    setup_logging()
    
    # Setup CORS
    CORS(app, resources={
        r"/api/*": {"origins": "*"},
        r"/generate_content": {"origins": "*"},
        r"/history": {"origins": "*"}
    })
    
    # Ensure data directory exists
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(api)
    app.register_blueprint(errors)

    # Add route to fetch content history
    @app.route('/history', methods=['GET'])
    def get_history():
        history_file = 'content_history.json'
        try:
            # Read history from the JSON file
            with open(history_file, 'r') as f:
                history_data = json.load(f)
            return jsonify(history_data)
        except FileNotFoundError:
            return jsonify({'error': 'History file not found.'}), 404
        except json.JSONDecodeError:
            return jsonify({'error': 'Failed to decode history data.'}), 500

    return app

# Main Execution
if __name__ == '__main__':
    app = create_app()
    app.run(debug=os.getenv('FLASK_DEBUG', 'True').lower() == 'true')
