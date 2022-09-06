import os
import shutil
from datetime import datetime

import allure
import pandas as pd
import pytest
import requests

from pages.login_page import LoginPage
from utils import session
from utils.api import API
from utils.browser_factory import BrowserFactory
from utils.helper import read_json
from utils.logger_util import get_logger
from utils.report_helpers import build_table, write_to_csv, build_data

requests.packages.urllib3.disable_warnings()

logger = get_logger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--BROWSER",
        action="store",
        default="Chrome",
        help="Supported browsers: Chrome | Firefox | Edge",
    )
    parser.addoption("--BROWSER_MODE", action="store", default="head")
    parser.addoption("--URL", action="store", required=True, help="Test Environment URL")
    parser.addoption(
        "--EMAIL",
        action="store",
        required=True,
        help="Provide username to run perform login",
    )
    parser.addoption(
        "--PASSWORD",
        action="store",
        required=True,
        help="Provide password to run perform login",
    )
    parser.addoption(
        "--ACCOUNT_ID",
        action="store",
        required=True,
        help="Account ID to run tests with",
    )


@pytest.fixture(scope="session", autouse=True)
def url(request):
    return request.config.getoption("URL")


@pytest.fixture(scope="session", autouse=True)
def email(request):
    return request.config.getoption("EMAIL")


@pytest.fixture(scope="session", autouse=True)
def password(request):
    return request.config.getoption("PASSWORD")


@pytest.fixture(scope="session", autouse=True)
def account_id(request):
    return request.config.getoption("ACCOUNT_ID")


@pytest.fixture(scope="session", autouse=True)
def driver(request, url, email, password, account_id):
    session.dsm_data["BROWSER_MODE"] = request.config.getoption("BROWSER_MODE")
    os.environ["BROWSER"] = request.config.getoption("BROWSER")
    os.environ["URL"] = url

    # Initialize WebDriver
    driver = BrowserFactory().get_browser(request.config.getoption("BROWSER"), request.config.getoption("BROWSER_MODE"))
    driver.maximize_window()

    # Wait implicitly for elements to be ready before attempting interactions
    default_wait = 10
    driver.implicitly_wait(default_wait)
    driver.get(url)
    lp = LoginPage(driver)
    lp.login(email, password)
    api = API(url, email, password)
    if account_id not in api.get_all_accounts():
        if driver:
            driver.quit()
        pytest.exit(f"{account_id} account does not exit. Please pass a valid account id!")
    lp.select_account(account_id)

    account_data = api.get_account_details(account_id)
    session.dsm_data["account"] = {}
    session.dsm_data["account"]["accountName"] = account_data.json()["name"]
    session.dsm_data["account"]["accountId"] = account_id

    dsm_user = {}
    temp_userdata = []
    temp_user = {"user_email": email, "user_password": password}
    api_obj = API(url, temp_user["user_email"], temp_user["user_password"])

    # Cleanup account objects(Keys, groups, apps, etc) as a part of setup
    api_obj.remove_objects_from_account(account_id)

    user_details = api_obj.get_user(api_obj.user_id)
    if not user_details.json().get("first_name"):
        # Set first/last name, if not already set
        api_obj.update_user_first_last_name(api_obj.user_id, "Test", "User")
    user_details = api_obj.get_user(api_obj.user_id)
    temp_user["first_name"] = user_details.json().get("first_name")
    temp_user["last_name"] = user_details.json().get("last_name")
    temp_user["token_type"] = api_obj.token_type
    temp_user["access_token"] = api_obj.access_token
    temp_user["headers"] = {"Authorization": "{} {}".format(temp_user["token_type"], temp_user["access_token"])}
    temp_userdata.append(temp_user)
    dsm_user["ACCOUNTADMINISTRATOR"] = temp_userdata
    session.dsm_data["user"] = dsm_user

    yield driver

    if driver:
        driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, "report_" + report.when, report)
    if report.when == "call":
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            try:
                allure.attach(
                    item.funcargs["driver"].get_screenshot_as_png(),
                    name="{}_{}".format(item.name, timestamp),
                    attachment_type=allure.attachment_type.PNG,
                )
            except:
                pass
    return report


def pytest_sessionfinish(session, exitstatus):
    try:
        allure_dir = os.path.join(os.getcwd(), "reports")
        if os.path.isdir(allure_dir):
            results, session = build_data(allure_dir)

            rows = []
            count = 0
            for item in results:
                count += 1
                single_row = [
                    count,
                    item["name"],
                    item["status"],
                    item.get("statusDetails"),
                ]
                rows.append(single_row)
            write_to_csv(rows=rows)

            report_date = session["stop"]
            pass_count = str(session["results"]["passed"])
            fail_count = str(session["results"]["failed"])
            skip_count = str(session["results"]["skipped"])
            error_count = str(session["results"]["broken"])
            total_tests = str(session["total"])

            df = pd.read_csv("records.csv")
            env_details = dict()
            if os.getenv("DSM_VERSION"):
                env_details["DSM Version"] = os.getenv("DSM_VERSION")
            if os.getenv("URL"):
                env_details["URL"] = os.getenv("URL")
            if os.getenv("BROWSER"):
                env_details["BROWSER"] = os.getenv("BROWSER")
            html_table_blue_light = build_table(
                df,
                "blue_light",
                report_date,
                pass_count,
                fail_count,
                skip_count,
                error_count,
                total_tests,
                test_info=env_details,
            )
            with open("reports/index.html", "w") as f:
                f.write(html_table_blue_light)
    except Exception as e:
        logger.info(f"Failed to generate html report: {e}")
