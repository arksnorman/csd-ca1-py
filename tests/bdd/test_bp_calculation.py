"""BDD test steps for BP calculation"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from models.blood_pressure import BloodPressure, BPCategory

# Load scenarios
scenarios("../features/bp_calculation.feature")


@pytest.fixture
def context():
    """Context to store test data"""
    return {}


@given("the BP Calculator application is running")
def app_is_running():
    """Application is running"""
    pass


@given(parsers.parse("I have a systolic pressure of {systolic:d}"))
def set_systolic(context, systolic):
    """Set systolic value"""
    context["systolic"] = systolic


@given(parsers.parse("I have a diastolic pressure of {diastolic:d}"))
def set_diastolic(context, diastolic):
    """Set diastolic value"""
    context["diastolic"] = diastolic


@when("I calculate the BP category")
def calculate_category(context):
    """Calculate BP category"""
    bp = BloodPressure(systolic=context["systolic"], diastolic=context["diastolic"])
    context["category"] = bp.category


@then(parsers.parse('the category should be "{expected_category}"'))
def check_category(context, expected_category):
    """Check the calculated category"""
    actual_category = context["category"].value
    assert (
        actual_category == expected_category
    ), f"Expected '{expected_category}' but got '{actual_category}'"
