from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, 'username')
    PASSWORD_INPUT = (By.ID, 'password')
    LOGIN_BUTTON = (By.ID, 'login_button')

    def enter_username(self, username):
        username_input = self.element(*self.USERNAME_INPUT)
        username_input.send_keys(username)

    def enter_password(self, password):
        password_input = self.driver.find_element(*self.PASSWORD_INPUT)
        password_input.send_keys(password)

    def click_login_button(self):
        login_button = self.driver.find_element(*self.LOGIN_BUTTON)
        login_button.click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
