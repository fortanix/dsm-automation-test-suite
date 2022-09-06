import enum

from selenium.webdriver.common.keys import Keys

from locators import security_objects_locators as sl
from pages.dashboard_page import DashboardPage
from utils.base_page import BasePage
from utils.logger_util import get_logger

logger = get_logger(__name__)


class SecurityObjectType(enum.Enum):
    """
    Enum Class for Security Object Types
    """

    IMPORT = "Import"
    GENERATE = "Generate"


class SecurityObjectKeyType(enum.Enum):
    """
    Enum Class for Security Object Key Types
    """

    AES = "AES"
    DES3 = "DES3"
    HMAC = "HMAC"
    RSA = "RSA"
    DSA = "DSA"
    DES = "DES"
    EC = "EC"
    TOKENIZATION = "TOKENIZATION"
    ARIA = "ARIA"
    EC_KCDSA = "ECKCDSA"
    KCDSA = "KCDSA"
    SEED = "SEED"


class SecurityObjectsSearchBy(enum.Enum):
    """
    Enum Class for Search filter options
    """

    UUID = "UUID"
    STATE = "State"
    NAME = "Name"
    KEY_OPS = "Key Ops"
    GROUP = "Group"
    CREATOR = "Creator"
    TYPE = "Type"
    CREATOR_TYPE = "Creator Type"
    KEY_SIZE = "Key Size"
    ELLIPTIC_CURVE = "Elliptic Curve"
    CUSTOM_ATTRIBUTES = "Custom Attributes"


class SecurityObjectsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.dp = DashboardPage(self.driver)

    def add_new_security_object(self, so_name, so_type: SecurityObjectType, **kwargs):
        """
        :param so_name: (str) Name of the security object to be created
        :param so_type: (enum) Type of security object
        :param kwargs: (kwargs/dict) additional parameters as key-word arguments
        :return: (obj) self
        """
        self.dp.navigate_to_security_objects()
        logger.info(f"Create new security objects: {so_name}, {so_type}, {kwargs}")
        self.wait_for_element_clickable(sl.addSOBtn).sleep(1)
        self.click(sl.addSOBtn)
        self.input_text(sl.nameInput, so_name, 10)
        if kwargs.get("description"):
            self.input_text(sl.descriptionInput, kwargs["description"], 5)
        if kwargs.get("group"):
            grp_name = kwargs.get("group")
            self.sleep(1).wait_for_element_clickable(sl.selectGrpDropDwn).click(sl.selectGrpDropDwn, 20)
            logger.info(f"Select group {grp_name}. Group dropdown list:")
            for el in self.get_elements(sl.selectGrpDropDwnValues, 20):
                logger.info(f"{el.text}")
                if el.text == grp_name:
                    el.click()
                    logger.info(f"Selected group")
                    break
            else:
                self.click(sl.createNewGroupBtn, 5)
                self.wait_for_element_clickable(sl.newgGroupTitleInput, 10)
                self.input_text(sl.newgGroupTitleInput, grp_name, 10)
                self.input_text(sl.newGroupDescriptionInput, "Created by Automation", 1)
                self.click(sl.modalCreateNewGroupBtn, 5)
        if so_type == SecurityObjectType.GENERATE:
            self.javascript_click(sl.generateRadioBtn)
        if kwargs.get("key_type"):
            if self.is_element_present(sl.skipTutorialText, 5):
                self.click(sl.skipTutorialText, 20)
            key_type = (
                sl.chooseTypeRadioBtn[0],
                sl.chooseTypeRadioBtn[1].replace("Type", kwargs["key_type"].strip()) + "+label",
            )
            self.javascript_click(key_type, 10)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if kwargs.get("key_type") == "ECKCDSA":
                self.select_curve_subgroup_size_dropdown_value(kwargs["curve_type"])
                self.select_hashing_algorithm_dropdown_value(kwargs["hash_algo"])
            if kwargs.get("key_type") == "KCDSA":
                self.select_keysize_dropdown_value(kwargs["key_size"])
                self.select_curve_subgroup_size_dropdown_value(kwargs["subgroup_size"])
                self.select_hashing_algorithm_dropdown_value(kwargs["hash_algo"])
        self.click(sl.generateBtn, 20)
        assert self.get_alert_msg() == "Security Object was successfully created"
        self.wait_for_element_presence(sl.keyTitle)
        return self

    def select_keysize_dropdown_value(self, key_size):
        """
        :param key_size: (str) Name of the key size
        :return: (obj) self
        """
        self.move_to_element_click(sl.keySizeDropDwn, 10)
        logger.info(f"Select key size: {key_size}")
        for el in self.get_elements(sl.keySizeDropDwnValues, 5):
            logger.info(f"{el.text}")
            if el.text == key_size:
                el.click()
                break
        return self

    def select_curve_subgroup_size_dropdown_value(self, curve_subgroup_size):
        """
        :param curve_subgroup_size: (str) Name of the curve or subgroup size
        :return: (obj) self
        """
        self.move_to_element_click(sl.subGroupSizeDropDwn, 10)
        logger.info(f"Select curve/subgroup size: {curve_subgroup_size}")
        for el in self.get_elements(sl.subGroupSizeDropDwnValues, 5):
            logger.info(f"{el.text}")
            if el.text == curve_subgroup_size:
                el.click()
                break
        return self

    def select_hashing_algorithm_dropdown_value(self, hash_algo):
        """
        :param hash_algo: (str) Name of the hashing algorithm
        :return: (obj) self
        """
        self.move_to_element_click(sl.hashingAlgoDropDwn, 10)
        logger.info(f"Select hashing algorithm: {hash_algo}")
        for el in self.get_elements(sl.hashingAlgoDropDwnValues, 5):
            logger.info(f"{el.text}")
            if el.text == hash_algo:
                el.click()
                break
        return self

    def search_open_security_object(self, search_by: SecurityObjectsSearchBy, search_text: str):
        """
        :param search_by: (enum) Search with filter option
        :param search_text: (str) search string
        :return: (obj) self
        """
        self.click(sl.searchInput, 10)
        search_by_el = (
            sl.searchOptions[0],
            sl.searchOptions[1].replace("SEARCH_OPTION", search_by.value),
        )
        self.click(search_by_el, 5)
        self.input_text(sl.searchInput, search_text + Keys.ENTER, 5)
        self.click(sl.firstSearchValue, 10)
        return self

    def copy_key(self, group_name):
        """
        :param group_name: (str) Select group name to copy key to
        :return: (obj) self
        """
        self.wait_for_element_presence(sl.keyTitle)
        self.click(sl.newObjectBtn, 10)
        self.click(sl.copyKeyBtn, 10)
        self.input_text(sl.copyKeyDescriptionInput, f"Copy Key description", 10)
        self.input_text(sl.copyKeySearchGrpName, group_name, 10)
        logger.info(f"Select group {group_name}")
        self.click(sl.copyKeyFirstGroupName, 10)
        self.click(sl.createCopyKeyBtn, 10)
        assert self.get_alert_msg() == "Security Object was successfully copied"
        self.wait_for_element_presence(sl.keyTitle)
        self.click(sl.keyLinkTab, 20)
        self.click(sl.copiedKey, 20)
        return self

    def rotate_key(self, delete_original=False):
        """
        :param delete_original: (bool) Select delete original key flag
        :return: (obj) self
        """
        self.wait_for_element_presence(sl.keyTitle)
        self.click(sl.rotateKeyBtn)
        if delete_original:
            self.click(sl.deactivateOriginalKeyChkBx, 10)
        self.input_text(sl.rotateKeyDescription, f"Rotate Key description", 10)
        self.click(sl.rotateKeyModalBtn, 10)
        alert_msg = self.get_alert_msg()
        assert alert_msg == "Security Object was successfully rotated", f"{alert_msg} message does not match"
        self.wait_for_element_presence(sl.keyTitle)
        return self

    def deactivate_key(self):
        """
        :return: (obj) self
        """
        self.wait_for_element_presence(sl.keyTitle)
        self.wait_for_element_presence(sl.deactivateNowBtn)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.click(sl.deactivateNowBtn)
        self.click(sl.deactivationUnderstandChkbx, 0)
        self.click(sl.saveBtn, 10)
        assert self.get_alert_msg() == "Key is deactivated"
        for _ in range(10):
            if self.get_text(sl.deactivationStatusText, 10) == "Deactivated":
                break
            self.sleep(1)
        else:
            assert False, "Deactivated text not updated"
        return self

    def destroy_key(self):
        """
        :return: (obj) self
        """
        self.wait_for_element_presence(sl.keyTitle)
        self.click(sl.destroyKeyBtn, 20)
        self.click(sl.destroyKeyUnderstandChkbx, 10)
        self.click(sl.destroyDeleteKeyProceedBtn, 10)
        alert_msg = self.get_alert_msg()
        assert alert_msg == "Security object was successfully destroyed", f"{alert_msg} message does not match"
        return self

    def delete_key(self):
        """
        :return: (obj) self
        """
        self.wait_for_element_presence(sl.keyTitle)
        self.click(sl.deleteKeyBtn, delay=60)
        self.click(sl.deleteKeyUnderstandChkbx, 10)
        if self.is_element_present(sl.deleteRotatedKeyUnderstandChkbx):
            self.click(sl.deleteRotatedKeyUnderstandChkbx, 3)
        self.click(sl.destroyDeleteKeyProceedBtn, 10)
        alert_msg = self.get_alert_msg(delay=40)
        assert (alert_msg == "Security object was successfully deleted") or (
            alert_msg == "sobject does not exist"
        ), f"{alert_msg} message does not match"
        return self
