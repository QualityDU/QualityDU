Feature: Login
	"""
	Login tests, require the register feature to have been tested before.
	"""
	Scenario: Success login test
		Given I navigate to login page
		And I enter correct credentials
		When I click on Login button
		Then I am logged in

	Scenario: Incorrect password
		Given I navigate to register page
		And I enter existing username and incorrect password
		When I click on Login button
		Then I am not logged in

	Scenario: Missing password
		Given I navigate to register page
		And I enter a username, email and no password
		When I click on Submit button
		Then Registration is unsuccessful