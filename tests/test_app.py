"""Unit tests for Flask application routes"""

import pytest
from app import app
from models.blood_pressure import BPCategory


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Test the index/home page route"""

    def test_index_get_request(self, client):
        """Test GET request to index page"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"BP Category Calculator" in response.data

    def test_index_initial_values(self, client):
        """Test that initial values are displayed"""
        response = client.get("/")
        assert b'value="100"' in response.data or b'value="100' in response.data
        assert b'value="60"' in response.data or b'value="60' in response.data

    def test_index_post_valid_ideal_bp(self, client):
        """Test POST with valid ideal BP values"""
        response = client.post(
            "/", data={"systolic": "110", "diastolic": "70"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Ideal Blood Pressure" in response.data

    def test_index_post_valid_low_bp(self, client):
        """Test POST with valid low BP values"""
        response = client.post(
            "/", data={"systolic": "85", "diastolic": "55"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Low Blood Pressure" in response.data

    def test_index_post_valid_pre_high_bp(self, client):
        """Test POST with valid pre-high BP values"""
        response = client.post(
            "/", data={"systolic": "130", "diastolic": "85"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Pre-High Blood Pressure" in response.data

    def test_index_post_valid_high_bp(self, client):
        """Test POST with valid high BP values"""
        response = client.post(
            "/", data={"systolic": "150", "diastolic": "95"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"High Blood Pressure" in response.data

    def test_index_post_systolic_too_low(self, client):
        """Test POST with systolic value too low"""
        response = client.post(
            "/", data={"systolic": "65", "diastolic": "70"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Invalid Systolic Value" in response.data

    def test_index_post_systolic_too_high(self, client):
        """Test POST with systolic value too high"""
        response = client.post(
            "/", data={"systolic": "195", "diastolic": "70"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Invalid Systolic Value" in response.data

    def test_index_post_diastolic_too_low(self, client):
        """Test POST with diastolic value too low"""
        response = client.post(
            "/", data={"systolic": "120", "diastolic": "35"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Invalid Diastolic Value" in response.data

    def test_index_post_diastolic_too_high(self, client):
        """Test POST with diastolic value too high"""
        response = client.post(
            "/", data={"systolic": "120", "diastolic": "105"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Invalid Diastolic Value" in response.data

    def test_index_post_systolic_less_than_diastolic(self, client):
        """Test POST with systolic less than or equal to diastolic"""
        response = client.post(
            "/", data={"systolic": "80", "diastolic": "85"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Systolic must be greater than Diastolic" in response.data

    def test_index_post_systolic_equals_diastolic(self, client):
        """Test POST with systolic equal to diastolic"""
        response = client.post(
            "/", data={"systolic": "80", "diastolic": "80"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Systolic must be greater than Diastolic" in response.data

    def test_index_post_missing_systolic(self, client):
        """Test POST with missing systolic value"""
        response = client.post("/", data={"diastolic": "70"}, follow_redirects=True)
        assert response.status_code == 200
        # Should show validation error

    def test_index_post_missing_diastolic(self, client):
        """Test POST with missing diastolic value"""
        response = client.post("/", data={"systolic": "120"}, follow_redirects=True)
        assert response.status_code == 200
        # Should show validation error


class TestPrivacyRoute:
    """Test the privacy page route"""

    def test_privacy_page(self, client):
        """Test privacy page loads successfully"""
        response = client.get("/privacy")
        assert response.status_code == 200
        assert b"Privacy Policy" in response.data


class TestHealthTipsRoute:
    """Test the health tips page route"""

    def test_health_tips_page(self, client):
        """Test health tips page loads successfully"""
        response = client.get("/tips")
        assert response.status_code == 200
        assert b"Health Tips" in response.data
        assert b"Low Blood Pressure" in response.data
        assert b"Ideal Blood Pressure" in response.data
        assert b"Pre-High Blood Pressure" in response.data
        assert b"High Blood Pressure" in response.data


class TestFaviconRoute:
    """Test the favicon route"""

    def test_favicon_returns_204(self, client):
        """Test favicon returns 204 No Content"""
        response = client.get("/favicon.ico")
        assert response.status_code == 204


class TestErrorHandlers:
    """Test error handler routes"""

    def test_404_error(self, client):
        """Test 404 error handler"""
        response = client.get("/nonexistent-page")
        assert response.status_code == 404
        assert b"Error" in response.data


class TestFormValidation:
    """Test form validation edge cases"""

    def test_boundary_values_low(self, client):
        """Test boundary values at low end"""
        response = client.post(
            "/", data={"systolic": "70", "diastolic": "40"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"Low Blood Pressure" in response.data

    def test_boundary_values_high(self, client):
        """Test boundary values at high end"""
        response = client.post(
            "/", data={"systolic": "190", "diastolic": "100"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert b"High Blood Pressure" in response.data

    def test_non_numeric_systolic(self, client):
        """Test non-numeric systolic value"""
        response = client.post(
            "/", data={"systolic": "abc", "diastolic": "70"}, follow_redirects=True
        )
        assert response.status_code == 200
        # Should show validation error

    def test_non_numeric_diastolic(self, client):
        """Test non-numeric diastolic value"""
        response = client.post(
            "/", data={"systolic": "120", "diastolic": "xyz"}, follow_redirects=True
        )
        assert response.status_code == 200
        # Should show validation error
