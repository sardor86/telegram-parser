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
        chrome_options.add_argument('''
        User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:123.0) Gecko/20100101 Firefox/123.0
        Accept: application/font-woff2;q=1.0,application/font-woff;q=0.9,*/*;q=0.8
        Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
        Accept-Encoding: identity
        Origin: https://aliexpress.ru
        Connection: keep-alive
        Referer: https://st.aestatic.net/
        Sec-Fetch-Dest: font
        Sec-Fetch-Mode: cors
        Sec-Fetch-Site: cross-site''')

        super().__init__(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.set_window_size(1920, 1080)

    def driver_sleep(self, time: int, class_name: str) -> bool:
        try:
            wait = WebDriverWait(self, time)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
            return True
        except TimeoutException:
            return False