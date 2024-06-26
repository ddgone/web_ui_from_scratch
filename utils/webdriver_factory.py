import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from config.pathconf import (
    LINUX_CHROME_PATH, LINUX_FIREFOX_PATH,
    WIN_CHROME_PATH, WIN_FIREFOX_PATH, WIN_EDGE_PATH,
    MAC_CHROME_PATH, MAC_FIREFOX_PATH, MAC_SAFARI_PATH,
)
from utils.logger import Logger


class WebDriverFactory:
    # 创建浏览器名称到 WebDriver 服务的映射
    _service_map = {
        'win32': {
            'edge': (webdriver.Edge, EdgeService(WIN_EDGE_PATH)),
            'chrome': (webdriver.Chrome, ChromeService(WIN_CHROME_PATH)),
            'firefox': (webdriver.Firefox, FirefoxService(WIN_FIREFOX_PATH)),
        },
        'linux': {
            'chrome': (webdriver.Chrome, ChromeService(LINUX_CHROME_PATH)),
            'firefox': (webdriver.Firefox, FirefoxService(LINUX_FIREFOX_PATH)),
        },
        'darwin': {
            'chrome': (webdriver.Chrome, ChromeService(MAC_CHROME_PATH)),
            'firefox': (webdriver.Firefox, FirefoxService(MAC_FIREFOX_PATH)),
            'safari': (webdriver.Safari, SafariService(MAC_SAFARI_PATH)),
        },
    }

    @staticmethod
    def get_driver(browser_name):
        current_sys = sys.platform.lower()
        browser_name = browser_name.lower()

        try:
            # 获取当前系统的浏览器服务映射
            browser_services = WebDriverFactory._service_map.get(current_sys)
            if browser_services is None:
                message = f"不支持的操作系统: {current_sys}"
                Logger.error(message)
                raise EnvironmentError(message)

            # 获取浏览器服务
            browser_service = browser_services.get(browser_name)
            if browser_service is None:
                supported_browsers = ", ".join(browser_services.keys())
                message = f"不支持的浏览器: {browser_name}. 支持的浏览器: {supported_browsers}"
                Logger.error(message)
                raise ValueError(message)

            # 创建 WebDriver 实例
            driver_class, service = browser_service
            return driver_class(service=service)

        except Exception as e:
            Logger.error(f"创建 WebDriver 时发生错误: {e}")
            raise ValueError("创建 WebDriver 时发生错误。请检查浏览器驱动是否正确安装。") from e
