import os
import time
from datetime import date, timedelta

import allure
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.logger_util import get_logger

logger = get_logger(__name__)


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, delay):
        return WebDriverWait(self.driver, delay)

    @allure.step("Verify Text")
    def open_url(self, url):
        logger.info(f"Open url: {url}")
        self.driver.get(url)
        return self

    @allure.step("Verify Text")
    def verify_text(self, locator, message, delay=40):
        logger.debug("Verify text - " + str(locator) + " message: " + str(message))
        try:
            self.wait(delay).until(EC.text_to_be_present_in_element(locator, message))
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException):
            text = self.driver.find_element(*locator).text
            assert text == message, text + "  :  " + message
        return self

    @allure.step("Input Text")
    def input_text(self, locator, data, delay=0, clear=False):
        logger.debug("Input text - " + str(locator) + " data: " + str(data))
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        if clear:
            ele = self.driver.find_element(*locator)
            time.sleep(0.5)
            ele.send_keys(Keys.CONTROL + "a")
            ele.send_keys(Keys.DELETE)
        self.driver.find_element(*locator).send_keys(data)
        return self

    @allure.step("Input Password")
    def input_password(self, locator, data, delay=0, clear=False):
        logger.debug("Input text - " + str(locator))
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        if clear:
            ele = self.driver.find_element(*locator)
            time.sleep(0.5)
            ele.send_keys(Keys.CONTROL + "a")
            ele.send_keys(Keys.DELETE)
        self.driver.find_element(*locator).send_keys(data)
        return self

    @allure.step("Get Text")
    def get_text(self, locator, delay=40):
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        text = self.driver.find_element(*locator).text
        logger.debug("Get text - " + str(locator) + " text: " + str(text))
        return text

    @allure.step("Get Texts")
    def get_texts(self, locator, delay=40):
        txt_list = []
        if delay != 0:
            self.wait_for_elements_visible(locator, delay)
        text = self.driver.find_elements(*locator)
        for i in text:
            logger.debug(i.text)
            txt_list.append(i.text)
        logger.debug("Get text - " + str(locator) + " text: " + str(txt_list))
        return txt_list

    @allure.step("Wait for element visible")
    def wait_for_element_visible(self, locator, delay=30):
        logger.debug("Wait for element visible - " + str(locator) + " delay: " + str(delay))
        self.set_implicitwait(0)
        self.wait(delay).until(EC.visibility_of_element_located(locator))
        self.set_implicitwait_default()
        return self

    @allure.step("Wait for elements visible")
    def wait_for_elements_visible(self, locator, delay=40):
        logger.debug("Wait for elements visible - " + str(locator) + " delay: " + str(delay))
        self.wait(delay).until(EC.visibility_of_all_elements_located(locator))
        return self

    @allure.step("Wait until element not visible")
    def wait_until_element_not_visible(self, locator, delay=40):
        logger.debug("Wait until element not visible - " + str(locator) + " delay: " + str(delay))
        self.set_implicitwait(0)
        self.wait(delay).until(EC.invisibility_of_element_located(locator))
        self.set_implicitwait_default()
        return self

    @allure.step("Wait for element contains text")
    def wait_for_element_contains_text(self, locator, text, delay=40):
        logger.debug("Wait for element contains text - " + str(locator) + " delay: " + str(delay))
        self.wait(delay).until(EC.text_to_be_present_in_element(locator, text))
        return self

    @allure.step("Wait for element presence")
    def wait_for_element_presence(self, locator, delay=40):
        logger.debug("Wait for element presence - " + str(locator) + " delay: " + str(delay))
        self.wait(delay).until(EC.presence_of_element_located(locator))
        return self

    @allure.step("Wait for element until count matches")
    def wait_for_element_count(self, locator, count, delay=40):
        self.set_implicitwait_default()
        logger.debug("Wait for element presence - " + str(locator) + " Count: " + str(count) + " delay: " + str(delay))
        self.set_implicitwait(0)
        self.wait(delay).until(lambda browser: len(browser.find_elements(*locator)) == int(count))
        self.set_implicitwait_default()
        return self

    @allure.step("Wait for element clickable")
    def wait_for_element_clickable(self, locator, delay=40):
        logger.debug("Wait for element clickable - " + str(locator) + " delay: " + str(delay))
        self.wait(delay).until(EC.element_to_be_clickable(locator))
        return self

    @allure.step("Get current date time")
    def get_datetime(self, data, dateformat="%m/%d/%Y"):
        value = int(data[1:])
        operation = data[0]
        if operation == "+":
            return (date.today() + timedelta(days=value)).strftime(dateformat)
        if operation == "-":
            return (date.today() - timedelta(days=value)).strftime(dateformat)
        else:
            return date.today().strftime(dateformat)

    @allure.step("Clear Text")
    def clear_text(self, locator):
        logger.debug("Clear Text - " + str(locator))
        self.driver.find_element(*locator).send_keys(Keys.CONTROL + "a")
        self.driver.find_element(*locator).send_keys(Keys.DELETE)
        return self

    @allure.step("Click")
    def click(self, locator, delay=40):
        logger.debug("Click element - " + str(locator))
        try:
            self.set_implicitwait(0)
            self.wait(delay).until(EC.element_to_be_clickable(locator)).click()
            self.set_implicitwait_default()
        except Exception as e:
            logger.debug(e)
            self.javascript_click(locator, delay)
        return self

    @allure.step("Sleep")
    def sleep(self, seconds):
        time.sleep(seconds)
        return self

    @allure.step("Javascript click")
    def javascript_click(self, locator, delay=0):
        logger.debug("Javascript Click element - " + str(locator))
        if delay != 0:
            self.wait_for_element_presence(locator, delay)
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", element)
        return self

    @allure.step("Select by label")
    def select_by_label(self, select_locator, option_locator, delay=0):
        if delay != 0:
            self.wait_for_element_visible(select_locator, delay)
        self.click(select_locator)
        self.javascript_click(option_locator, 10)
        return self

    @allure.step("Select by label search")
    def select_by_label_search(
            self, select_locator=None, option_locator=None, search_locator=None, search_text=None, delay=0
    ):
        if delay != 0:
            self.wait_for_element_visible(select_locator, delay)
        if select_locator:
            self.click(select_locator)
        if search_locator:
            self.input_text(search_locator, search_text, 5, clear=True)
        time.sleep(1)
        if option_locator:
            self.javascript_click(option_locator, 30)
        return self

    @allure.step("Set implicit wait")
    def set_implicitwait(self, second):
        self.driver.implicitly_wait(second)
        return self

    @allure.step("Set default implicit wait")
    def set_implicitwait_default(self, wait=10):
        self.driver.implicitly_wait(wait)
        return self

    @allure.step("Get element")
    def get_element(self, locator, delay=0):
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        element = self.driver.find_element(*locator)
        return element

    @allure.step("Get elements")
    def get_elements(self, locator, delay=0):
        self.set_implicitwait(0)
        elements = []
        try:
            if delay != 0:
                self.wait_for_elements_visible(locator, delay)
            elements = self.driver.find_elements(*locator)
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException):
            logger.debug("Element not present - " + str(locator))
        self.set_implicitwait_default()
        logger.debug(f"Elements: {elements}")
        return elements

    @allure.step("Get element count")
    def get_element_count(self, locator, delay=0):
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        elements = self.driver.find_elements(*locator)
        return len(elements)

    @allure.step("Check if element is visible")
    def is_element_visible(self, locator, delay=10):
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        return self.driver.find_element(*locator).is_displayed()

    @allure.step("Check if element is present")
    def is_element_present(self, locator, delay=10):
        self.set_implicitwait(0)
        try:
            if delay != 0:
                logger.debug(locator)
                self.wait_for_element_presence(locator, delay)
            is_present = self.driver.find_element(*locator).is_displayed()
        except (StaleElementReferenceException, TimeoutException, NoSuchElementException):
            logger.debug("Element not present - " + str(locator))
            is_present = False
        self.set_implicitwait_default()
        return is_present

    @allure.step("Check element text")
    def element_text(self, locator, delay=0):
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        return self.driver.find_element(*locator).text

    @allure.step("Move to element click")
    def move_to_element_click(self, locator, delay=40):
        logger.debug("Move to element click- " + str(locator))
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        ele = self.driver.find_element(*locator)
        ActionChains(self.driver).move_to_element(ele).click(ele).perform()
        return self

    @allure.step("Move to element")
    def move_to_element(self, locator, delay=2):
        logger.debug("Move to = " + str(locator))
        time.sleep(delay)
        self.driver.find_element(*locator).send_keys("")
        time.sleep(delay)
        return self

    @allure.step("Is Element enabled")
    def is_element_enabled(self, locator, delay=40):
        logger.debug("Element enabled - " + str(locator))
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        ele = self.driver.find_element(*locator).is_enabled()
        logger.debug(ele)
        return ele

    @allure.step("Verify date")
    def verify_date(self, dates, data, date_format="%B,%Y,%-d"):
        dformat = date_format.split(",")
        dates = str(dates)
        if "+" not in dates and "-" not in dates:
            dates = "+" + dates
        assert self.get_datetime(dates, dateformat=dformat[0]) in data, (
                str(self.get_datetime(dates, dateformat=dformat[0])) + " " + data
        )
        assert self.get_datetime(dates, dateformat=dformat[1]) in data, (
                str(self.get_datetime(dates, dateformat=dformat[1])) + " " + data
        )
        assert self.get_datetime(dates, dateformat=dformat[2]) in data, (
                str(self.get_datetime(dates, dateformat=dformat[2])) + " " + data
        )

    @allure.step("Hover and click")
    def hover_and_click(self, locator, delay=40):
        logger.debug("Hover element - " + str(locator))
        try:
            self.wait(delay).until(EC.presence_of_element_located(locator)).click()
        except Exception as e:
            logger.debug(e)
            self.javascript_click(locator, delay)

    @allure.step("Perform Keyboard Action")
    def perform_keyboard_action(self, key_stroke):
        action = ActionChains(self.driver)
        if key_stroke == "ARROW_LEFT":
            action.send_keys(Keys.ARROW_LEFT).perform()
        elif key_stroke == "ARROW_RIGHT":
            action.send_keys(Keys.ARROW_RIGHT).perform()

    @allure.step("Scroll down")
    def perform_scroll_down(self, locator):
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        return self

    @allure.step("Input CodeMirror Object Text")
    def input_codemirror_text(self, locator, data, delay=0):
        logger.debug("Input CodeMirror text - " + str(locator) + " data: " + str(data))
        if delay != 0:
            self.wait_for_element_visible(locator, delay)
        ele = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].CodeMirror.setValue('')", ele)
        ActionChains(self.driver).move_to_element(ele).click(ele).perform()
        ActionChains(self.driver).send_keys(data).perform()
        return self

    def get_alert_msg(self, delay=20):
        locator = (By.CSS_SELECTOR, '[role="alert"]')
        alert_text = self.get_text(locator, delay).strip()
        for _ in range(5):
            if self.is_element_present(locator, 5):
                self.click(locator)
                self.sleep(1)
                continue
            break
        self.sleep(1)
        return alert_text
