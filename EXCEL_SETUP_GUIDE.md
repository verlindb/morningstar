# Excel Macro Setup Guide

## Step-by-Step Instructions

### 1. Prepare Your Environment

1. **Install Python**: Download and install Python from https://python.org
2. **Install Dependencies**: Open Command Prompt and run:
   ```
   pip install requests beautifulsoup4 lxml
   ```

### 2. Setup Excel Macro

1. **Open Excel** and create a new workbook
2. **Enable Developer Tab**:
   - Go to `File` → `Options` → `Customize Ribbon`
   - Check "Developer" in the right panel
   - Click OK

3. **Open VBA Editor**:
   - Click `Developer` tab → `Visual Basic`
   - Or press `Alt + F11`

4. **Insert Module**:
   - Right-click on VBAProject in the left panel
   - Select `Insert` → `Module`

5. **Copy Code**:
   - Open `morningstar_excel_macro.vba` in a text editor
   - Copy all the code
   - Paste it into the VBA editor

### 3. Configure Paths

Update these variables in the macro if needed:

```vba
pythonPath = "python"  ' Change to full path if needed
scriptPath = ThisWorkbook.Path & "\morningstar_scraper.py"
```

### 4. Save and Test

1. **Save as Macro-Enabled Workbook**:
   - Save as `.xlsm` format
   - Place `morningstar_scraper.py` in the same folder

2. **Test the Macro**:
   - Put `0P0000RZ3F` in cell A1
   - Run the `GetMorningstarData` macro
   - Check results in cells below

### 5. Create Button (Optional)

1. **Insert Button**:
   - Go to `Developer` → `Insert` → `Button`
   - Draw button on worksheet
   - Assign `GetMorningstarData` macro

2. **Format Button**:
   - Right-click button → `Edit Text`
   - Change text to "Get Fund Data"

## Usage

1. Enter fund ID in cell A1 (e.g., `0P0000RZ3F`)
2. Click the button or run the macro
3. Results will appear in cells A3 and below

## Troubleshooting

### Common Issues

1. **"Python not found"**:
   - Install Python from python.org
   - Add Python to PATH during installation
   - Or use full path like `C:\Python39\python.exe`

2. **"Module not found"**:
   - Install required packages: `pip install requests beautifulsoup4 lxml`

3. **"Script not found"**:
   - Ensure `morningstar_scraper.py` is in the same folder as Excel file
   - Check the `scriptPath` variable in the macro

4. **Macro security**:
   - Go to `File` → `Options` → `Trust Center` → `Trust Center Settings`
   - Enable macros for this workbook

### Testing Python Script

Test the Python script separately:

```bash
python morningstar_scraper.py 0P0000RZ3F
```

This should return JSON data if everything is working correctly.

## Advanced Usage

### Multiple Fund IDs

To scrape multiple funds, modify the macro to read from a range:

```vba
For Each cell In Range("A1:A10")
    If cell.Value <> "" Then
        ' Process each fund ID
    End If
Next cell
```

### Scheduled Updates

Use Excel's built-in scheduling or Windows Task Scheduler to run the macro automatically.

### Error Logging

Add error logging to track failed requests:

```vba
Open "error_log.txt" For Append As #1
Print #1, Now() & " - " & Err.Description
Close #1
```