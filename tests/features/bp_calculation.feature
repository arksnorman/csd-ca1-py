Feature: Blood Pressure Category Calculation
  As a healthcare professional
  I want to calculate blood pressure categories
  So that I can quickly assess patient health status

  Background:
    Given the BP Calculator application is running

  Scenario: Calculate Low Blood Pressure
    Given I have a systolic pressure of 85
    And I have a diastolic pressure of 55
    When I calculate the BP category
    Then the category should be "Low Blood Pressure"

  Scenario: Calculate Ideal Blood Pressure
    Given I have a systolic pressure of 110
    And I have a diastolic pressure of 70
    When I calculate the BP category
    Then the category should be "Ideal Blood Pressure"

  Scenario: Calculate Pre-High Blood Pressure from Systolic
    Given I have a systolic pressure of 130
    And I have a diastolic pressure of 75
    When I calculate the BP category
    Then the category should be "Pre-High Blood Pressure"

  Scenario: Calculate Pre-High Blood Pressure from Diastolic
    Given I have a systolic pressure of 115
    And I have a diastolic pressure of 85
    When I calculate the BP category
    Then the category should be "Pre-High Blood Pressure"

  Scenario: Calculate High Blood Pressure
    Given I have a systolic pressure of 150
    And I have a diastolic pressure of 95
    When I calculate the BP category
    Then the category should be "High Blood Pressure"

  Scenario Outline: Calculate various BP categories
    Given I have a systolic pressure of <systolic>
    And I have a diastolic pressure of <diastolic>
    When I calculate the BP category
    Then the category should be "<category>"

    Examples:
      | systolic | diastolic | category                   |
      | 85       | 55        | Low Blood Pressure         |
      | 90       | 60        | Ideal Blood Pressure       |
      | 119      | 79        | Ideal Blood Pressure       |
      | 120      | 80        | Pre-High Blood Pressure    |
      | 139      | 89        | Pre-High Blood Pressure    |
      | 140      | 90        | High Blood Pressure        |
      | 160      | 100       | High Blood Pressure        |
