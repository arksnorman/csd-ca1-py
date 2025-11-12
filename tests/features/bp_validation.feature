Feature: Blood Pressure Input Validation
  As a user
  I want the system to validate my blood pressure inputs
  So that I only get results for valid measurements

  Background:
    Given the BP Calculator application is running

  Scenario: Valid systolic and diastolic values
    Given I have a systolic pressure of 120
    And I have a diastolic pressure of 80
    When I validate the blood pressure
    Then the validation should pass

  Scenario: Systolic value too low
    Given I have a systolic pressure of 65
    And I have a diastolic pressure of 70
    When I validate the blood pressure
    Then the validation should fail with "Invalid Systolic Value"

  Scenario: Systolic value too high
    Given I have a systolic pressure of 195
    And I have a diastolic pressure of 70
    When I validate the blood pressure
    Then the validation should fail with "Invalid Systolic Value"

  Scenario: Diastolic value too low
    Given I have a systolic pressure of 120
    And I have a diastolic pressure of 35
    When I validate the blood pressure
    Then the validation should fail with "Invalid Diastolic Value"

  Scenario: Diastolic value too high
    Given I have a systolic pressure of 120
    And I have a diastolic pressure of 105
    When I validate the blood pressure
    Then the validation should fail with "Invalid Diastolic Value"

  Scenario: Systolic must be greater than diastolic
    Given I have a systolic pressure of 80
    And I have a diastolic pressure of 85
    When I validate the blood pressure
    Then the validation should fail with "Systolic must be greater than Diastolic"

  Scenario Outline: Boundary value validation
    Given I have a systolic pressure of <systolic>
    And I have a diastolic pressure of <diastolic>
    When I validate the blood pressure
    Then the validation should <result>

    Examples:
      | systolic | diastolic | result |
      | 70       | 40        | pass   |
      | 69       | 40        | fail   |
      | 190      | 100       | pass   |
      | 191      | 100       | fail   |
      | 120      | 100       | pass   |
      | 120      | 101       | fail   |
