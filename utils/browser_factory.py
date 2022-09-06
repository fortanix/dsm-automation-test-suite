import os
import platform
import shutil

from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.chrome.options import Options as chrome_pref
from selenium.webdriver.firefox.options import Options as firefox_pref
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class BrowserFactory:
    @staticmethod
    def get_browser(browser_name, browser_mode):
        # Add current file dir to PYTHONPATH
        # os.environ['PYTHONPATH'] = '/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
        driver = None
        download_dir = os.path.dirname(os.path.realpath(__file__)) + "/../resources"
        if not os.path.exists(download_dir):
            os.mkdir(download_dir)
        if browser_name == "Chrome":
            chrome_options = chrome_pref()
            chrome_options.add_argument("--window-size=1920x1080")
            if browser_mode == "headless":
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-extensions")
                chrome_options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        elif browser_name == "Firefox":
            firefox_options = firefox_pref()
            firefox_options.add_argument("--window-size=1280x800")
            firefox_options.set_preference("browser.download.folderList", 2)
            firefox_options.set_preference("browser.download.manager.showWhenStarting", False)
            firefox_options.set_preference("browser.download.dir", download_dir)
            if browser_mode == "headless":
                firefox_options.add_argument("-headless")
            driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=firefox_options)
        elif browser_name == "Edge":
            edge_options = EdgeOptions()
            edge_options.use_chromium = True
            edge_options.binary_location = r"/usr/bin/microsoft-edge"
            edge_options.set_capability("platform", "LINUX")
            edge_options.add_argument("disable-gpu")
            edge_options.add_argument("--window-size=1920x1080")
            if browser_mode == "headless":
                edge_options.add_argument("--headless")
                edge_options.add_argument("--no-sandbox")
                edge_options.add_argument("--disable-extensions")
                edge_options.add_argument("--disable-dev-shm-usage")
            driver = Edge(
                options=edge_options,
                executable_path=EdgeChromiumDriverManager().install(),
            )
        else:
            raise Exception('"{}" is not a supported browser'.format(browser_name))
        if browser_name != "Firefox":
            if platform.system() == "Linux":
                params = {"behavior": "allow", "downloadPath": download_dir}
                driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
            else:
                params = {
                    "behavior": "allow",
                    "downloadPath": download_dir.replace("/", "\\"),
                }
                driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
        return driver
