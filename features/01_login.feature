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
		Given I navigate to login page
		And I enter incorrect credentials
		When I click on Login button
		Then I am not logged in