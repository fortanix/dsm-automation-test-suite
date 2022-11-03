import allure
import pytest

from pages.dashboard_page import DashboardPage


@allure.parent_suite("DSM")
@allure.suite("Dashboard")
@pytest.mark.smoke
@pytest.mark.dashboard
class TestHomeDashboardUI:

    @pytest.fixture(autouse=True)
    def setup_class(self, driver):
        self.driver = driver
        self.dp = DashboardPage(self.driver)

    @pytest.mark.skip("On-prem cluster")
    def test_ui_navigate_to_home(self):
        self.dp.navigate_to_home()
        assert "Welcome" in self.dp.get_homepage_welcome_text()

    def test_ui_navigate_to_integrations(self):
        self.dp.navigate_to_integrations()
        assert self.dp.get_page_title() == "Integrations", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_groups(self):
        self.dp.navigate_to_groups()
        assert self.dp.get_page_title() == "Groups", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_apps(self):
        self.dp.navigate_to_apps()
        assert self.dp.get_page_title() == "Apps", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_security_objects(self):
        self.dp.navigate_to_security_objects()
        assert self.dp.get_page_title() == "Security Objects", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_users(self):
        self.dp.navigate_to_users()
        assert self.dp.get_page_title() == "Users", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_plugins(self):
        self.dp.navigate_to_plugins()
        assert self.dp.get_page_title() == "Plugins", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_tasks(self):
        self.dp.navigate_to_tasks()
        assert self.dp.get_page_title() == "Tasks", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_audit_logs(self):
        self.dp.navigate_to_audit_logs()
        assert self.dp.get_page_title_audit_log() == "Audit Log", "Navigation to page failed. Title does not match!"

    def test_ui_navigate_to_settings(self):
        self.dp.navigate_to_settings()
        assert self.dp.get_page_title() == "Account settings", "Navigation to page failed. Title does not match!"

    def test_ui_verify_text(self):
        self.dp.navigate_to_dashboard()
        assert all(item in self.dp.get_total_apps_card_texts() for item in ['Total Active Apps', 'Cloud Connections'])
        assert all(item in self.dp.get_total_operations_card_texts() for item in
                   ['Total Operations', 'Encrypt', 'Decrypt', 'Secret Operations', 'Sign', 'Verify', 'Others'])
        assert all(item in self.dp.get_tokenization_operations_apps_card_texts() for item in
                   ['Tokenization Operations', 'Tokenization Apps'])
        assert 'Total Security Objects' in self.dp.get_total_security_objects_card_texts()
        assert 'Total Plugins' in self.dp.get_total_plugins_card_texts()
        assert 'HSM Gateways' in self.dp.get_hsm_gateway_card_texts()
        assert all(item in self.dp.get_usage_charts_cards_texts() for item in
                   ['Total Operations', 'Total Tokenization Operations', 'Total Plugin Invocations'])
