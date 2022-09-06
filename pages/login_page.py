import os

import locators.login_locators as ll
import locators.dashboard_locators as dl
from utils.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def login(self, email, password):
        """
        :param email: (str) Email of the user
        :param password: (str) Password of the user
        """
        try:
            self.input_text(ll.emailInput, email, 30)
            self.click(ll.loginWithOutSSO)
            self.input_password(ll.passwordInput, password, 30)
            self.click(ll.loginBtn)
            self.wait_for_element_visible(ll.loginSuccess)
        except:
            self.driver.execute_script("window.localStorage.clear();")
            self.driver.refresh()
            self.input_text(ll.emailInput, email, 30)
            self.click(ll.loginWithOutSSO)
            self.input_password(ll.passwordInput, password, 30)
            self.click(ll.loginBtn)
            self.wait_for_element_visible(ll.loginSuccess)
        os.environ["DSM_VERSION"] = self.get_text(ll.versionText, 10)
        return self

    def select_account(self, account_id):
        """
        :param account_id: (str) account id of the user account.
        Account ID Can be obtained from: Select account > Settings > Copy Account ID
        """
        account_el = (
            ll.selectAccount[0],
            ll.selectAccount[1].replace("ACCOUNT_ID", account_id),
        )
        for _ in range(5):
            if self.is_element_present(account_el, 5):
                self.move_to_element_click(account_el, 5)
                break
            elif self.is_element_present(ll.dashboardPage, 10):
                self.click(dl.accountSwitcherBtn, 5)
                self.click(dl.viewAllBtn, 5)
            else:
                self.click(ll.loadMoreBtn, 5)
                self.sleep(1)
        logger.info(f"Selected account: {account_id}")
        return self
