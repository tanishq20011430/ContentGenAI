# This is a content generation Flask application.
Description
## This Flask application takes a URL as input, scrapes the content from the webpage, extracts keywords, and generates a new article based on those keywords using Google Generative AI.

## Features
Scrape content from webpages
Extract keywords from scraped content
Generate new content based on keywords using Google Generative AI
View generation history
Track analytics on generated content
Requirements

Python 3.6 or later
Flask
Flask-CORS
BeautifulSoup4
requests
spacy
google-generativeai
dotenv
Installation

Clone the repository:
git clone https://github.com/your-username/content-generation-app.git
Install required libraries:
pip install -r requirements.txt
Create a .env file in the root directory of the project and add the following environment variable:   
API_KEY=your_google_generative_ai_api_key
Usage

Start the development server:
FLASK_DEBUG=true flask run
Generate content:
Send a POST request to /generate_content with the following JSON data in the request body:
JSON

{
  "url": "https://www.example.com/article"
}
The response will be a JSON object containing the original URL, extracted keywords, generated content, and timestamp.
View history:
Access the /history endpoint to view a list of previously generated content.
Get analytics:
Access the /api/analytics endpoint to get various analytics on generated content, such as total generations, keyword usage, and average word count.
Contributing

We welcome contributions to this project. Please see the CONTRIBUTING.md file for details.

License

### This project is licensed under the MIT License. See the LICENSE file for details.


### Automated Update - Sat Feb  1 06:21:18 UTC 2025 🚀


### Automated Update - Sat Feb  1 06:25:40 UTC 2025 🚀


### Automated Update - Sat Feb  1 06:37:14 UTC 2025 🚀
