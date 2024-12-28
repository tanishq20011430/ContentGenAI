from flask import jsonify, Blueprint

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@errors.app_errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@errors.app_errorhandler(429)
def ratelimit_error(error):
    return jsonify({"error": "Rate limit exceeded"}), 429