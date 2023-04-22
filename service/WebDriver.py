from selenium import webdriver
from selenium.webdriver.support.ui import Select
import Environment
from selenium.webdriver.chrome.service import Service


class WebDriver:
    def __init__(self):
        self._c_service = None
        self._driver = None
        self._option = None
        self.period = ''
        self.draw_day = ''
        self.common_num = []
        self.special_num = ''
        self.fetch_draw_info = []
        self.ip = ''

    def do_init(self):
        chrome_path = Environment.CHROME_DRIVER
        self._c_service = Service(chrome_path)
        self._c_service.command_line_args()
        self._c_service.start()
        self._option = webdriver.ChromeOptions()
        # self._option.add_argument('--headless')
        # self._option.add_argument('--disable-gpu')
        self._option.add_argument('--no-sandbox')
        self._option.add_argument("--disable-extensions")
        # self._option.add_argument(f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36'
        #                           f' (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
        if self.ip:
            self._option.add_argument('--proxy-server=%s' % self.ip)
        if chrome_path:
            self._driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=self._option)
        else:
            self._driver = webdriver.Chrome(chrome_options=self._option)
        self._driver.set_page_load_timeout(time_to_wait=Environment.SELENIUM_TIME_OUT)

    def selector(self, ele_select):
        selector = Select(ele_select)
        return selector

    def do_bot_close(self):
        self._driver.quit()
        self._c_service.stop()

    @property
    def driver(self):
        return self._driver

    @property
    def option(self):
        return self._option
