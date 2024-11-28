Feature: Register
	"""
	Register feature tests for registration success and failure
	"""

	Scenario: Success registration test
		Given I navigate to register page
		And I enter unused username, email and password
		When I click on Submit button
		Then Registration is successful

	Scenario: Reusing username
		Given I navigate to register page
		And I enter used username, email and password
		When I click on Submit button
		Then Registration is unsuccessful

	Scenario: Missing password
		Given I navigate to register page
		And I enter a username, email and no password
		When I click on Submit button
		Then Registration is unsuccessful