#!/usr/bin/env python3
"""
Morningstar Fund Data Scraper

This script scrapes fund data from Morningstar, specifically extracting
NAV (Net Asset Value) and fund name information.
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import re
from urllib.parse import urljoin


class MorningstarScraper:
    """Scraper for Morningstar fund data."""
    
    def __init__(self):
        self.base_url = "https://global.morningstar.com"
        self.session = requests.Session()
        # Set headers to mimic a real browser
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
    
    def scrape_fund_data(self, fund_id, country_code='nl'):
        """
        Scrape fund data from Morningstar.
        
        Args:
            fund_id (str): The fund identifier (e.g., '0P0000RZ3F')
            country_code (str): Country code for the Morningstar site (default: 'nl')
            
        Returns:
            dict: Fund data including name, NAV, and other relevant information
        """
        try:
            # Construct the URL
            url = f"{self.base_url}/{country_code}/beleggingen/fondsen/{fund_id}/quote"
            
            # Make the request
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract fund data
            fund_data = self._extract_fund_data(soup, fund_id)
            
            return fund_data
            
        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}
        except Exception as e:
            return {'error': f'Parsing failed: {str(e)}'}
    
    def _extract_fund_data(self, soup, fund_id):
        """Extract fund data from the parsed HTML."""
        fund_data = {
            'fund_id': fund_id,
            'name': None,
            'nav': None,
            'currency': None,
            'nav_date': None,
            'raw_data': {}
        }
        
        try:
            # Extract fund name - try multiple selectors
            name_selectors = [
                'h1.product-name',
                'h1[data-test="product-name"]',
                '.product-name',
                'h1.security-name',
                '.security-name'
            ]
            
            for selector in name_selectors:
                name_elem = soup.select_one(selector)
                if name_elem:
                    fund_data['name'] = name_elem.get_text(strip=True)
                    break
            
            # Extract NAV - try multiple selectors
            nav_selectors = [
                '[data-test="nav-value"]',
                '.nav-value',
                '[data-moduleId="KeyStatistics"] .value',
                '.key-stat-value',
                '.sal-component-number'
            ]
            
            for selector in nav_selectors:
                nav_elem = soup.select_one(selector)
                if nav_elem:
                    nav_text = nav_elem.get_text(strip=True)
                    # Extract numeric value and currency
                    nav_match = re.search(r'([A-Z]{3})\s*([\d,]+\.?\d*)', nav_text)
                    if nav_match:
                        fund_data['currency'] = nav_match.group(1)
                        fund_data['nav'] = nav_match.group(2).replace(',', '')
                        break
                    else:
                        # Try without currency
                        nav_match = re.search(r'([\d,]+\.?\d*)', nav_text)
                        if nav_match:
                            fund_data['nav'] = nav_match.group(1).replace(',', '')
                            break
            
            # Extract NAV date
            date_selectors = [
                '[data-test="nav-date"]',
                '.nav-date',
                '.as-of-date'
            ]
            
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    fund_data['nav_date'] = date_elem.get_text(strip=True)
                    break
            
            # Extract additional data that might be useful
            self._extract_additional_data(soup, fund_data)
            
        except Exception as e:
            fund_data['extraction_error'] = str(e)
        
        return fund_data
    
    def _extract_additional_data(self, soup, fund_data):
        """Extract additional fund data that might be useful."""
        try:
            # Look for key statistics table
            key_stats = soup.find('div', {'data-moduleId': 'KeyStatistics'})
            if key_stats:
                stats = {}
                rows = key_stats.find_all('tr')
                for row in rows:
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= 2:
                        key = cells[0].get_text(strip=True)
                        value = cells[1].get_text(strip=True)
                        stats[key] = value
                fund_data['raw_data']['key_statistics'] = stats
            
            # Look for any JSON data in script tags
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string and 'nav' in script.string.lower():
                    # Try to extract JSON data
                    try:
                        json_match = re.search(r'({.*})', script.string)
                        if json_match:
                            json_data = json.loads(json_match.group(1))
                            fund_data['raw_data']['json_data'] = json_data
                            break
                    except:
                        continue
                        
        except Exception as e:
            fund_data['raw_data']['extraction_error'] = str(e)


def main():
    """Main function for command-line usage."""
    if len(sys.argv) != 2:
        print("Usage: python morningstar_scraper.py <fund_id>")
        print("Example: python morningstar_scraper.py 0P0000RZ3F")
        sys.exit(1)
    
    fund_id = sys.argv[1]
    scraper = MorningstarScraper()
    
    print(f"Scraping fund data for: {fund_id}")
    result = scraper.scrape_fund_data(fund_id)
    
    # Output as JSON for easy parsing by other tools
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()