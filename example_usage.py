#!/usr/bin/env python3
"""
Example script showing how to use the Morningstar scraper.
"""

from morningstar_scraper import MorningstarScraper
import json

def main():
    # Initialize the scraper
    scraper = MorningstarScraper()
    
    # Example fund ID
    fund_id = "0P0000RZ3F"
    
    print(f"Scraping data for fund: {fund_id}")
    print("=" * 50)
    
    # Scrape the data
    result = scraper.scrape_fund_data(fund_id)
    
    # Display results
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Fund ID: {result['fund_id']}")
        print(f"Fund Name: {result['name'] or 'Not found'}")
        print(f"NAV: {result['nav'] or 'Not found'}")
        print(f"Currency: {result['currency'] or 'Not found'}")
        print(f"NAV Date: {result['nav_date'] or 'Not found'}")
        
        if result['raw_data']:
            print("\nAdditional Data:")
            print(json.dumps(result['raw_data'], indent=2))

if __name__ == "__main__":
    main()