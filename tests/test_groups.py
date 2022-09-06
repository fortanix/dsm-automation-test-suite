import os
import uuid

import allure
import pytest
from pytest_steps import test_steps

from pages.dashboard_page import DashboardPage
from pages.groups_page import GroupsPage, GroupsSearchBy
from utils import session
from utils.helper import read_json
from utils.logger_util import get_logger

logger = get_logger(__name__)


@allure.parent_suite("DSM")
@allure.suite("Groups")
@pytest.mark.smoke
@pytest.mark.groups
class TestGroup:
    @classmethod
    def setup_class(cls):
        cls.group_title = "Group_" + uuid.uuid4().hex[:8]

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.dp = DashboardPage(self.driver)
        self.gp = GroupsPage(self.driver)

    @test_steps(
        "01-Quorum Policy",
        "02-Crypto Policy",
        "03-Key Metadata Policy",
        "04-Key Undo Policy",
        "05-Delete Group",
    )
    def test_groups(self):
        grp_title = "Group_Quorum_" + uuid.uuid4().hex[:8]
        user = session.dsm_data["user"]["ACCOUNTADMINISTRATOR"]
        quorum_data = {
            "qty": 1,
            "users": [user[0]["first_name"] + ("" if user[0]["last_name"] is None else " " + user[0]["last_name"])],
        }

        # Create group with quorum policy
        logger.info(f"Create a new group {grp_title} with quorum policy")
        self.dp.navigate_to_groups()
        self.gp.add_new_group(name=grp_title, quorum_data=quorum_data)
        self.gp.delete_group()
        yield

        # Add crypto policy
        logger.info(f"Add crypto policy to the group: {grp_title}")
        self.dp.navigate_to_groups()
        self.gp.add_new_group(name=self.group_title)
        self.gp.click_add_crypto_policy().click_save_crypto_policy()
        yield

        # Add key metadata policy
        logger.info(f"Add key metadata policy to the group: {grp_title}")
        self.gp.add_key_metadata_policy(attribute_text=f"Attr_{uuid.uuid4().hex[:8]}")
        yield

        # Add key undo policy
        logger.info(f"Add key undo policy to the group: {grp_title}")
        self.gp.add_key_undo_policy(days=5)
        yield

        # Delete group
        self.gp.delete_group()
        yield
