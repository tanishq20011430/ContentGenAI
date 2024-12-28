import spacy
import google.generativeai as genai
from collections import Counter
import time
import logging
from config.settings import Config
from core.exceptions import ProcessingError

class ContentGenerator:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        genai.configure(api_key=Config.API_KEY)

    def extract_keywords(self, text, num_keywords=10):
        try:
            text = text[:50000]
            doc = self.nlp(text)
            
            keywords = [token.text.lower() for token in doc 
                       if token.pos_ in ["NOUN", "PROPN"] 
                       and len(token.text) > 2
                       and not token.is_stop]
            
            keyword_freq = Counter(keywords)
            most_common = keyword_freq.most_common(num_keywords)
            
            return [keyword for keyword, _ in most_common]
            
        except Exception as e:
            logging.error(f"Keyword extraction error: {e}")
            raise ProcessingError("Failed to extract keywords")

    def generate_content(self, prompt):
        retries = 0
        while retries < Config.MAX_RETRIES:
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(prompt)
                return response.text.strip()
            except Exception as e:
                retries += 1
                if retries == Config.MAX_RETRIES:
                    logging.error(f"Content generation error after {retries} retries: {e}")
                    raise ProcessingError("Failed to generate content")
                time.sleep(1)