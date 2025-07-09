Sub GetMorningstarData()
    '
    ' GetMorningstarData Macro
    ' This macro scrapes Morningstar fund data using Python
    ' 
    ' Instructions:
    ' 1. Install Python with pip
    ' 2. Install required packages: pip install requests beautifulsoup4 lxml
    ' 3. Place morningstar_scraper.py in the same directory as this Excel file
    ' 4. Enter fund ID in cell A1
    ' 5. Run this macro
    '
    
    Dim fundId As String
    Dim pythonPath As String
    Dim scriptPath As String
    Dim command As String
    Dim shell As Object
    Dim exec As Object
    Dim result As String
    Dim jsonData As String
    
    ' Configuration - Update these paths as needed
    pythonPath = "python"  ' Or full path like "C:\Python39\python.exe"
    scriptPath = ThisWorkbook.Path & "\morningstar_scraper.py"
    
    ' Get fund ID from cell A1
    fundId = Trim(Range("A1").Value)
    
    ' Validate input
    If fundId = "" Then
        MsgBox "Please enter a fund ID in cell A1", vbExclamation
        Exit Sub
    End If
    
    ' Clear previous results
    Range("A3:Z100").Clear
    
    ' Show progress
    Range("A3").Value = "Scraping data for fund: " & fundId
    Range("A4").Value = "Please wait..."
    Application.ScreenUpdating = False
    
    ' Create shell object
    Set shell = CreateObject("WScript.Shell")
    
    ' Build command
    command = pythonPath & " """ & scriptPath & """ " & fundId
    
    ' Execute Python script
    On Error GoTo ErrorHandler
    Set exec = shell.Exec(command)
    
    ' Wait for completion and get result
    Do While exec.Status = 0
        DoEvents
        Application.Wait DateAdd("s", 1, Now)
    Loop
    
    ' Get the output
    result = exec.StdOut.ReadAll
    
    ' Parse JSON result
    If result <> "" Then
        Call ParseJsonResult(result)
    Else
        Range("A4").Value = "No data received"
    End If
    
    Application.ScreenUpdating = True
    Exit Sub
    
ErrorHandler:
    Application.ScreenUpdating = True
    MsgBox "Error: " & Err.Description & vbCrLf & vbCrLf & _
           "Make sure Python is installed and the script path is correct:" & vbCrLf & _
           scriptPath, vbCritical
    Range("A4").Value = "Error occurred"
End Sub

Private Sub ParseJsonResult(jsonResult As String)
    '
    ' Parse JSON result and display in Excel
    '
    Dim lines() As String
    Dim i As Integer
    Dim currentRow As Integer
    Dim fundName As String
    Dim navValue As String
    Dim currency As String
    Dim navDate As String
    
    ' Split result into lines
    lines = Split(jsonResult, vbCrLf)
    currentRow = 3
    
    ' Clear status
    Range("A4").Value = ""
    
    ' Parse JSON manually (simple approach for basic data)
    For i = 0 To UBound(lines)
        If InStr(lines(i), """name"":") > 0 Then
            fundName = ExtractJsonValue(lines(i))
        ElseIf InStr(lines(i), """nav"":") > 0 Then
            navValue = ExtractJsonValue(lines(i))
        ElseIf InStr(lines(i), """currency"":") > 0 Then
            currency = ExtractJsonValue(lines(i))
        ElseIf InStr(lines(i), """nav_date"":") > 0 Then
            navDate = ExtractJsonValue(lines(i))
        ElseIf InStr(lines(i), """error"":") > 0 Then
            Range("A" & currentRow).Value = "Error: " & ExtractJsonValue(lines(i))
            currentRow = currentRow + 1
        End If
    Next i
    
    ' Display results in a formatted way
    Range("A3").Value = "Fund Data Results:"
    Range("A4").Value = "Fund ID:"
    Range("B4").Value = Range("A1").Value
    
    If fundName <> "" Then
        Range("A5").Value = "Fund Name:"
        Range("B5").Value = fundName
    End If
    
    If navValue <> "" Then
        Range("A6").Value = "NAV:"
        Range("B6").Value = navValue
        If currency <> "" Then
            Range("C6").Value = currency
        End If
    End If
    
    If navDate <> "" Then
        Range("A7").Value = "NAV Date:"
        Range("B7").Value = navDate
    End If
    
    ' Format the results nicely
    Range("A3:A7").Font.Bold = True
    Range("A3:C7").Borders.LineStyle = xlContinuous
    
    ' Add instructions
    Range("A9").Value = "Instructions:"
    Range("A10").Value = "1. Enter fund ID in cell A1"
    Range("A11").Value = "2. Run the GetMorningstarData macro"
    Range("A12").Value = "3. Results will appear above"
    Range("A9:A12").Font.Italic = True
    
End Sub

Private Function ExtractJsonValue(jsonLine As String) As String
    '
    ' Extract value from a JSON line
    '
    Dim startPos As Integer
    Dim endPos As Integer
    Dim value As String
    
    ' Find the colon
    startPos = InStr(jsonLine, ":")
    If startPos > 0 Then
        ' Find the opening quote
        startPos = InStr(startPos, jsonLine, """")
        If startPos > 0 Then
            startPos = startPos + 1
            ' Find the closing quote
            endPos = InStr(startPos, jsonLine, """")
            If endPos > 0 Then
                value = Mid(jsonLine, startPos, endPos - startPos)
            End If
        Else
            ' Handle non-string values (numbers, null)
            value = Trim(Mid(jsonLine, InStr(jsonLine, ":") + 1))
            ' Remove comma and whitespace
            value = Replace(value, ",", "")
            value = Trim(value)
        End If
    End If
    
    ExtractJsonValue = value
End Function

Sub SetupExample()
    '
    ' Setup example data for testing
    '
    Range("A1").Value = "0P0000RZ3F"
    Range("A1").Font.Bold = True
    Range("A2").Value = "Enter fund ID above and run GetMorningstarData macro"
    Range("A2").Font.Italic = True
End Sub