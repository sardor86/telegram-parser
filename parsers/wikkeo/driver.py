from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BaseDriver(webdriver.Chrome):
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("user-agent=Mozilla/5.0 "
                                    "(Windows NT 10.0; Win64; x64) "
                                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        super().__init__(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.set_window_size(1924, 1080)

    def driver_sleep(self, time: int, class_name: str) -> bool:
        try:
            wait = WebDriverWait(self, time)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return True
        except TimeoutException:
            return False