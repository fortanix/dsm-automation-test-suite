import uuid

import allure
import pytest
from pytest_steps import test_steps

from pages.security_objects_page import SecurityObjectKeyType, SecurityObjectType
from pages.security_objects_page import SecurityObjectsPage
from utils.logger_util import get_logger

logger = get_logger(__name__)


@allure.parent_suite("DSM")
@allure.suite("SecurityObjects")
@pytest.mark.smoke
@pytest.mark.security_objects
class TestSecurityObjects:
    @classmethod
    def setup_class(cls):
        cls.so_title = "SO_" + uuid.uuid4().hex[:5]
        cls.grp_title = "Group_" + uuid.uuid4().hex[:5]

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.so = SecurityObjectsPage(self.driver)

    @test_steps(
        "01-Create Security Object",
        "02-Copy Key",
        "03-Rotate Key",
        "04-Deactivate Key",
        "05-Destroy Key",
        "06-Delete Key",
    )
    @pytest.mark.parametrize("key_type", [v.value for v in SecurityObjectKeyType.__members__.values()])
    def test_security_object(self, key_type):
        so_title = f"{self.so_title}_{key_type}"
        logger.info(f"Create a new security object: {so_title}")
        self.so.add_new_security_object(
            so_name=so_title,
            group=self.grp_title,
            so_type=SecurityObjectType.GENERATE,
            key_type=key_type,
            key_size="2048",
            curve_type="NistP256",
            subgroup_size="256",
            hash_algo="SHA256",
        )
        key_url = self.driver.current_url
        logger.info(f"Key url: {key_url}")
        yield

        logger.info(f"Test step: Copy Key")
        self.so.copy_key(group_name=self.grp_title)
        copied_key_url = self.driver.current_url
        logger.info(f"Copied key url: {copied_key_url}")
        self.so.open_url(key_url)
        yield

        if key_type != "TOKENIZATION":
            logger.info(f"Test step: Rotate Key")
            self.so.rotate_key()
        yield
        rotated_key_url = self.driver.current_url
        logger.info(f"Rotated key url: {rotated_key_url}")

        logger.info(f"Test step: Deactivate Key")
        self.so.deactivate_key()
        yield

        logger.info(f"Test step: Destroy Key")
        self.so.open_url(rotated_key_url)
        self.so.destroy_key()
        yield

        logger.info(f"Test step: Delete Copied Key")
        self.so.open_url(copied_key_url)
        self.so.delete_key()

        if key_type != "TOKENIZATION":
            logger.info(f"Test step: Delete Rotated Key")
            self.so.open_url(rotated_key_url)
            self.so.delete_key()

        logger.info(f"Test step: Delete Key")
        self.so.open_url(key_url)
        self.so.delete_key()
        yield
