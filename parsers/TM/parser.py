import requests
from bs4 import BeautifulSoup

from googletrans import Translator


class TMParser:
    def __init__(self, api_key):
        self.category = {}
        self.translator = Translator()
        self.api_key = api_key

    @staticmethod
    def decode_text(text):
        return text.encode('latin1').decode('utf-8')

    def translate_text(self, text):
        return self.translator.translate(text, dest='ru').text

    def get_categories(self):
        html = requests.get('https://www.1688.com')
        soup = BeautifulSoup(html.text, 'html.parser')
        categories = soup.find(class_='home-category').find_all('a')
        for category in categories:
            self.category[self.translate_text(self.decode_text(category.text))] = self.decode_text(category.text)

    def get_products(self, category_name: str):
        params = {"apiToken": self.api_key,
                  "page": 1,
                  "page_size": 20,
                  "keyword": self.category[category_name],
                  "sort": "default"}

        result = requests.get('http://api.tmapi.top/1688/search/items', params=params).json()
        return result

    def get_product_details(self, link):
        url = "http://api.tmapi.top/1688/v2/item_detail_by_url"

        querystring = {"apiToken": self.api_key}

        payload = {"url": link}

        response = requests.post(url, json=payload, params=querystring)

        return response.json()
