from parsers.aliexpress.driver import BaseDriver

from selenium.webdriver.common.by import By
from selenium.common import InvalidArgumentException, NoSuchElementException


class AliexpressParser(BaseDriver):
    def __init__(self):
        super().__init__()
        self.category: dict = {}
        self.base_url = 'https://aliexpress.ru/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/111.0.0.0 Safari/537.36'}

    def get_category(self):
        self.get(self.base_url)

        self.driver_sleep(100, 'RedHeaderNavigationItem_RedHeaderNavigationItem_'
                          '_root__91jxr')
        self.find_element(By.CLASS_NAME, 'RedHeaderNavigationItem_RedHeaderNavigationItem_'
                          '_root__91jxr').click()

        category_list = self.find_element(By.CLASS_NAME,
                                          'RedHeaderCatalogPopup_RedHeaderCatalogPopup_'
                                          '_categories__484gh')
        for category in category_list.find_elements(By.TAG_NAME, 'a'):
            self.category[category.text[0:29]] = category.get_attribute('href')
        return self.category

    async def get_products_list(self, category: str, min_price: int = None, max_price: int = None) -> list:
        products_list = []
        self.get(f'{self.category[category]}&minPrice={min_price}&maxPrice={max_price}')

        try:
            self.driver_sleep(5, 'snow-ali-kit_Button-Secondary__button__4468ot')
            self.find_elements(By.CLASS_NAME, 'snow-ali-kit_Button-Secondary__button__4468ot')[-1].click()
        except IndexError:
            pass

        self.driver_sleep(5, 'product-snippet_ProductSnippet__container__1r2its')

        for product in self.find_elements(By.CLASS_NAME, 'product-snippet_ProductSnippet__container__1r2its'):
            product_description = product.find_element(By.CLASS_NAME, 'product-snippet_ProductSnippet_'
                                                                      '_description__1r2its')
            products_list.append({
                'link': product_description.find_element(By.TAG_NAME, 'a').get_attribute('href'),
                'name': product.find_element(By.CLASS_NAME, 'product-snippet_ProductSnippet__name__1r2its').text,
                'price': product.find_element(By.CLASS_NAME, 'snow-price_SnowPrice__blockMain__1cmks6').text
            })
        return products_list

    async def get_product_details(self, link: str):
        try:
            self.get(link)
            self.driver_sleep(5, 'HazeProductDescription_HazeProductDescription__root__8s9ws')
            product_name = self.find_element(By.XPATH, '/html/body/div[2]/div/div[9]/div/div[1]/'
                                                       'div/div/div[2]/h1')
            product_price = self.find_element(By.XPATH, '/html/body/div[2]/div/div[9]/div/div[4]/'
                                                        'div/div[1]/div[1]/div/div[2]/div[2]')
            category = self.find_element(By.XPATH,
                                         '/html/body/div[2]/div/div[8]').find_elements(By.TAG_NAME, 'li')[-1]

            return {
                'name': product_name.text,
                'price': product_price.text,
                'category': category.text
            }
        except (InvalidArgumentException, NoSuchElementException):
            return None
