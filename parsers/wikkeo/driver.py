import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


class BaseDriver(webdriver.Chrome):
    """
    Base driver class is used for browsing the web pages.
    """
    def __init__(self):
        """
        method init is used for installing chrome driver and prepare it for browsing the web pages.
        """
        logger.info("Initializing driver...")

        logger.info('set chrome options')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent=Mozilla/5.0 "
                                    "(Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--no-sandbox')

        logger.info('initialize chrome driver and set window size ')
        super().__init__(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.set_window_size(1920, 1080)

    def driver_sleep(self, time: int, class_name: str) -> bool:
        """
        method driver_sleep is used for wait when the block element is visible.

        :param time: time in seconds.
        :param class_name: class name of the block element.
        :return: will return True, if the driver can find the block, or
        will return False, if the driver cannot find the block.
        """
        try:
            logger.info(f'driver sleep for {class_name}')
            wait = WebDriverWait(self, time)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            logger.info('driver can find element')
            return True
        except TimeoutException:
            logger.warning('driver_sleep timed out')
            return False
