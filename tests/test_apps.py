import os
import uuid

import allure
import pytest
from pytest_steps import test_steps

from pages.apps_page import AppsPage, AppAuthMethod
from pages.dashboard_page import DashboardPage
from pages.groups_page import GroupsPage
from utils.logger_util import get_logger

logger = get_logger(__name__)


@allure.parent_suite("DSM")
@allure.suite("Apps")
@pytest.mark.smoke
@pytest.mark.apps
class TestApps:
    @classmethod
    def setup_class(cls):
        cls.app_title = "App_" + uuid.uuid4().hex[:5]

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.dp = DashboardPage(self.driver)
        self.gp = GroupsPage(self.driver)
        self.ap = AppsPage(self.driver)
        self.certificate = open(os.getcwd() + "/testdata/general/certificate.pem", "r").read()
        self.ca_cert = open(os.getcwd() + "/testdata/general/certificate2.pem", "r").read()

    @test_steps("01-Create App", "02-Delete App")
    @pytest.mark.parametrize("auth_method", [v.value for v in AppAuthMethod.__members__.values()])
    def test_apps(self, auth_method):
        app_title = f"{self.app_title}_{auth_method}"
        gs_app_name = f"service-sample-28${uuid.uuid4().hex[:5]}@gcp-sa-ekms.iam.gserviceaccount.com"
        grp_title = "Group_Apps_" + uuid.uuid4().hex[:5]

        self.dp.navigate_to_groups()
        self.gp.add_new_group(name=grp_title)

        self.dp.navigate_to_apps()
        logger.info(f"Create a new {auth_method} app: {app_title}")
        if auth_method == "API Key":
            self.ap.create_new_app(app_title, auth_method, grp_title)

        if auth_method == "Certificate":
            self.ap.create_new_app(app_title, auth_method, grp_title, certificate=self.certificate)

        if auth_method == "Trusted CA":
            self.ap.create_new_app(
                app_title,
                auth_method,
                grp_title,
                trustedca=self.ca_cert,
                san_type="DNS Name",
                san_value="sample.com",
            )

        if auth_method == "Google Service Account":
            self.ap.create_new_app(gs_app_name, auth_method, grp_title)

        if auth_method == "JSON Web Token":
            self.ap.create_new_app(
                app_title,
                auth_method,
                grp_title,
                issuer="https://sample.com",
                key_url="https://sample12.com",
            )

        yield

        if auth_method == "Google Service Account":
            logger.info(f"Delete app: {gs_app_name}")
            self.ap.delete_app(gs_app_name)
        else:
            logger.info(f"Delete app: {app_title}")
            self.ap.delete_app(app_title)
        yield
