import unittest
from time import sleep

from appium import webdriver
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.interaction import POINTER_TOUCH
from selenium.webdriver.common.actions.pointer_input import PointerInput

capabilities = {
    'platformName': 'Android',
    'automationName': 'uiautomator2',
    'deviceName': 'Android',
    'appPackage': 'com.google.android.documentsui',
    'appActivity': 'com.android.documentsui.ViewDownloadsActivity',
    'language': 'en',
    'locale': 'US'
}

APPIUM_SERVER_URL = 'http://hub.home:4723'


class TestAppium(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = webdriver.Remote(APPIUM_SERVER_URL,  # type: ignore
                                       options=AppiumOptions().load_capabilities(capabilities))

    def tearDown(self) -> None:
        if self.driver:
            self.driver.quit()

    def test_use_google_lens(self) -> None:
        # //android.widget.TextView[@resource-id="android:id/title"]

        # print display size
        print(self.driver.get_window_size())

        file_button = self.driver.find_element(AppiumBy.XPATH,
                                               '//android.widget.ImageView[@resource-id="com.google.android.documentsui:id/icon_thumb"]')
        file_button.click()

        # //android.widget.ImageView[@content-desc="Lens"]
        sleep(0.3)
        lens_button = self.driver.find_element(AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="Lens"]')
        lens_button.click()

        # scroll up
        print('Scrolling up')
        scroll_menu(self, 'down', 600)

        add_text = self.driver.find_element(AppiumBy.XPATH,
                                            '//android.widget.Button[@content-desc="Add a text query to your search."]')
        add_text.click()

        # class name: android.widget.EditText
        text_input = self.driver.find_element(AppiumBy.CLASS_NAME, 'android.widget.EditText')
        text_input.send_keys('armani')
        self.driver.press_keycode(66)


        # Assume self.driver is already set up
        all_elements = self.driver.find_elements(AppiumBy.XPATH, "//*")
        print(len(all_elements))
        for element in all_elements:
            print(element.text)

        print(self.driver.page_source)


def scroll_menu(self, direction: str = 'up', distance: int = 400) -> None:
    action = ActionChains(self.driver)
    window_size = self.driver.get_window_size()
    x, y = window_size['width'] / 2, window_size['height'] * 0.8
    move_distance = distance if direction == 'down' else -distance

    action.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(POINTER_TOUCH, 'touch'))
    action.w3c_actions.pointer_action.move_to_location(x, y)
    action.w3c_actions.pointer_action.click_and_hold()
    action.w3c_actions.pointer_action.move_to_location(x, y - move_distance)
    action.w3c_actions.pointer_action.release()
    action.w3c_actions.perform()


if __name__ == '__main__':
    unittest.main()
