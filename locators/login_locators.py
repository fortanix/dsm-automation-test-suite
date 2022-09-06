from selenium.webdriver.common.by import By

emailInput = (By.CSS_SELECTOR, "input[name=email]")
passwordInput = (By.CSS_SELECTOR, "input[name=password]")
loginSuccess = (
    By.CSS_SELECTOR,
    "[data-label=login-success], .dashboard .apps-progress-bar",
)
dashboardPage = (By.CSS_SELECTOR, ".dashboard")
loginError = (By.CSS_SELECTOR, ".errors")
loginWithOutSSO = (By.CSS_SELECTOR, ".frm-login .btn-most-simple")
loginBtn = (By.CSS_SELECTOR, ".log-in-action:not(disabled)")

authUserMenu = (By.CSS_SELECTOR, "[data-label='toggle-authuser-menu']")
signOut = (By.CSS_SELECTOR, "[data-label='action-logout']")
selectAccount = (By.XPATH, "//*[@data-id='ACCOUNT_ID'] | //*[@class='account__name']")
loadMoreBtn = (By.CSS_SELECTOR, ".accounts-list__load-more")

signUpLink = (By.CSS_SELECTOR, "a[class*='sign-up']")
firstName = (By.CSS_SELECTOR, "input[name='name']:nth-child(1)")
lastName = (By.CSS_SELECTOR, "input[name='name']:nth-child(2)")
retypePasswordInput = (By.CSS_SELECTOR, "input[name=password_copy]")

signupBtn = (By.CSS_SELECTOR, "[type='submit']")
versionText = (By.CSS_SELECTOR, ".ccm-footer .version")

# Microsoft Login
loginWithSSOBtn = (By.CSS_SELECTOR, ".sso-login")
msEmailInput = (By.CSS_SELECTOR, "input[name='loginfmt']")
msPasswordInput = (By.CSS_SELECTOR, "[name='passwd']")
msSignInNextBtn = (By.CSS_SELECTOR, ".win-button")
msAcceptBtn = (By.CSS_SELECTOR, "[value='Accept']")
