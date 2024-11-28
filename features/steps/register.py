from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time


@given("I navigate to register page")
def visit_register(context):
	context.browser.get("http://localhost:5000/auth/api/register")

@given("I enter unused username, email and password")
def register_new_user(context):
	context.browser.find_element(By.NAME, "username").send_keys(context.randomly_generated_user)
	context.browser.find_element(By.NAME, "password").send_keys(context.randomly_generated_user)
	context.browser.find_element(By.NAME, "confirm_password").send_keys(context.randomly_generated_user)
	context.browser.find_element(By.NAME, "email").send_keys(f"{context.randomly_generated_user}@example.com")

@when("I click on Submit button")
def submit_form(context):
	context.browser.find_elements(By.CLASS_NAME, "btn-primary")[0].click()

@then("Registration is successful")
def assert_register(context):
	wait = WebDriverWait(context.browser, timeout=2)
	wait.until(lambda d : d.current_url != "http://localhost:5000/auth/api/register")
	assert context.browser.current_url == "http://localhost:5000/"

@given("I enter used username, email and password")
def register_old_user(context):
	register_new_user(context) # Reuse the same credentials

@then("Registration is unsuccessful")
def assert_register(context):
	wait = WebDriverWait(context.browser, timeout=2)
	time.sleep(4) # sleep to make sure that the browser has the chance to redirect
	assert context.browser.current_url != "http://localhost:5000/"

@given("I enter a username, email and no password")
def no_password(context):
	context.browser.find_element(By.NAME, "username").send_keys(context.randomly_generated_user)
	context.browser.find_element(By.NAME, "email").send_keys(f"{context.randomly_generated_user}@example.com")