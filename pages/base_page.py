import sys
import os
import time
import requests
import allure
import ddddocr

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import Logger
from config.pathconf import PROPER_SCREEN_DIR


class BasePage:
    # 创建定位方式到 By 类属性的映射
    _locator_mapping = {
        'id': By.ID,
        'name': By.NAME,
        'class': By.CLASS_NAME,
        'lt': By.LINK_TEXT,
        'xpath': By.XPATH,
        'tag': By.TAG_NAME,
        'css': By.CSS_SELECTOR,
        'plt': By.PARTIAL_LINK_TEXT,
    }

    def __init__(self, driver):
        self.driver = driver

    def element(self, _type, locate):
        """
        定位单个元素,只会查找页面中符合条件的第一个节点,并返回
        该方法返回基于指定查询条件的webElement对象，或抛出不符合条件的异常
        :param _type: 定位方式
        :param locate: 定位语句
        :return: 元素对象
        """
        by_type = self._locator_mapping.get(_type.lower())
        if by_type is None:
            supported_locator = ', '.join(self._locator_mapping.keys())
            message = f"定位方式（{_type}）错误, 支持的定位方式：({supported_locator})"
            Logger.error(message)
            raise ValueError(message)
        try:
            return self.driver.find_element(by_type, locate)
        except Exception as e:
            message = f"定位失败，请检查定位方式（{_type}）和表达式（{locate}）是否准确, 错误信息：({e})"
            Logger.error(message)
            raise ValueError(message) from e

    def elements(self, _type, locate):
        """
        定位多个元素,返回一个列表,列表里的元素全是WebElement节点对象
        该方法返回指定查询条件的WebElement的对象集合，或返回空列表
        :param _type: 定位方式
        :param locate: 定位语句
        :return: 元素对象
        """
        by_type = self._locator_mapping.get(_type.lower())
        if by_type is None:
            supported_locator = ', '.join(self._locator_mapping.keys())
            message = f"定位方式（{_type}）错误, 支持的定位方式：({supported_locator})"
            Logger.error(message)
            raise ValueError(message)
        return self.driver.find_elements(by_type, locate)

    def element_wait(self, _type, locate, wait=5):  # 等待
        """
        显示等待定位,在设置时间内，默认每隔一段时间检测一次当前页面元素是否存在，如果超过设置时间检测不到则抛出异常。
        :param _type: 定位方式
        :param locate: 定位语句
        :param wait: 等待时间,默认以秒为单位
        :return: None
        """
        by_type = self._locator_mapping.get(_type.lower())
        if by_type is None:
            supported_locator = ', '.join(self._locator_mapping.keys())
            message = f"定位方式（{_type}）错误, 支持的定位方式：({supported_locator})"
            Logger.error(message)
            raise ValueError(message)
        try:
            WebDriverWait(self.driver, wait, 1).until(EC.presence_of_element_located((by_type, locate)))
        except Exception as e:
            message = f"等待元素时发生错误，定位方式：({_type}), 定位表达式：({locate}), 错误信息：({e})"
            Logger.error(message)
            raise ValueError(message) from e

    @staticmethod
    def is_valid_address(url: str) -> bool:
        """
        判断url地址是否可以正常请求
        :param url: 请求地址
        :return: True or False
        """
        try:
            rep = requests.get(url, timeout=5)  # 默认设置5秒超时
            code = rep.status_code
            return code == 200
        except Exception as e:
            message = f'请求地址（{url}）异常: ({e})'
            Logger.error(message)
            return False

    @staticmethod
    def sleep(s: float):
        """
        休眠指定的秒数。参数 s 必须是非负数值类型（整数或浮点数）。
        :param s: 休眠时间（秒），必须是非负数值。
        :return: None
        """
        if not isinstance(s, (int, float)) or s < 0:
            message = f"休眠时间必须是非负数值，请检查输入：({s})"
            Logger.error(message)
            raise ValueError(message)
        Logger.debug(f'等待{s}秒')
        time.sleep(s)

    def open(self, url):
        """
        打开浏览器
        :param url: 网页地址
        :return: None
        """
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        try:
            self.driver.get(url)
            Logger.debug(f'打开网页: ({url})')
        except Exception as e:
            message = f'无法打开网页 {url}: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def set_max_window(self):
        """
        最大化浏览器
        :return: None
        """
        try:
            self.driver.maximize_window()
            Logger.debug('开启网页最大化')
        except Exception as e:
            message = f'无法使网页最大化: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def set_win_size(self, wide, high):
        """
        设置窗口
        :param wide: 宽
        :param high: 高
        :return:
        """
        try:
            self.driver.set_window_size(wide, high)
            Logger.debug(f'设置窗孔大小：宽({wide})高({high})')
        except Exception as e:
            message = f'无法设置窗口大小: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def send_key(self, _type, locate, text):
        """
        输入文本
        :param _type: 定位方式
        :param locate: 定位语句
        :param text: 输入内容
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            e1 = self.element(_type, locate)
            e1.clear()
            e1.send_keys(text)
            Logger.debug(f'向元素 {_type}={locate} 输入文字：{text}')
        except Exception as e:
            message = f'无法在元素 {_type}={locate} 输入文字 {text}: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    @staticmethod
    def upload_files(filepath, sleep=1):
        """
        文件上传
        :param filepath: 文件路径 路径必须要输入正确 函数没办法判断是否成功
        :param sleep: 等待window 窗口时间 默认 1 秒
        :return: None
        """
        try:
            if sys.platform.lower() == 'win32':
                import pyautogui
                import pyperclip
                pyperclip.copy(filepath)
                time.sleep(sleep)
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(sleep)
                pyautogui.press('enter', presses=2)
                Logger.debug(f'上传文件路径：{filepath}')
        except Exception as e:
            message = f'文件上传失败：{filepath} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def clear(self, _type, locate):
        """
        清除元素中的内容
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            self.element(_type, locate).clear()
            Logger.debug(f'清空元素 {_type}={locate} 的内容')
        except Exception as e:
            message = f'无法清空元素 {_type}={locate} 的内容: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def enter(self, _type, locate):
        """
        在元素上按回车键
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            self.element(_type, locate).send_keys(Keys.ENTER)
            Logger.debug(f'在元素 {_type}={locate} 上按回车键')
        except Exception as e:
            message = f'无法在元素 {_type}={locate} 上按回车键: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def click(self, _type, locator):
        """
        在元素上单击
        :param _type: 定位方式
        :param locator: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locator)
            self.element(_type, locator).click()
            Logger.debug(f'点击元素 {_type}={locator}')
        except Exception as e:
            message = f'点击元素 {_type}={locator} 执行失败: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def right_click(self, _type, locate):
        """
        右击
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            e1 = self.element(_type, locate)
            ActionChains(self.driver).context_click(e1).perform()
            Logger.debug(f'在元素 {_type}={locate} 上右击')
        except Exception as e:
            message = f'无法在元素 {_type}={locate} 上右击: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def double_click(self, _type, locate):
        """
        双击
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            e1 = self.element(_type, locate)
            ActionChains(self.driver).double_click(e1).perform()
            Logger.debug(f'在元素 {_type}={locate} 上双击')
        except Exception as e:
            message = f'无法在元素 {_type}={locate} 上双击: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def move_element(self, _type, locate):
        """
        移动鼠标到目标位置
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            e1 = self.element(_type, locate)
            ActionChains(self.driver).move_to_element(e1).perform()
            Logger.debug(f'鼠标移动到元素 {_type}={locate}')
        except Exception as e:
            message = f'无法将鼠标移动到元素 {_type}={locate}: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def move_offset_click(self, x_coordinate, y_coordinate, left_click=True):
        """
        移动鼠标到指定坐标然后点击
        :param x_coordinate: x坐标
        :param y_coordinate: y坐标
        :param left_click: bool 左键(True)或right(False)点击，不填默认左键
        :return: None
        """
        try:
            action = ActionChains(self.driver).move_by_offset(x_coordinate, y_coordinate)
            action.click() if left_click else action.context_click()
            action.perform()
            button = 'left' if left_click else 'right'
            Logger.debug(f'{button}点击坐标 ({x_coordinate}, {y_coordinate})')
        except Exception as e:
            message = f'无法点击坐标 ({x_coordinate}, {y_coordinate}): ({e})'
            Logger.error(message)
            raise ValueError(message) from e
        finally:
            ActionChains(self.driver).move_by_offset(-x_coordinate, -y_coordinate).perform()

    def drag_and_drop(self, _type1, e1, _type2, e2):
        """
        拖动一个元素到另一个元素位置
        :param _type1: 定位方式
        :param e1: 要拖动元素的定位
        :param _type2: 定位方式
        :param e2: 目标位置元素的定位
        :return: None
        """
        try:
            source_element = self.element_wait(_type1, e1) and self.element(_type1, e1)
            target_element = self.element_wait(_type2, e2) and self.element(_type2, e2)
            ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()
            Logger.debug(f'将元素 {_type1}={e1} 拖动到元素 {_type2}={e2}')
        except Exception as e:
            message = f'无法将元素 {_type1}={e1} 拖动到元素 {_type2}={e2}: ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def click_text(self, text):
        """
        点击文字
        :param text: 文字
        :return: None
        """
        try:
            self.element("lt", text).click()
            Logger.debug(f'点击链接：{text}')
        except Exception as e:
            message = f'无法点击链接：{text} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def close(self):
        """
        关闭当前页面
        :return: None
        """
        try:
            self.driver.close()
            Logger.debug('关闭当前页面')
        except Exception as e:
            message = f'无法关闭当前页面 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def quit(self):
        """
        关闭所有页面
        :return: None
        """
        try:
            self.driver.quit()
            Logger.debug('关闭所有页面')
        except Exception as e:
            message = f'无法关闭所有页面 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def f5(self):
        """
        刷新
        :return: None
        """
        try:
            self.driver.refresh()
            Logger.debug('刷新页面')
        except Exception as e:
            message = f'无法刷新页面 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def back(self):
        """
        页面后退
        :return: None
        """
        try:
            self.driver.back()
            Logger.debug('页面后退')
        except Exception as e:
            message = f'无法后退页面 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def forward(self):
        """
        页面向前
        :return: None
        """
        try:
            self.driver.forward()
            Logger.debug('页面向前')
        except Exception as e:
            message = f'无法向前页面 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def scroll_top(self):
        """
        滚动至顶部
        :return: None
        """
        try:
            self.js("window.scrollTo(document.body.scrollHeight,0)")
            Logger.debug('滚动至顶部')
        except Exception as e:
            message = f'无法滚动至顶部 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def scroll_bottom(self):
        """
        滚动至底部
        :return: None
        """
        try:
            self.js("window.scrollTo(0,document.body.scrollHeight)")
            Logger.debug('滚动至底部')
        except Exception as e:
            message = f'无法滚动至底部 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def js(self, script):
        """
        执行js
        :param script: js
        :return: None
        """
        try:
            self.driver.execute_script(script)
            Logger.debug(f'执行JS语句：{script}')
        except Exception as e:
            message = f'执行JS语句失败：{script} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def get_attribute(self, _type, locate, attribute):
        """
        获取元素属性的值
        :param _type: 定位方式
        :param locate: 定位语句
        :param attribute: 属性名
        :return: 属性值
        """
        try:
            self.element_wait(_type, locate)
            value = self.element(_type, locate).get_attribute(attribute)
            Logger.debug(f'获取元素 {_type}={locate} 的属性 {attribute} 值为：{value}')
            return value
        except Exception as e:
            message = f'获取元素 {_type}={locate} 的属性 {attribute} 值失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def get_ele_text(self, _type, locate):
        """
        返回元素的文本
        :param _type: 定位方式
        :param locate: 定位语句
        :return: 元素的文本
        """
        try:
            text = self.element(_type, locate).text
            Logger.debug(f'获取元素 {_type}={locate} 的文本为：{text}')
            return text
        except Exception as e:
            message = f'获取元素 {_type}={locate} 的文本失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def get_title(self):
        """
        获取title
        :return: 页面标题
        """
        title = self.driver.title
        Logger.debug(f'获取页面标题：{title}')
        return title

    def get_screen(self, doc, img_report=True):
        """
        截取当前界面图片
        :param doc: str 名称
        :param img_report: bool 图片追加到测试报告 默认添加到报告
        :return: 截图文件路径
        """
        try:
            filename = doc + "_" + str(round(time.time() * 1000)) + ".png"
            if len(filename) >= 200:
                filename = str(round(time.time() * 1000)) + ".png"
            filepath = os.path.join(PROPER_SCREEN_DIR, filename)

            self.driver.save_screenshot(filepath)
            if img_report:
                allure.attach.file(filepath, name=filename, attachment_type=allure.attachment_type.PNG)
            Logger.debug(f"截图成功已经存储在: {filepath}")
            return filepath
        except Exception as e:
            message = f'截取当前界面图片失败：{doc} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def alert_accept(self):
        """
        alert点确认
        :return: None
        """
        try:
            self.driver.switch_to.alert.accept()
            Logger.debug('点击弹框确认')
        except Exception as e:
            message = '点击弹框确认失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def alert_dismiss(self):
        """
        alert点取消
        :return: None
        """
        try:
            self.driver.switch_to.alert.dismiss()
            Logger.debug('点击弹框取消')
        except Exception as e:
            message = '点击弹框取消失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def switch_to_frame(self, _type, locate):
        """
        进入frame
        :param _type: 定位方式
        :param locate: 定位语句
        :return: None
        """
        try:
            self.element_wait(_type, locate)
            frame_element = self.element(_type, locate)
            self.driver.switch_to.frame(frame_element)
            Logger.debug(f'进入frame：{_type}={locate}')
        except Exception as e:
            message = f'进入frame失败：{_type}={locate} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def switch_to_default_content(self):
        """
        跳出frame
        :return: None
        """
        try:
            self.driver.switch_to.default_content()
            Logger.debug("跳出frame")
        except Exception as e:
            message = '跳出frame失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def get_selected(self, _type, locate, value_index, index=None):
        """
        通过index获取我们selected，然后选择我们selected
        :param _type: 定位方式
        :param locate: 定位语句
        :param value_index: 选择项的索引
        :param index: 如果是多个元素，指定元素的索引
        :return: None
        """
        try:
            selected_element = self.elements(_type, locate)[index] if index is not None else self.element(_type, locate)
            Select(selected_element).select_by_index(value_index)
            Logger.debug(f'选择元素 {_type}={locate} 的选项索引 {value_index}')
        except Exception as e:
            message = f'选择元素 {_type}={locate} 的选项索引 {value_index} 失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def high_light(self, _type, locate, style="background: yellow; border: 2px solid red;"):
        """
        高亮显示选中元素
        :param _type: 定位方式
        :param locate: 定位语句
        :param style: 应用于元素的样式
        :return: None
        """
        try:
            element = self.element(_type, locate)
            self.driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, style)
            Logger.debug(f'高亮显示元素 {_type}={locate}')
        except Exception as e:
            message = f'高亮显示元素 {_type}={locate} 失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def save_as_img(self, _type, locate, filename, sleep=1):
        """
        图片另存为  下载文件也可以直接使用
        :param _type: 定位类型
        :param locate: 定位器
        :param filename: 图片名称 路径必须要输入正确 因为函数没办法判断是否成功
        :param sleep: 等待窗口时间 默认 1 秒
        :return: str path 文件路径
        """
        try:
            if sys.platform.lower() == 'win32':
                import pyautogui
                import pyperclip
                # 右键点击
                self.right_click(_type, locate)
                # 图片另存为
                pyautogui.typewrite(['V'])

                # 将地址以及文件名复制
                pic_dir = os.path.join(PROPER_SCREEN_DIR, f'{filename}.jpg')
                pyperclip.copy(pic_dir)
                # 等待窗口打开
                time.sleep(sleep)

                # 粘贴
                pyautogui.hotkey('ctrl', 'v')
                # 保存
                pyautogui.press('enter')
                # 如果询问是否覆盖，选择"是"
                pyautogui.typewrite("y")

                time.sleep(2)
                Logger.debug(f'图片路径为{pic_dir}')
                return pic_dir
            else:
                Logger.error('图片另存为功能仅支持Windows平台')
                return None
        except Exception as e:
            message = f'图片另存为失败：{filename} ({e})'
            Logger.error(message)
            raise ValueError(message) from e

    def get_capt(self, _type, locate, filename):
        """
        使用OCR获取验证码
        :param _type: 定位类型
        :param locate: 定位器
        :param filename: 图片名称
        :return: 识别的文本
        """
        try:
            ocr = ddddocr.DdddOcr()
            with open(self.save_as_img(_type, locate, filename), 'rb') as f:
                image = f.read()
            res = ocr.classification(image)
            r = res.lower()
            Logger.debug(f"验证码: {r}")
            return r
        except Exception as e:
            message = f'获取验证码失败 ({e})'
            Logger.error(message)
            raise ValueError(message) from e
