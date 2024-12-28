import json
import os
from datetime import datetime
import logging
from config.settings import Config
from core.exceptions import ProcessingError

class HistoryManager:
    @staticmethod
    def read_history():
        try:
            if os.path.exists(Config.HISTORY_FILE):
                with open(Config.HISTORY_FILE, 'r') as file:
                    return json.load(file)
            return []
        except Exception as e:
            logging.error(f"Error reading history: {e}")
            return []

    @staticmethod
    def save_to_history(data):
        try:
            history = HistoryManager.read_history()
            history.insert(0, {
                "url": data["url"],
                "keywords": data["keywords"],
                "generated_content": data["generated_content"],
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "word_count": len(data["generated_content"].split()),
                    "keyword_count": len(data["keywords"])
                }
            })
            
            # Limiting history to the last 100 entries
            history = history[:100]
            
            with open(Config.HISTORY_FILE, 'w') as file:
                json.dump(history, file, indent=4)
                
        except Exception as e:
            logging.error(f"Error saving to history: {e}")
            raise ProcessingError("Failed to save content history")

    @staticmethod
    def get_analytics():
        try:
            history = HistoryManager.read_history()
            
            analytics = {
                "total_generations": len(history),
                "keywords": {},
                "timeline": {},
                "average_word_count": 0,
                "average_keywords": 0
            }
            
            total_words = 0
            total_keywords = 0
            
            for entry in history:
                for keyword in entry["keywords"]:
                    analytics["keywords"][keyword] = analytics["keywords"].get(keyword, 0) + 1
                
                date = entry["timestamp"][:10]
                analytics["timeline"][date] = analytics["timeline"].get(date, 0) + 1
                
                if "metadata" in entry:
                    total_words += entry["metadata"]["word_count"]
                    total_keywords += entry["metadata"]["keyword_count"]
            
            if history:
                analytics["average_word_count"] = total_words / len(history)
                analytics["average_keywords"] = total_keywords / len(history)
            
            # Convert timeline dictionary into a sorted list
            analytics["timeline"] = [
                {"date": date, "count": count}
                for date, count in sorted(analytics["timeline"].items())
            ]
            
            return analytics
            
        except Exception as e:
            logging.error(f"Analytics error: {e}")
            raise ProcessingError("Failed to fetch analytics")
