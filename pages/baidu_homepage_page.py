from pages.base_page import BasePage
from utils.logger import Logger


class BaiduHomePage:
    SEARCH_BOX = ('css', '#kw')
    SEARCH_BUTTON = ('css', '#su')

    def __init__(self, driver):
        self.base = BasePage(driver)

    def input_search_query(self, text):
        self.base.send_key(*self.SEARCH_BOX, text)
        Logger.debug(f'向搜索输入框中输入: {text}')

    def click_search_button(self):
        self.base.click(*self.SEARCH_BUTTON)
        Logger.debug("点击搜索按钮")
