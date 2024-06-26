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
@pytest.fixture(scope="session")
def driver(request):
    driver_instance = WebDriverFactory.get_driver(BROWSER_NAME)
    Logger.debug("打开浏览器")
    yield driver_instance
    driver_instance.quit()
    Logger.debug("浏览器被关闭")


@pytest.fixture(scope="session")
def base(driver):
    return BasePage(driver)


@pytest.fixture(scope="session")
def baidu_homepage(driver):
    return BaiduHomePage(driver)
