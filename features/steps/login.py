from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

@given("I navigate to login page")
def login_nav(context):
	context.browser.get("http://localhost:5000/auth/login")

@given('I enter correct credentials')
def enter_correct_creds(context):
	context.browser.find_element(By.NAME, "username").send_keys(context.randomly_generated_user)
	context.browser.find_element(By.NAME, "password").send_keys(context.randomly_generated_user)

@when('I click on Login button')
def press_login(context):
	context.browser.find_elements(By.CLASS_NAME, "btn-primary")[0].click()

@then('I am logged in')
def check_logged_in(context):
	wait = WebDriverWait(context.browser, timeout=2)
	wait.until(lambda d : d.current_url != "http://localhost:5000/auth/login")
	assert context.browser.current_url == "http://localhost:5000/"

@given('I enter existing username and incorrect password')
def enter_incorrect_creds(context):
	context.browser.find_element(By.NAME, "username").send_keys(context.randomly_generated_user * 2)
	context.browser.find_element(By.NAME, "password").send_keys(context.randomly_generated_user * 2)

@then('I am not logged in')
def check_not_logged_in(context):
	wait = WebDriverWait(context.browser, timeout=2)
	wait.until(lambda d : d.current_url != "http://localhost:5000/auth/login")
	assert context.browser.current_url == "http://localhost:5000/auth/login"