from locators import dashboard_locators as dl
from utils.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_page_title(self):
        """
        Get title of the the page
        :return: (obj) self
        """
        return self.get_text(dl.pageTitleText)

    def navigate_to_dashboard(self):
        """
        Navigate to dashboard
        :return: (obj) self
        """
        self.click(dl.dashboardTab)
        return self

    def navigate_to_integrations(self):
        """
        Navigate to integrations tab
        :return: (obj) self
        """
        self.click(dl.integrationsTab)
        return self

    def navigate_to_groups(self):
        """
        Navigate to groups tab
        :return: (obj) self
        """
        self.click(dl.groupsTab)
        return self

    def navigate_to_apps(self):
        """
        Navigate to apps tab
        :return: (obj) self
        """
        self.click(dl.appsTab)
        return self

    def navigate_to_security_objects(self):
        """
        Navigate to security objects tab
        :return: (obj) self
        """
        self.click(dl.sobjectsTab)
        return self

    def navigate_to_users(self):
        """
        Navigate to users tab
        :return: (obj) self
        """
        self.click(dl.usersTab)
        return self

    def navigate_to_plugins(self):
        """
        Navigate to plugins tab
        :return: (obj) self
        """
        self.click(dl.pluginsTab)
        return self

    def navigate_to_tasks(self):
        """
        Navigate to tasks tab
        :return: (obj) self
        """
        self.click(dl.tasksTab)
        return self

    def navigate_to_audit_logs(self):
        """
        Navigate to audit logs tab
        :return: (obj) self
        """
        self.click(dl.eventsTab)
        return self

    def navigate_to_settings(self):
        """
        Navigate to settings tab
        :return: (obj) self
        """
        self.click(dl.settingsTab)
        return self

    def get_total_apps_card_texts(self):
        """
        Get total apps card texts
        :return: text_list (list)
        """
        self.wait_for_element_presence(dl.totalAppsCountText)
        text_list = self.get_text(dl.totalAppsText).split("\n")
        logger.info(f"Total Active Apps card text list: {text_list}")
        return text_list

    def get_total_operations_card_texts(self):
        """
        Get total operations card texts
        :return: text_list (list)
        """
        text_list = self.get_text(dl.totalOperationsText).split("\n")
        logger.info(f"Total Active Apps card text list: {text_list}")
        return text_list

    def get_total_security_objects_card_texts(self):
        """
        Get total security objects card texts
        :return: text_list (list)
        """
        text_list = self.get_text(dl.totalSObjectsText).split("\n")
        logger.info(f"Total operations card text list: {text_list}")
        return text_list

    def get_tokenization_operations_apps_card_texts(self):
        """
        Get tokenization operations apps card texts
        :return: text_list (list)
        """
        text_list = self.get_text(dl.tokenizationText).split("\n")
        logger.info(f"Tokenization operations/apps card text list: {text_list}")
        return text_list

    def get_total_plugins_card_texts(self):
        """
        Get total plugins card texts
        :return: text_list (list)
        """
        text_list = self.get_text(dl.totalPluginsText).split("\n")
        logger.info(f"Total plugins card text list: {text_list}")
        return text_list

    def get_hsm_gateway_card_texts(self):
        """
        Get hsm gateway card texts
        :return: text_list (list)
        """
        text_list = self.get_text(dl.hsmGatewayText).split("\n")
        logger.info(f"HSM Gateway card text list: {text_list}")
        return text_list

    def get_usage_charts_cards_texts(self):
        """
        Get usage charts cards texts
        :return: text_list (list)
        """
        text_list = self.get_texts(dl.usageCharts)
        logger.info(f"Usage charts card text list: {text_list}")
        return text_list
