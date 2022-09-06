from selenium.webdriver.common.by import By

addNewGroup = (By.CSS_SELECTOR, ".add-new-group")
groupTitleInput = (By.CSS_SELECTOR, '[name="new-group-title"]')
groupDescriptionInput = (By.CSS_SELECTOR, '[data-label="group-description"] textarea')
saveBtn = (By.CSS_SELECTOR, "[data-label='action-submit']")
groupTitleText = (By.CSS_SELECTOR, ".main-title span.lbl")

# Quorum Policy
addQuorumPolicyBtn = (By.XPATH, '//*[text()="Add quorum policy"]')
addEditQuorumPolicyBtn = (
    By.XPATH,
    "//i[contains(@class,'icon-quorum')]/ancestor::div[1]//*[contains(@class,'btn')]",
)
quorumQtyInput = (By.CSS_SELECTOR, "[name='qty']")
userSearchInput = (By.CSS_SELECTOR, ".choose-people input")
userSelectOption = (
    By.XPATH,
    "//ul[contains(@class,'users-autocomplete')]//*[normalize-space(text())='User']",
)
quorumOperation = (
    By.XPATH,
    "//div[@class='quorum-approval-operation']/label[text("
    ")='QuorumOperation']/preceding-sibling::input[@type='checkbox']",
)
saveQuorumPolicyBtn = (By.CSS_SELECTOR, "[data-modal='confirm-quorum']")
saveQuorumPolicyConfirmBtn = (By.XPATH, "//button[text()='Save']")

searchInput = (By.CSS_SELECTOR, '[placeholder="Search"]')
searchOptions = (
    By.XPATH,
    '//*[@class="ui-menu-item-wrapper" and text()="SEARCH_OPTION"]',
)
firstSearchValue = (By.XPATH, '(//*[@class="group-info"]//*[@class="name"])[1]')
deleteGroup = (By.ID, "delete-group")

# Key Meta Data Policy
addKeyMetaDataPolicyBtn = (By.CSS_SELECTOR, ".key-metadata-policy .btn.manage-policy")
keyDescription = (
    By.CSS_SELECTOR,
    ".key-metadata-policy__item__fields__item:nth-of-type(1)",
)
keyDescriptionBtn = (By.XPATH, "//label[contains(@for,'description-Value')]")
activationDateBtn = (
    By.XPATH,
    "//h5[text()='Activation date']/..//div//label//div[text()='Value']",
)
deactivationDateBtn = (By.XPATH, "//label[contains(@for,'deactivation-date-Value')]")
customAddBtn = (
    By.XPATH,
    "//button[contains(@id,'custom-attribute-add-new-attribute')]",
)
customAttributeBtn = (
    By.XPATH,
    "//label[contains(@for,'custom-attribute-value-Value')]",
)
customAttributeKey = (By.XPATH, "//input[contains(@id,'custom-attribute-name')]")
customAttributeNameTextbox = (
    By.XPATH,
    "//input[contains(@id,'custom-attribute-name')]",
)
customAttributeCloseIcon = (By.CSS_SELECTOR, ".bkl-close--dark")
cannotContainWhitespaceCheckbox = (
    By.XPATH,
    "//label[contains(@for,'custom-attribute-no-white-space')]",
)
restrictValueToOneValueCheckbox = (
    By.XPATH,
    "//label[contains(@for,'custom-attribute-restrict-values')]",
)
customAttributeTextbox = (
    By.XPATH,
    "//input[contains(@id,'custom-attribute-allowed-values')]",
)
handlingKeysAllowedBtn = (By.CSS_SELECTOR, "[for='non-compliance-action-Value']")

# Crypto Policy
addEditCryptoPolicyBtn = (
    By.XPATH,
    "//i[contains(@class,'crypto-policy')]/ancestor::div[1]//*[contains(@class,'btn')]",
)
savePolicyBtn = (By.CSS_SELECTOR, ".set-crypto-policy [class*='action'] .btn")

# Key Undo Policy
addKeyUndoPolicyBtn = (
    By.CSS_SELECTOR,
    ".key-history-policy-summary .btn.manage-policy",
)
editKeyUndoPolicyBtn = (
    By.XPATH,
    "//*[contains(@class,'key-history-policy-summary')]//*[text()='Edit Policy']",
)
deleteKeyUndoPolicyBtn = (By.CSS_SELECTOR, ".policy-footer__delete-btn")
daysKeyUndoPolicyInput = (By.CSS_SELECTOR, "[name='days_qty']")
saveKeyUndoPolicyBtn = (By.CSS_SELECTOR, ".policy-footer .btn")
keyUndoPolicyDetails = (
    By.CSS_SELECTOR,
    ".reversible-period-configuration__description",
)
