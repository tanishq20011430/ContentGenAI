from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import re
from config.settings import Config
from core.exceptions import ContentFetchError

class WebScraper:
    @staticmethod
    def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    @staticmethod
    def is_allowed_domain(url):
        try:
            domain = urlparse(url).netloc
            return domain in Config.ALLOWED_DOMAINS or True
        except Exception:
            return False

    @staticmethod
    def scrape_content(url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=Config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            
            if main_content:
                text = main_content.get_text()
                text = re.sub(r'\s+', ' ', text).strip()
                text = re.sub(r'\n\s*\n', '\n', text)
                return text
            
            return None

        except requests.Timeout:
            raise ContentFetchError("Request timed out while fetching content")
        except requests.RequestException as e:
            raise ContentFetchError(f"Failed to fetch content: {str(e)}")