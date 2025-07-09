# Morningstar Fund Data Scraper

This project provides a complete solution for scraping Morningstar fund data, specifically designed to extract NAV (Net Asset Value) and fund name information. It includes both a Python scraper and an Excel VBA macro for easy integration.

## Features

- **Python Scraper**: Robust web scraping using requests and BeautifulSoup
- **Excel Integration**: VBA macro for direct Excel usage
- **Error Handling**: Comprehensive error handling and validation
- **Flexible Input**: Support for different fund IDs and country codes
- **JSON Output**: Structured data output for easy parsing

## Quick Start

### Prerequisites

- Python 3.7+ installed
- Excel (for VBA macro usage)
- Internet connection

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/verlindb/morningstar.git
   cd morningstar
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Python Script

Run the scraper directly from command line:

```bash
python morningstar_scraper.py 0P0000RZ3F
```

Example output:
```json
{
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
```

### Excel VBA Macro

1. **Setup**:
   - Open Excel
   - Press `Alt + F11` to open VBA editor
   - Insert a new module (`Insert` → `Module`)
   - Copy and paste the code from `morningstar_excel_macro.vba`

2. **Usage**:
   - Place the fund ID in cell A1 (e.g., `0P0000RZ3F`)
   - Run the `GetMorningstarData` macro
   - Results will appear in the worksheet

3. **Configuration**:
   - Update the `pythonPath` variable if Python is not in your PATH
   - Ensure `morningstar_scraper.py` is in the same directory as your Excel file

## File Structure

```
morningstar/
├── morningstar_scraper.py      # Main Python scraper
├── morningstar_excel_macro.vba # Excel VBA macro
├── test_scraper.py             # Test script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## API Reference

### MorningstarScraper Class

#### `scrape_fund_data(fund_id, country_code='nl')`

Scrapes fund data from Morningstar.

**Parameters:**
- `fund_id` (str): The fund identifier (e.g., '0P0000RZ3F')
- `country_code` (str): Country code for the Morningstar site (default: 'nl')

**Returns:**
- `dict`: Fund data including name, NAV, currency, date, and raw data

**Example:**
```python
from morningstar_scraper import MorningstarScraper

scraper = MorningstarScraper()
result = scraper.scrape_fund_data('0P0000RZ3F')
print(f"Fund: {result['name']}")
print(f"NAV: {result['nav']} {result['currency']}")
```

## Excel Macro Functions

### `GetMorningstarData()`

Main macro function that:
1. Reads fund ID from cell A1
2. Calls Python scraper
3. Displays results in formatted cells

### `SetupExample()`

Helper function to set up example data for testing.

## Testing

Run the test script to validate the scraper:

```bash
python test_scraper.py
```

## Error Handling

The scraper includes comprehensive error handling:

- **Network errors**: Timeout and connection issues
- **Parsing errors**: Invalid HTML or missing data
- **Invalid fund IDs**: Proper error messages
- **Missing dependencies**: Clear installation instructions

## Troubleshooting

### Common Issues

1. **Python not found**: Update `pythonPath` in the VBA macro
2. **Dependencies missing**: Run `pip install -r requirements.txt`
3. **Script path issues**: Ensure `morningstar_scraper.py` is in the correct location
4. **Network issues**: Check internet connection and firewall settings

### Excel Macro Issues

1. **Macro security**: Enable macros in Excel settings
2. **Path issues**: Use absolute paths if relative paths don't work
3. **Python path**: Verify Python installation and PATH variable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is provided as-is for educational and personal use. Please respect Morningstar's terms of service and rate limits when using this scraper.

## Disclaimer

This tool is for educational purposes. Users are responsible for complying with Morningstar's terms of service and applicable laws. The authors are not responsible for any misuse of this tool.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the error messages
3. Open an issue on GitHub