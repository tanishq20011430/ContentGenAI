from flask import Blueprint, jsonify, request, g, render_template, current_app
import time
import logging
import os
from services.web_scraper import WebScraper  # Keep this import
from config.settings import Config
from core.exceptions import ContentFetchError
from services.content_generator import ContentGenerator
from services.history_manager import HistoryManager
from core.exceptions import ContentFetchError, ProcessingError

api = Blueprint('api', __name__)
content_generator = ContentGenerator()

@api.before_request
def before_request():
    g.request_start_time = time.time()

@api.after_request
def after_request(response):
    if hasattr(g, 'request_start_time'):
        elapsed = time.time() - g.request_start_time
        logging.info(f"Request processed in {elapsed:.2f} seconds")
    return response

@api.route('/')
def index():
    return render_template('index.html')

@api.route('/generate_content', methods=['POST'])
def generate_content():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"error": "URL is required"}), 400

        if not WebScraper.is_valid_url(url):
            return jsonify({"error": "Invalid URL format"}), 400

        if not WebScraper.is_allowed_domain(url):
            return jsonify({"error": "Domain not allowed"}), 403

        content = WebScraper.scrape_content(url)
        if not content:
            return jsonify({"error": "No content found at URL"}), 400

        keywords = content_generator.extract_keywords(content)
        if not keywords:
            return jsonify({"error": "Failed to extract keywords"}), 400

        prompt = f"""Based on the following keywords, write a comprehensive article:
        Keywords: {', '.join(keywords)}
        
        Please make sure the content is:
        - Well-structured with clear paragraphs
        - Engaging and informative
        - Between 400-600 words
        - Written in a professional tone
        """
        
        generated_content = content_generator.generate_content(prompt)
        if not generated_content:
            return jsonify({"error": "Failed to generate content"}), 500

        response_data = {
            "url": url,
            "keywords": keywords,
            "generated_content": generated_content,
            "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
        }

        HistoryManager.save_to_history(response_data)

        return jsonify(response_data)

    except ContentFetchError as e:
        return jsonify({"error": str(e)}), 400
    except ProcessingError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@api.route('/history')
def get_history():
    try:
        # Fetch history data from HistoryManager
        history = HistoryManager.read_history()
        return render_template('history.html', history=history)  # Pass the history to the template
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        return jsonify({"error": "Failed to fetch history"}), 500

@api.route('/api/analytics')
def get_analytics():
    try:
        # Fetch analytics data from HistoryManager
        analytics = HistoryManager.get_analytics()
        return jsonify(analytics)
    except Exception as e:
        logging.error(f"Analytics error: {e}")
        return jsonify({"error": "Failed to fetch analytics"}), 500

from flask import Blueprint, render_template, session, redirect, url_for, flash

main = Blueprint('main', __name__)

@main.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first!', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('dashboard.html', username=session['username'])
