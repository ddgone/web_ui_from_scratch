# -*- coding: utf-8 -*-

import os

from selenium.webdriver.chrome.service import Service as Chrome
from selenium.webdriver.firefox.service import Service as Firefox
from selenium.webdriver.edge.service import Service as Edge

"""
配置路径
"""

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUEST_ADDRESS = 'http://39.107.88.21:3300/url/get?userId='
BROWSER_NAME = 'chrome'

# 浏览器驱动参数配置 ######## 可用绝对路径
# LINUX 系统浏览器驱动路劲
LINUX_CHROME_PATH = os.path.join(BASE_DIR, "driver", "linux", "chromedriver")  # linux 谷歌浏览器
LINUX_FIREFOX_PATH = os.path.join(BASE_DIR, "driver", "linux", "geckodriver")  # linux 火狐浏览器

# MAC
MAC_CHROME_PATH = os.path.join(BASE_DIR, "driver", "mac", "chromedriver")  # mac 谷歌浏览器
MAC_FIREFOX_PATH = os.path.join(BASE_DIR, "driver", "mac", "geckodriver")  # mac 火狐浏览器
MAC_SAFARI_PATH = os.path.join(BASE_DIR, "driver", "mac", "safaridriver")  # mac safari浏览器

# WIN
WIN_EDGE_PATH = os.path.join(BASE_DIR, "driver", "windows", "msedgedriver.exe")  # win edge浏览器
WIN_CHROME_PATH = os.path.join(BASE_DIR, "driver", "windows", "chromedriver.exe")  # win 谷歌浏览器
WIN_FIREFOX_PATH = os.path.join(BASE_DIR, "driver", "windows", "geckodriver.exe")  # win 火狐浏览器

# 日志路径----------------------------
LOG_DIR = os.path.join(BASE_DIR, "log")

# 测试用例集路径

CASE_DIR = os.path.join(BASE_DIR, "case", )

# yaml测试用列数据路径
CASE_YAML_DIR = os.path.join(BASE_DIR, "database", "caseYAML", )  # 测试数据
LOCATOR_YAML_DIR = os.path.join(BASE_DIR, "database", "locatorYAML", )  # 定位数据

# 测试文件路径
DATA_FILE = os.path.join(BASE_DIR, "database", "file")

# 测试图片断言路径
DIFF_IMG_PATH = os.path.join(BASE_DIR, "database", "file", "img")

# 测试用例结果目录
PROPER_JSON_DIR = os.path.join(BASE_DIR, "output", "report_json")

# 测试结果报告目录
PROPER_ALLURE_DIR = os.path.join(BASE_DIR, "output", "reports")
MAILE_REPO = os.path.join(BASE_DIR, "output")
# 测试截图目录
PROPER_SCREEN_DIR = os.path.join(BASE_DIR, "output", "report_screen")
