import enum

from locators import apps_locators as al
from pages.dashboard_page import DashboardPage
from utils.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class AppAuthMethod(enum.Enum):
    """
    Enum Class for Security Object Types
    """

    API_KEY = "API Key"
    CERTIFICATE = "Certificate"
    TRUSTED_CA = "Trusted CA"
    GOOGLE_SERVICE_ACCOUNT = "Google Service Account"
    JSON_WEB_TOKEN = "JSON Web Token"


class AppsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.dp = DashboardPage(self.driver)

    def create_new_app(self, app_name: str, auth_method: AppAuthMethod, group_name, **kwargs):
        """ "
        :param app_name: (str) Name of the app to be created
        :param auth_method: (enum) Type of App Auth Method
        :param group_name: (str) Assigning the new app to groups
        :param kwargs: (kwargs/dict) additional parameters as key-word arguments
        :return: (obj) self
        """
        self.click(al.newAppBtn)
        self.wait_for_element_visible(al.appNameInput).input_text(al.appNameInput, app_name)
        if kwargs.get("interface"):
            app_type = (
                al.appTypeOption[0],
                al.appTypeOption[1].replace("AppType", kwargs.get("interface")),
            )
            self.select_by_label(al.appTypeSelect, app_type)
        app_method = (
            al.appMethodRadioBtn[0],
            al.appMethodRadioBtn[1].replace("AppMethod", auth_method),
        )
        self.click(app_method)
        if kwargs.get("secret_size"):
            secret_size_loc = (
                al.secretSizeOption[0],
                al.secretSizeOption[1].replace("SecretSize", kwargs.get("secret_size")),
            )
            self.click(al.setAppSecretLink).select_by_label(al.secretSizeSelect, secret_size_loc)
        if kwargs.get("certificate"):
            self.input_text(al.certificateTextarea, kwargs.get("certificate"))
        if kwargs.get("trustedca"):
            self.input_text(al.taCertificateTextarea, kwargs.get("trustedca"))
        if kwargs.get("san_type"):
            san_type_locator = (
                al.sanTypeOption[0],
                al.sanTypeOption[1].replace("SANType", kwargs.get("san_type")),
            )
            self.select_by_label(al.sanTypeSelect, san_type_locator)
            if kwargs.get("san_type") == "Directory Name":
                san_direc_locator = (
                    al.directoryTypeOption[0],
                    al.directoryTypeOption[1].replace("DirectoryType", kwargs.get("directory_type")),
                )
                self.select_by_label(al.directoryTypeSelect, san_direc_locator).input_text(
                    al.directoryValue, kwargs.get("san_type")
                )
            else:
                self.input_text(al.sanValueInput, kwargs.get("san_value"))
        if kwargs.get("issuer"):
            self.input_text(al.issuerInput, kwargs.get("issuer"))
        if kwargs.get("key_url"):
            self.click(al.fetchedSigningKeyRadio).input_text(al.keyUrlInput, kwargs.get("key_url"))
        if kwargs.get("oauth_url"):
            self.click(al.enableOauthToggle).input_text(al.redirectUrlInput, kwargs.get("oauth_url"))
        group_option = (
            al.searchGroupOption[0],
            al.searchGroupOption[1].replace("GroupName", group_name),
        )
        self.select_by_label_search(
            search_locator=al.searchGroupInput,
            search_text=group_name,
            option_locator=group_option,
        )
        self.click(al.saveAppBtn)
        assert self.get_alert_msg() == "App was successfully created"
        self.wait_for_element_presence(al.appTitle)
        return self

    def delete_app(self, app_name):
        """
        :param app_name: (str) Name of the app
        :return: (obj) self
        """
        self.click(al.deleteAppBtn, 10)
        self.click(al.deleteAppConfirmBtn, 10)
        assert self.get_alert_msg() == "App was successfully deleted"
        return self
