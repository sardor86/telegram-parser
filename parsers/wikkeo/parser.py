import logging

from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By

from .driver import BaseDriver

logger = logging.getLogger(__name__)


class WikkeoParser(BaseDriver):
    """
    Wikkeo parser
    this class is used for getting information from Wikkeo site
    this class can parse category and save it to self.category, get products list, and product details
    """
    def __init__(self):
        """
        method init prepare chrome driver
        """
        super(WikkeoParser, self).__init__()
        self.category = {}

    def get_category(self):
        """
        method get_category visits to https://wikkeo.com/ and wait when site is done
        then this method click to button with class header-category__button after that
        this method looking for all categories and save them to self.category such as 'category name': 'url'
        :return: category dict ('category name': 'url')
        """

        logger.info('driver is visiting to https://wikkeo.com/')
        self.get('https://wikkeo.com/')
        self.driver_sleep(10, 'header-category__button')

        logger.info('click to the button with class header-category__button')
        self.find_element(By.CLASS_NAME, 'header-category__button').click()

        logger.info('get categories')
        for category in self.find_elements(By.CLASS_NAME, 'categories-block__general-item'):
            self.category[category.text[0:29]] = category.find_element(By.TAG_NAME, 'a').get_attribute('href')

        return self.category

    async def get_products_list(self, category: str, min_price: int = 0, max_price: int = 99999999):
        """
        this method visit to site with category and another filters for example
        https://wikkeo.com/category/electric?min_price=25&max_price=131000

        :param category: category name from self.category dict
        :param min_price: min price of product
        :param max_price: max price of product
        :return: list of dict with product details(url, name, price)
        """

        logger.info('driver is visiting to {self.category[category]}?min_price={min_price}&max_price={max_price}')
        self.get(f'{self.category[category]}?min_price={min_price}&max_price={max_price}')
        self.driver_sleep(5, 'product-list-block-list-item')

        products = []

        for product in self.find_elements(By.CLASS_NAME, 'product-list-block-list-item'):
            products.append({
                'url': product.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                'name': product.find_element(By.CLASS_NAME, 'product-list-block-list-item_'
                                                            '_info-name-block-text').text,
                'price': product.find_element(By.CLASS_NAME, 'product-list-block-list-item_'
                                                             '_info-additional-price-current').text
            })

        return products

    async def get_product_details(self, url):
        """
        this method visit to url and collect product details
        if this method cannot find product, You will get None
        :param url: url of product
        :return: dict with product details(name, price, description)
        """
        try:
            logger.info(f'driver is visiting to {url}')
            self.get(url)
            self.driver_sleep(5, 'product-header-info__title')
            try:
                price = self.find_element(By.CLASS_NAME, 'product-selection__option-list-state-price')
            except NoSuchElementException:
                try:
                    price = self.find_element(By.CLASS_NAME, 'product-selection__option-list-item-discount-price')
                except NoSuchElementException:
                    price = self.find_element(By.CLASS_NAME, 'product-selection_'
                                                             '_option-list-sum-price-list-item-info-value')
            product_detail = {
                'name': self.find_element(By.CLASS_NAME, 'product-header-info__title').text,
                'price': price.text,
                'description': self.find_element(By.CLASS_NAME, 'description__value').text
            }

            return product_detail
        except (InvalidArgumentException, NoSuchElementException):
            return None
