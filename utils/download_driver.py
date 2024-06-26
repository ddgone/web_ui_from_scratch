import os
import shutil
import platform
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import SessionNotCreatedException

from config.pathconf import (
    WIN_CHROME_PATH, WIN_FIREFOX_PATH, WIN_EDGE_PATH,
    MAC_CHROME_PATH, MAC_FIREFOX_PATH, MAC_SAFARI_PATH,
    LINUX_FIREFOX_PATH, LINUX_CHROME_PATH
)

BROWSER_CONFIG = {
    "chrome": {
        "driver_manager": ChromeDriverManager,
        "service_class": ChromeService,
        "webdriver_class": webdriver.Chrome,
        "paths": {
            "Windows": WIN_CHROME_PATH,
            "Darwin": MAC_CHROME_PATH,
            "Linux": LINUX_CHROME_PATH
        },
        "executable_name": {
            "Windows": "chromedriver.exe",
            "Darwin": "chromedriver",
            "Linux": "chromedriver"
        }
    },
    "firefox": {
        "driver_manager": GeckoDriverManager,
        "service_class": FirefoxService,
        "webdriver_class": webdriver.Firefox,
        "paths": {
            "Windows": WIN_FIREFOX_PATH,
            "Darwin": MAC_FIREFOX_PATH,
            "Linux": LINUX_FIREFOX_PATH
        },
        "executable_name": {
            "Windows": "geckodriver.exe",
            "Darwin": "geckodriver",
            "Linux": "geckodriver"
        }
    },
    "edge": {
        "driver_manager": EdgeChromiumDriverManager,
        "service_class": EdgeService,
        "webdriver_class": webdriver.Edge,
        "paths": {
            "Windows": WIN_EDGE_PATH,
        },
        "executable_name": {
            "Windows": "msedgedriver.exe"
        }
    },
    "safari": {
        "paths": {
            "Darwin": MAC_SAFARI_PATH
        }
    }
}


def download_driver(browser_name, driver_version=None):
    config = BROWSER_CONFIG[browser_name]
    os_name = platform.system()

    if os_name not in config["paths"]:
        print(f"错误: {browser_name} 不支持当前操作系统 {os_name}。")
        return

    driver_manager_cls = config.get("driver_manager")
    if driver_manager_cls:
        driver_manager = driver_manager_cls(version=driver_version) if driver_version else driver_manager_cls()
    else:
        driver_manager = None

    binary_path = config["paths"][os_name]
    executable_name = config["executable_name"][os_name] if "executable_name" in config else None

    if executable_name:
        custom_path = binary_path.replace(executable_name, "").strip("\\/")
        print(f"正在下载 {executable_name} 到: {custom_path}")

    driver = None  # 初始化 driver 变量

    if driver_manager:
        driver_path = driver_manager.install()

        if not executable_name:
            raise ValueError(f"配置中缺少 executable_name 用于 browser: {browser_name} on OS: {os_name}")

        custom_path = binary_path.replace(executable_name, "").strip("\\/")
        if not os.path.exists(custom_path):
            os.makedirs(custom_path, exist_ok=True)

        try:
            shutil.move(driver_path, binary_path)
        except FileNotFoundError as e:
            print(f"移动文件时出错: {e}")

        download_root = os.path.dirname(driver_path)
        if os.path.exists(download_root):
            try:
                shutil.rmtree(download_root)
                print(f"成功删除多余文件: {download_root}")
            except Exception as e:
                print(f"删除多余文件时出错: {e}")

        print(f"已成功下载 {executable_name} 到: {binary_path}")

    if "service_class" in config:
        service = config["service_class"](binary_path)

        try:
            driver = config["webdriver_class"](service=service)
            driver.quit()
            print(f"{browser_name.capitalize()} 浏览器驱动已成功启动")
        except SessionNotCreatedException:
            print(f"错误: 无法启动 {browser_name} 驱动。请确保浏览器已正确安装。")
    else:
        print(f"未配置 {browser_name.capitalize()} 浏览器驱动")


if __name__ == '__main__':
    # 示例，不设置驱动版本，默认下载最新版本，请保证本地浏览器更新到最新版
    download_driver("chrome")
    download_driver("firefox")
    download_driver("edge")
    download_driver("safari")

    # 示例，手动设置驱动版本
    # download_driver("chrome", "114.0.5735.90")
    # download_driver("firefox", "0.29.1")
    # download_driver("edge", "103.0.1264.62")
