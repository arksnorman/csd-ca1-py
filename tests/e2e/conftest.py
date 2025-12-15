"""Playwright configuration for E2E tests"""

import pytest

# from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser_type_launch_args():
    """Browser launch arguments"""
    return {"headless": True, "args": ["--no-sandbox", "--disable-setuid-sandbox"]}
