import requests
from .config import config
from .logger import logger

print("Starting API Client")
class APIClient:
    def __init__(self):
        self.base_url = config.get('http://localhost:8000')
        # self.token = config.get('api_token')

    def get(self, endpoint):
        try:
            response = requests.get(f"{self.base_url}/{endpoint}", headers={'Authorization': f'Bearer {self.token}'})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None

    def post(self, endpoint, data):
        try:
            response = requests.post(f"{self.base_url}/{endpoint}", json=data, headers={'Authorization': f'Bearer {self.token}'})
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            return None