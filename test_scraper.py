#!/usr/bin/env python3
"""
Test script for the Morningstar scraper.
Since the actual site is blocked, this creates a mock test.
"""

import json
import sys
import os
from unittest.mock import Mock, patch

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from morningstar_scraper import MorningstarScraper


def test_scraper_structure():
    """Test that the scraper has the correct structure."""
    scraper = MorningstarScraper()
    
    # Test that required methods exist
    assert hasattr(scraper, 'scrape_fund_data')
    assert hasattr(scraper, '_extract_fund_data')
    assert hasattr(scraper, '_extract_additional_data')
    
    print("✓ Scraper structure test passed")


def test_error_handling():
    """Test error handling with invalid fund ID."""
    scraper = MorningstarScraper()
    
    # Mock a failed request
    with patch('requests.Session.get') as mock_get:
        mock_get.side_effect = Exception("Network error")
        
        result = scraper.scrape_fund_data("INVALID_ID")
        
        # Should return error in result
        assert 'error' in result
        print("✓ Error handling test passed")


def test_fund_data_structure():
    """Test that the fund data structure is correct."""
    scraper = MorningstarScraper()
    
    # Mock successful response
    mock_html = """
    <html>
        <body>
            <h1 class="product-name">Test Fund Name</h1>
            <div data-test="nav-value">EUR 123.45</div>
            <div data-test="nav-date">2023-12-01</div>
        </body>
    </html>
    """
    
    with patch('requests.Session.get') as mock_get:
        mock_response = Mock()
        mock_response.content = mock_html.encode()
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        result = scraper.scrape_fund_data("TEST_ID")
        
        # Check structure
        expected_keys = ['fund_id', 'name', 'nav', 'currency', 'nav_date', 'raw_data']
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
        
        print("✓ Fund data structure test passed")


def create_sample_output():
    """Create sample output for documentation."""
    sample_data = {
        "fund_id": "0P0000RZ3F",
        "name": "Example Fund Name",
        "nav": "123.45",
        "currency": "EUR",
        "nav_date": "2023-12-01",
        "raw_data": {
            "key_statistics": {
                "NAV": "EUR 123.45",
                "Total Assets": "1.2B",
                "Expense Ratio": "0.75%"
            }
        }
    }
    
    print("\nSample output structure:")
    print(json.dumps(sample_data, indent=2))
    return sample_data


if __name__ == "__main__":
    print("Running Morningstar Scraper Tests...")
    print("=" * 50)
    
    try:
        test_scraper_structure()
        test_error_handling()
        test_fund_data_structure()
        
        print("\n" + "=" * 50)
        print("All tests passed! ✓")
        
        # Create sample output
        create_sample_output()
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)