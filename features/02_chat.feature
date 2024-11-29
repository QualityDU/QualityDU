Feature: Chat
	"""
	Chat tests. Require the login feature to have been tested before to have a logged in user.
	"""
	Scenario: Chat messaging test
		Given I navigate to chat page
		And I write a query in the box
		When I click the submit button
		Then I get a response from the bot