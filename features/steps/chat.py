from behave import given, when, then
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time

@given("I navigate to chat page")
def chat_nav(context):
	context.browser.get("http://localhost:5000/")

@given('I write a query in the box')
def write_query(context):
	time.sleep(2)
	context.browser.find_element(By.ID, "message-input").send_keys("Czym zajmował się Józef Piłsudski?")

@when('I click the submit button')
def step_when(context):
	context.browser.find_element(By.ID, "send-button").click()

@then('I get a response from the bot')
def step_then(context):
	time.sleep(10) # should be enough for the response to come back
	messages = context.browser.find_elements(By.CLASS_NAME, "bot-message")
	assert "Józef" in messages[-1] # would be nice if the message was related to the query
