import pytest
from config.pathconf import BROWSER_NAME
from utils.webdriver_factory import WebDriverFactory
from utils.logger import Logger
from pages.base_page import BasePage
from pages.baidu_homepage_page import BaiduHomePage


@pytest.fixture(autouse=True)
def log_test_rerun(request):
    # 当前测试的相关信息
    node_id = request.node.nodeid
    # 当前重试次数
    rerun = getattr(request.node, "execution_count", 1)
    # 在测试开始时记录日志
    if rerun == 1:
        Logger.info(f"开始执行测试：{node_id}")
    else:
        Logger.warning(f"重试测试（第{rerun - 1}次）：{node_id}")


# 由于使用了pytest-rerunfailures的重试机制，所用域目前仅支持function和session
@pytest.fixture(scope="function")
def driver(request):
    driver_instance = WebDriverFactory.get_driver(BROWSER_NAME)
    Logger.debug("打开浏览器")
    yield driver_instance
    driver_instance.quit()
    Logger.debug("浏览器被关闭")


@pytest.fixture(scope="class")
def base(driver):
    return BasePage(driver)


@pytest.fixture(scope="function")
def baidu_homepage(driver):
    return BaiduHomePage(driver)


# TODO 分离建立干净driver实例和开启关闭浏览器的作用域
'''
@pytest.fixture(scope='class')
def browser_class_scope():
    # 这个 fixture 负责启动和关闭浏览器
    print("启动浏览器")
    driver_instance = WebDriverFactory.get_driver(BROWSER_NAME)
    yield driver_instance
    print("关闭浏览器")
    driver_instance.quit()

@pytest.fixture(scope='function')
def driver(browser_class_scope):
    # 这个 fixture 负责为每个测试函数提供一个干净的 driver 实例
    # 在运行每个测试之前，重置浏览器状态
    browser_class_scope.delete_all_cookies()
    browser_class_scope.execute_script("window.localStorage.clear();")
    browser_class_scope.execute_script("window.sessionStorage.clear();")
    # 可以添加其他的状态重置代码，如导航到一个空白页等
    browser_class_scope.get("about:blank")
    yield browser_class_scope
    # 如果需要，可以在这里添加每个测试后的清理代码
'''
