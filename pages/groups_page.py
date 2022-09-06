import enum

from selenium.webdriver.common.keys import Keys

from locators import groups_locators as gl
from utils.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class GroupsSearchBy(enum.Enum):
    """
    Enum Class for Search filter options
    """

    NAME = "Name"
    USERS = "Users"
    PLUGINS = "Plugins"
    APPS = "Apps"
    SECURITY_OBJECTS = "Security Objects"
    CREATED = "Created"
    DESCRIPTION = "Description"


class GroupsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def add_new_group(self, name, **kwargs):
        """
        Add a new group
        :param name: (str) Group title
        :param kwargs: (key-word arguments)
        :return: (obj) self
        """
        self.click(gl.addNewGroup, 20)
        self.input_text(gl.groupTitleInput, name, 10)
        logger.info(f"kwargs: {kwargs}")
        if kwargs.get("description"):
            self.input_text(gl.groupDescriptionInput, name, 3)
        if kwargs.get("quorum_data"):
            self.click(gl.addQuorumPolicyBtn, 1)
            self.input_text(gl.quorumQtyInput, kwargs["quorum_data"]["qty"], 10)
            for user in kwargs["quorum_data"]["users"]:
                user_option = (
                    gl.userSelectOption[0],
                    gl.userSelectOption[1].replace("User", user.strip()),
                )
                self.click(gl.userSearchInput).click(user_option, 10)
        self.click(gl.saveBtn, 5)
        assert self.get_alert_msg() == "Group was successfully created"
        return self

    def search_open_group(self, search_by: GroupsSearchBy, search_text: str):
        """
        :param search_by: (enum) Search filter options
        :param search_text: (str) Search string or substring
        :return: (obj) self
        """
        self.click(gl.searchInput, 20)
        self.input_text(gl.searchInput, search_text + Keys.ENTER, 5)
        self.click(gl.firstSearchValue, 10)

    def delete_group(self):
        """
        Click on delete group button
        :return: (obj) self
        """
        self.click(gl.deleteGroup, 20)
        return self

    def add_key_metadata_policy(self, **kwargs):
        """
        Add key metadata policy to the group
        :param kwargs: (key-word arguments)
        :return: (obj) self
        """
        self.click(gl.addKeyMetaDataPolicyBtn)
        # Close custom attribute option
        self.wait_for_element_visible(gl.customAttributeCloseIcon).click(gl.customAttributeCloseIcon)
        self.wait_for_element_visible(gl.keyDescription)
        # Add data
        if kwargs.get("key_description"):
            key_option = (
                gl.keyDescriptionBtn[0],
                gl.keyDescriptionBtn[1].replace("Value", kwargs.get("key_description_value")),
            )
            self.wait_for_element_visible(key_option).click(key_option)
        if kwargs.get("activation_date"):
            activation_option = (
                gl.activationDateBtn[0],
                gl.activationDateBtn[1].replace("Value", kwargs.get("activation_date_value")),
            )
            self.wait_for_element_visible(activation_option).click(activation_option)
        if kwargs.get("deactivation_date"):
            deactivation_option = (
                gl.deactivationDateBtn[0],
                gl.deactivationDateBtn[1].replace("Value", kwargs.get("deactivation_date_value")),
            )
            self.wait_for_element_visible(deactivation_option).click(deactivation_option)
        if kwargs.get("custom_attribute"):
            self.click(gl.customAddBtn)
            if kwargs.get("attribute_text"):
                # Tap on option
                custom_attribute_option = (
                    gl.customAttributeBtn[0],
                    gl.customAttributeBtn[1].replace("Value", kwargs.get("custom_attribute_value")),
                )
                self.wait_for_element_visible(custom_attribute_option).click(custom_attribute_option)
                self.input_text(gl.customAttributeKey, kwargs.get("attribute_text"))
                if kwargs.get("custom_attribute_value") == "required":
                    # Check the checkbox
                    self.wait_for_element_visible(gl.cannotContainWhitespaceCheckbox).click(
                        gl.cannotContainWhitespaceCheckbox
                    )
                    self.wait_for_element_visible(gl.restrictValueToOneValueCheckbox).click(
                        gl.restrictValueToOneValueCheckbox
                    )
                    # Enter allowed value post checking checkbox
                    allowed_values = kwargs.get("attribute_text")[0:10]
                    logger.info(f"Allowed values - {allowed_values}")
                    self.input_text(gl.customAttributeTextbox, allowed_values)
        if kwargs.get("non_compilant_keys"):
            # Select option of non-compliant keys
            non_compilant_keys_option = (
                gl.handlingKeysAllowedBtn[0],
                gl.handlingKeysAllowedBtn[1].replace("Value", kwargs.get("non_compilant_keys")),
            )
            self.wait_for_element_visible(non_compilant_keys_option).click(non_compilant_keys_option)
        self.click(gl.saveBtn)
        assert self.get_alert_msg() == "Group was successfully updated"
        return self

    def click_add_crypto_policy(self):
        """
        Click on add crypto policy button
        :return: (obj) self
        """
        self.click(gl.addEditCryptoPolicyBtn)
        return self

    def click_save_crypto_policy(self):
        """
        Click on save crypto policy button
        :return: (obj) self
        """
        self.click(gl.savePolicyBtn)
        assert self.get_alert_msg() == "Group was successfully updated"
        return self

    def add_key_undo_policy(self, days, quorum=False):
        """
        Add key undo policy to the group
        :return: (obj) self
        """
        if quorum:
            self.click(gl.addKeyUndoPolicyBtn).input_text(gl.daysKeyUndoPolicyInput, days, clear=True).click(
                gl.saveKeyUndoPolicyBtn
            )
        else:
            self.click(gl.addKeyUndoPolicyBtn)
            self.input_text(gl.daysKeyUndoPolicyInput, days, clear=True)
            self.click(gl.saveKeyUndoPolicyBtn)
            assert self.get_alert_msg() == "Group was successfully updated"
        return self
