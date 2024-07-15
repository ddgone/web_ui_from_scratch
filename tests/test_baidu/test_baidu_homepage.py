import allure
import pytest


@allure.epic("web平台")  # 侧边栏、web后台等
@allure.feature("百度首页")  # 测试用例模块名
@allure.story("平台需求-首页搜索自动跳转")  # 需求名字
class TestBaidu:
    @allure.title("输入正确的内容进行搜索")  # 测试用例名
    @allure.description('输入正确的内容，可以成功进行搜索并且自动跳转')  # 测试用例描述
    @allure.tag('冒烟测试')
    @allure.testcase('', 'test case')  # 测试用例case文档链接及其文档名
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("data", load_yaml)
    def test_baidu_search(self, base, baidu_homepage):
        with allure.step("打开百度首页"):
            base.set_max_window()
            base.open("https://www.baidu.com")

        with allure.step("输入内容"):
            keyword = '今天天气真好'
            baidu_homepage.input_search_query(keyword)

        with allure.step("点击搜索按钮"):
            baidu_homepage.click_search_button()

        with allure.step("断言检查网页title"):
            base.sleep(2)
            title = base.get_title()
            assert keyword in title, f"Expected {keyword} in title, but got '{title}'"

    @allure.title("点击下一个")  # 测试用例名
    @allure.description('点击下一个，打开链接')  # 测试用例描述
    @allure.tag('冒烟测试')
    @allure.testcase('', 'test case')  # 测试用例case文档链接及其文档名
    @allure.severity(allure.severity_level.NORMAL)
    def test_click_next_page(self, base, baidu_homepage):
        with allure.step("点击下一步"):
            base.click("css", ".s-tab-item.s-tab-item_1CwH-.s-tab-video_1Sf_u.s-tab-video")
