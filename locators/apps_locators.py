from selenium.webdriver.common.by import By

newAppBtn = (By.CLASS_NAME, "add-new")
appNameInput = (By.CSS_SELECTOR, "[name='new-app-title']")
appTypeSelect = (
    By.CSS_SELECTOR,
    "[data-label='app-name'] .input-field:nth-child(2) input",
)
appTypeOption = (By.XPATH, "//*[@data-label='app-name']//ul//*[text()='AppType']")
appMethodRadioBtn = (
    By.XPATH,
    "//*[@class='app-auth-method']//label[text()='AppMethod']",
)
setAppSecretLink = (By.CLASS_NAME, "secret-size")
secretSizeSelect = (By.CSS_SELECTOR, ".apikey-option input")
secretSizeOption = (By.XPATH, "//*[@class='apikey-option']//ul//*[text()='SecretSize']")
searchGroupInput = (By.CSS_SELECTOR, "[data-label='search-input']")
searchGroupOption = (By.XPATH, "//*[@data-label='items-list']//*[text()='GroupName']")
editgroups = (By.CSS_SELECTOR, "[id='btn-edit-groups']")
certificateTextarea = (By.CSS_SELECTOR, "[data-label='app-certificate'] textarea")
taCertificateTextarea = (
    By.CSS_SELECTOR,
    "[data-label='app-certificate'] .action + textarea",
)
sanTypeSelect = (By.CSS_SELECTOR, ".san-container input")
sanTypeOption = (By.XPATH, "//*[@class='san-container']//ul//*[text()='SANType']")
sanValueInput = (By.NAME, "san-value")
acceptAllCheckbox = (By.CSS_SELECTOR, "[for='accept-all']")
allowMissingCheckbox = (By.CSS_SELECTOR, "[for='allow-missing']")
customerSupportCheckbox = (By.CSS_SELECTOR, "[for='reason-CUSTOMER_INITIATED_SUPPORT']")
customerAccessCheckbox = (By.CSS_SELECTOR, "[for='reason-CUSTOMER_INITIATED_ACCESS']")
issuerInput = (By.CSS_SELECTOR, "[data-label='valid-issuer']")
fetchedSigningKeyRadio = (By.CSS_SELECTOR, ".two-ways span:nth-child(2) label")
keyUrlInput = (By.CSS_SELECTOR, "[data-label='key-url']")
enableOauthToggle = (By.CSS_SELECTOR, ".element")
redirectUrlInput = (By.XPATH, "//input[@name='oauth_redirect_uri']")
directoryTypeSelect = (By.CSS_SELECTOR, ".input-group input.select-dropdown")
directoryTypeOption = (
    By.XPATH,
    "//*[@class='input-group']//span[text()='DirectoryType']",
)
directoryValue = (By.NAME, "oid-value")
saveAppBtn = (By.CSS_SELECTOR, "button[data-label='action-submit']")
appTitle = (By.CSS_SELECTOR, ".app-details__wrapper .main-title .lbl")
deleteAppBtn = (By.ID, "delete-app")
deleteAppConfirmBtn = (By.XPATH, '//*[text()="Delete"]')
