"""End-to-end tests using Playwright"""

import pytest
from playwright.sync_api import Page, expect


# Base URL for the application
BASE_URL = "http://localhost:5000"


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


class TestBPCalculatorE2E:
    """E2E tests for BP Calculator"""

    def test_page_loads_correctly(self, page: Page):
        """Test that the main page loads with all expected elements"""
        page.goto(BASE_URL)

        # Check page title
        expect(page).to_have_title("BP Category Calculator - BPCalculator")

        # Check heading
        expect(page.locator("h4")).to_contain_text("BP Category Calculator")

        # Check form elements exist
        expect(page.locator("#systolic")).to_be_visible()
        expect(page.locator("#diastolic")).to_be_visible()
        expect(page.locator("input[type='submit']")).to_be_visible()

    def test_initial_values_displayed(self, page: Page):
        """Test that initial values are pre-filled"""
        page.goto(BASE_URL)

        # Check initial values
        systolic_input = page.locator("#systolic")
        diastolic_input = page.locator("#diastolic")

        expect(systolic_input).to_have_value("100")
        expect(diastolic_input).to_have_value("60")

    def test_calculate_ideal_blood_pressure(self, page: Page):
        """Test calculating ideal blood pressure"""
        page.goto(BASE_URL)

        # Fill in values
        page.fill("#systolic", "110")
        page.fill("#diastolic", "70")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check result
        expect(page.locator("body")).to_contain_text("Ideal Blood Pressure")

    def test_calculate_low_blood_pressure(self, page: Page):
        """Test calculating low blood pressure"""
        page.goto(BASE_URL)

        # Fill in values
        page.fill("#systolic", "85")
        page.fill("#diastolic", "55")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check result
        expect(page.locator("body")).to_contain_text("Low Blood Pressure")

    def test_calculate_pre_high_blood_pressure(self, page: Page):
        """Test calculating pre-high blood pressure"""
        page.goto(BASE_URL)

        # Fill in values
        page.fill("#systolic", "130")
        page.fill("#diastolic", "85")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check result
        expect(page.locator("body")).to_contain_text("Pre-High Blood Pressure")

    def test_calculate_high_blood_pressure(self, page: Page):
        """Test calculating high blood pressure"""
        page.goto(BASE_URL)

        # Fill in values
        page.fill("#systolic", "150")
        page.fill("#diastolic", "95")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check result
        expect(page.locator("body")).to_contain_text("High Blood Pressure")

    def test_validation_systolic_too_low(self, page: Page):
        """Test validation error for systolic too low"""
        page.goto(BASE_URL)

        # Fill in invalid values
        page.fill("#systolic", "65")
        page.fill("#diastolic", "70")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check error message
        expect(page.locator("body")).to_contain_text("Invalid Systolic Value")

    def test_validation_systolic_too_high(self, page: Page):
        """Test validation error for systolic too high"""
        page.goto(BASE_URL)

        # Fill in invalid values
        page.fill("#systolic", "195")
        page.fill("#diastolic", "70")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check error message
        expect(page.locator("body")).to_contain_text("Invalid Systolic Value")

    def test_validation_diastolic_too_low(self, page: Page):
        """Test validation error for diastolic too low"""
        page.goto(BASE_URL)

        # Fill in invalid values
        page.fill("#systolic", "120")
        page.fill("#diastolic", "35")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check error message
        expect(page.locator("body")).to_contain_text("Invalid Diastolic Value")

    def test_validation_diastolic_too_high(self, page: Page):
        """Test validation error for diastolic too high"""
        page.goto(BASE_URL)

        # Fill in invalid values
        page.fill("#systolic", "120")
        page.fill("#diastolic", "105")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check error message
        expect(page.locator("body")).to_contain_text("Invalid Diastolic Value")

    def test_validation_systolic_not_greater_than_diastolic(self, page: Page):
        """Test validation error when systolic <= diastolic"""
        page.goto(BASE_URL)

        # Fill in invalid values
        page.fill("#systolic", "80")
        page.fill("#diastolic", "85")

        # Submit form
        page.click("input[type='submit']")

        # Wait for response
        page.wait_for_load_state("networkidle")

        # Check error message
        expect(page.locator("body")).to_contain_text(
            "Systolic must be greater than Diastolic"
        )

    def test_navigation_to_privacy_page(self, page: Page):
        """Test navigation to privacy page"""
        page.goto(BASE_URL)

        # Click privacy link
        page.click("text=Privacy")

        # Wait for navigation
        page.wait_for_load_state("networkidle")

        # Check we're on privacy page
        expect(page).to_have_url(f"{BASE_URL}/privacy")
        expect(page.locator("h1")).to_contain_text("Privacy Policy")

    def test_navigation_back_to_home(self, page: Page):
        """Test navigation from privacy back to home"""
        page.goto(f"{BASE_URL}/privacy")

        # Click BP Calculator link (home link)
        page.click("text=BP Calculator")

        # Wait for navigation
        page.wait_for_load_state("networkidle")

        # Check we're on home page
        expect(page).to_have_url(f"{BASE_URL}/")
        expect(page.locator("h4")).to_contain_text("BP Category Calculator")

    def test_multiple_calculations(self, page: Page):
        """Test performing multiple calculations in sequence"""
        page.goto(BASE_URL)

        # First calculation
        page.fill("#systolic", "110")
        page.fill("#diastolic", "70")
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_contain_text("Ideal Blood Pressure")

        # Second calculation
        page.fill("#systolic", "150")
        page.fill("#diastolic", "95")
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_contain_text("High Blood Pressure")

        # Third calculation
        page.fill("#systolic", "85")
        page.fill("#diastolic", "55")
        page.click("input[type='submit']")
        page.wait_for_load_state("networkidle")
        expect(page.locator("body")).to_contain_text("Low Blood Pressure")

    def test_responsive_layout(self, page: Page):
        """Test that layout is responsive"""
        page.goto(BASE_URL)

        # Test different viewport sizes
        page.set_viewport_size({"width": 375, "height": 667})  # Mobile
        expect(page.locator("#systolic")).to_be_visible()

        page.set_viewport_size({"width": 768, "height": 1024})  # Tablet
        expect(page.locator("#systolic")).to_be_visible()

        page.set_viewport_size({"width": 1920, "height": 1080})  # Desktop
        expect(page.locator("#systolic")).to_be_visible()
