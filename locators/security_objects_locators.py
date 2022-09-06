from selenium.webdriver.common.by import By

# New Security Object
addSOBtn = (By.CSS_SELECTOR, "a[class*='add-new']")
nameInput = (By.CSS_SELECTOR, "[name='new-so-title']")
descriptionInput = (By.CSS_SELECTOR, "div[data-label='so-description'] textarea")
addDescriptionBtn = (By.CSS_SELECTOR, "[data-label='so-name'] [class*='btn']")

# Create new Group
selectGrpDropDwn = (By.CSS_SELECTOR, ".group-selector .material-icons")
selectGrpDropDwnValues = (By.CSS_SELECTOR, ".group-name--with-icons .name")
createNewGroupBtn = (By.CSS_SELECTOR, '[data-label="create-group"]')
newgGroupTitleInput = (By.CSS_SELECTOR, '[name="new-group-title"]')
newGroupDescriptionInput = (By.CSS_SELECTOR, '[name="new-group-description"]')
modalCreateNewGroupBtn = (By.XPATH, '//*[@class="btn" and text()="Create new group"]')

importRadioBtn = (By.CSS_SELECTOR, ".action-import input")
generateRadioBtn = (By.CSS_SELECTOR, ".action-generate input")

keyTypeLabels = (By.CSS_SELECTOR, ".so-type-editor__type label")
keyTypeInputs = (By.CSS_SELECTOR, ".so-type-editor__type input")
skipTutorialText = (By.XPATH, '//*[text()="Skip tutorial"]')
chooseTypeRadioBtn = (By.CSS_SELECTOR, "input[value='Type']")

keySizeDropDwn = (By.CSS_SELECTOR, '[data-label="key-size"] input.select-dropdown')
keySizeDropDwnValues = (
    By.CSS_SELECTOR,
    '[data-label="key-size"] .dropdown-content span',
)
subGroupSizeDropDwn = (
    By.CSS_SELECTOR,
    '[data-label="subgroup-size"] input.select-dropdown',
)
subGroupSizeDropDwnValues = (
    By.CSS_SELECTOR,
    '[data-label="subgroup-size"] .dropdown-content span',
)
hashingAlgoDropDwn = (
    By.CSS_SELECTOR,
    '[data-label="hashing-alg"] input.select-dropdown',
)
hashingAlgoDropDwnValues = (
    By.CSS_SELECTOR,
    '[data-label="hashing-alg"] .dropdown-content span',
)
generateBtn = (By.CSS_SELECTOR, '[data-label="action-generate"]')

keyTitle = (By.CSS_SELECTOR, ".lbl.key-name")
searchInput = (By.CSS_SELECTOR, ".bkl-search-input__input input")
searchOptions = (
    By.XPATH,
    '//*[@class="bkl-dropdown__menu-item" and text()="SEARCH_OPTION"]',
)
firstSearchValue = (By.XPATH, '(//*[contains(@class, "sobject-name-component")])[1]')

# Copy Key
newObjectBtn = (By.XPATH, '//*[text()="NEW OBJECT"]')
copyKeyBtn = (By.XPATH, '//*[text()="COPY KEY"]')
copyKeyDescriptionInput = (By.CSS_SELECTOR, '[name="description"]')
copyKeySearchGrpName = (By.CSS_SELECTOR, '[placeholder="Search"]')
copyKeyFirstGroupName = (By.XPATH, '(//*[@class="copy-group-list"]//input)[2]')
createCopyKeyBtn = (By.XPATH, '//*[text()="CREATE COPY"]')
copiedKey = (By.XPATH, '(//*[@class="so-info"])[1]')
keyLinkTab = (By.XPATH, '//*[text()="Key Links"]')

# Security Object tabs
keyLinkTab = (By.XPATH, '//*[text()="Key Links"]')
keyLinkHeader = (
    By.XPATH,
    '[name="Key Links"] .collapsible-header',
)  # Source: Copied to

# Rotate Key
rotateKeyBtn = (By.CSS_SELECTOR, ".icon-rotation")
deactivateOriginalKeyChkBx = (
    By.CSS_SELECTOR,
    ".modal-key-rotation__deactivate-rotated-key input",
)
rotateKeyDescription = (By.CSS_SELECTOR, '[name="so-description"]')
rotateKeyModalBtn = (
    By.CSS_SELECTOR,
    ".modal-action .icon-rotation",
)  # Security Object was successfully rotated

# Destroy / Delete Key
destroyKeyBtn = (By.CSS_SELECTOR, '[data-label="sobject-destroy-btn"]')
destroyKeyUnderstandChkbx = (
    By.XPATH,
    '//*[text()="Data encrypted with the object can no longer be used once the object is destroyed"]',
)
destroyDeleteKeyProceedBtn = (By.XPATH, '//button[text()="Proceed"]')
deleteKeyUnderstandChkbx = (
    By.XPATH,
    '//*[text()="The object cannot be restored once it is deleted"]',
)
deleteRotatedKeyUnderstandChkbx = (
    By.XPATH,
    '//*[text()="Data encrypted with the object can no longer be used once the object is deleted"]',
)
deleteKeyBtn = (By.CSS_SELECTOR, '[data-label="sobject-deletion-btn"]')

# Deactivate Key
deactivateNowBtn = (
    By.CSS_SELECTOR,
    '[data-label="sobject-deactivation-deactivate-now"]',
)
deactivationUnderstandChkbx = (
    By.XPATH,
    '//*[text()="Deactivation is irreversible, and the object cannot be activated back"]',
)
deactivationStatusText = (By.CSS_SELECTOR, ".info-block--expires .desc")

alertMsg = (By.CSS_SELECTOR, '[role="alert"]')
saveBtn = (By.XPATH, '//button[text()="Save"]')
