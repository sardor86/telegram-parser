import logging

import requests
from bs4 import BeautifulSoup
from googletrans import Translator

logger = logging.getLogger(__name__)


class TMParser:
    """
    TM parser
    this class get product ans return it from site 1688 with TM api

    you can study the documentation about api from https://tmapi.top/docs/ali/item-detail/get-item-detail-by-id
    """
    def __init__(self, api_key):
        """
        this is an init method for prepare parser
        :param api_key: tm api key

        self.category keeps category information such as 'russian name': 'china name'
        self.translator is used for translate china text to russian text
        self.api_key is tm api key
        """
        logger.info('set 1688 parser')
        self.category = {}
        self.translator = Translator()
        self.api_key = api_key

    @staticmethod
    def decode_text(text):
        """
        this method is used to decode text from latin1 to utf-8

        :param text: latin1 text
        :return: utf-8 text
        """
        return text.encode('latin1').decode('utf-8')

    def translate_text(self, text):
        """
        this method is used to translate text from china to russian text

        :param text: china text
        :return: russian text
        """
        return self.translator.translate(text, dest='ru').text

    def get_category(self):
        """
        this method is used to get category information

        this method get china category name and save it to self.category
        but firstly the name is filtered by length and translated to russian text

        then save it to self.category
        such as 'russian name': 'china name'
        :return:
        """

        logger.info('get category')
        html = requests.get('https://www.1688.com')
        soup = BeautifulSoup(html.text, 'html.parser')
        categories = soup.find(class_='home-category').find_all('a')

        logger.info('save category')
        for category in categories:
            self.category[self.translate_text(self.decode_text(category.text))[0:29]] = self.decode_text(category.text)

    async def get_products_list(self, category_name: str, max_price: int = None, min_price: int = None):
        """
        this method is used to get product list from tm api

        :param category_name: category name from self.category in russian text
        :param max_price: data is filtered by max price
        :param min_price: data is filtered by min price
        :return: product list with dicts (title, price, and url)
        """

        logger.info('prepare params')
        params = {'apiToken': self.api_key,
                  'page': 1,
                  'page_size': 20,
                  'keyword': self.category[category_name],
                  'sort': 'default',
                  'price_start': min_price,
                  'price_end': max_price}

        logger.info('get products list')
        result = requests.get('http://api.tmapi.top/1688/search/items', params=params).json()

        product_list = [{
            'title': self.translate_text(product['title']),
            'price': product['price'],
            'url': product['product_url']
        } for product in result['data']['items']]
        return product_list

    async def get_product_details(self, link):
        """
        this method is used to get product details from tm api

        :param link: product link
        :return: dict (name: 'product name',
                       price: 'price',
                       url: 'url')
        """
        logger.info('prepare params')
        querystring = {"apiToken": self.api_key}
        payload = {"url": link}

        logger.info('get product details')
        response = requests.post("http://api.tmapi.top/1688/v2/item_detail_by_url",
                                 json=payload,
                                 params=querystring).json()

        if not response['data'] is None:
            product_info = {
                'name': self.translate_text(response['data']['title']),
                'price': response['data']['sku_price_scale'],
                'category_id': response["data"]["category_id"]
            }
            return product_info

        return None
