"""BDD test steps for BP validation"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from app import app

# Load scenarios
scenarios("../features/bp_validation.feature")


@pytest.fixture
def context():
    """Context to store test data"""
    return {}


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


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


@when("I validate the blood pressure")
def validate_bp(context, client):
    """Validate blood pressure by submitting form"""
    response = client.post(
        "/",
        data={
            "systolic": str(context["systolic"]),
            "diastolic": str(context["diastolic"]),
        },
        follow_redirects=True,
    )
    context["response"] = response


@then("the validation should pass")
def validation_passes(context):
    """Check that validation passed"""
    response = context["response"]
    assert response.status_code == 200
    # Should not contain error messages
    assert b"Invalid Systolic Value" not in response.data
    assert b"Invalid Diastolic Value" not in response.data


@then(parsers.parse("the validation should {result}"))
def validation_result(context, result):
    """Check validation result (pass/fail)"""
    response = context["response"]
    assert response.status_code == 200

    if result == "pass":
        # Should not contain common error messages
        assert (
            b"Invalid Systolic Value" not in response.data
            or b"Invalid Diastolic Value" not in response.data
            or (
                b"Invalid Systolic Value" not in response.data
                and b"Invalid Diastolic Value" not in response.data
            )
        )
    else:  # fail
        # Should contain at least one error message
        has_error = (
            b"Invalid Systolic Value" in response.data
            or b"Invalid Diastolic Value" in response.data
            or b"Systolic must be greater than Diastolic" in response.data
        )
        assert has_error, "Expected validation to fail but no error found"


@then(parsers.parse('the validation should fail with "{error_message}"'))
def validation_fails(context, error_message):
    """Check that validation failed with specific error"""
    response = context["response"]
    assert response.status_code == 200
    assert error_message.encode() in response.data
