from selenium.common.exceptions import NoSuchElementException, InvalidArgumentException
from selenium.webdriver.common.by import By

from .driver import BaseDriver


class WikkeoParser(BaseDriver):
    def __init__(self):
        super(WikkeoParser, self).__init__()
        self.category = {}

    def get_category(self):
        self.get('https://wikkeo.com/')
        self.driver_sleep(10, 'header-category__button')
        self.find_element(By.CLASS_NAME, 'header-category__button').click()
        for category in self.find_elements(By.CLASS_NAME, 'categories-block__general-item'):
            self.category[category.text] = category.find_element(By.TAG_NAME, 'a').get_attribute('href')

        return self.category

    def get_products_list(self, category: str):
        self.get(self.category[category])
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

    def get_product_details(self, url):
        try:
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
