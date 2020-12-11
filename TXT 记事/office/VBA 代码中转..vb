【取cell】
    Range("a1").Value = "test"
    Cells(2, 1).Value = "test2"

【复制行】
Sub renderAll()
    Dim maxRow, curRow, preRow As Integer
    'Dim payslipSheet As Worksheet
    'payslipSheet = Sheets("S-Payslip") ' error
    maxRow = Sheets("复制页").UsedRange.Rows.count
    
    If maxRow < 8 Then
        'MsgBox ("No Data In 复制页", vbOKOnly)
        MsgBox "No Data In 复制页", vbOKOnly
        Exit Sub
    End If
    
    For curRow = 8 To maxRow
        preRow = curRow - 1
        'payslipSheet.Rows(curRow).Insert
        'Debug.Print (curRow & " - " & preRow)
        Sheets("S-Payslip").Range(curRow & ":" & curRow).Insert
        Sheets("S-Payslip").Range(preRow & ":" & preRow).Copy Range(curRow & ":" & curRow)
        Sheets("S-Payroll Report").Range(curRow & ":" & curRow).Insert
        Sheets("S-Payroll Report").Range(preRow & ":" & preRow).Copy Range(curRow & ":" & curRow)
    Next
End Sub
Sub renderAll()
    Dim maxRow, curRow, preRow As Integer
    maxRow = Sheets("复制页").UsedRange.Rows.count
    
    If maxRow < 8 Then
        MsgBox "No Data In 复制页", vbOKOnly
        Exit Sub
    End If
    
    For curRow = 8 To maxRow
        preRow = curRow - 1
        Sheets("S-Payslip").Range(preRow & ":" & preRow).Copy
        Sheets("S-Payslip").Range(curRow & ":" & curRow).Insert shift:=xlDown
        Application.CutCopyMode = False
        Sheets("S-Payroll Report").Range(preRow & ":" & preRow).Copy
        Sheets("S-Payroll Report").Range(curRow & ":" & curRow).Insert shift:=xlDown
        Application.CutCopyMode = False
    Next
End Sub

【清除一些行】
Sub clear()
    Dim startRow, lastRow As Integer
    lastRow = Sheets("S-Payroll Report").UsedRange.Rows.count
    
    If lastRow < 8 Then
        MsgBox "No Data in 'S-Payroll Report' to Clear", vbOKOnly
        Exit Sub
    End If
    For startRow = 8 To lastRow
        'Debug.Print (Mid("asdfg", 0, 2))
        'Debug.Print (Sheets("S-Payroll Report").Range("a" & startRow))
        'Debug.Print (Mid(Sheets("S-Payroll Report").Range("a" & (startRow + 2)), 0, 3))
        If IsNumeric(Sheets("S-Payroll Report").Range("a" & startRow)) _
            And Sheets("S-Payroll Report").Range("a" & (startRow + 1)) = "" Then
            'Debug.Print (Sheets("S-Payroll Report").Range("a" & startRow))
            'Debug.Print (startRow)
            Sheets("S-Payroll Report").Range("8:" & startRow).Delete
            Exit For
        End If
        'Sheets("S-Payroll Report").Range(startRow).Delete
    Next
    
End Sub

【过滤】
Sub clearFilter()
    Call initBefore
    ' need the initialization
    Call init

    Call initAfter
End Sub

Sub lackInfo()
    Call initBefore
    ' need the initialization
    Call init
    
    '' combined filter
    Selection.AutoFilter Field:=8, Criteria1:="=", Operator:=xlAnd, _
        Criteria2:="<>n/a" 'H col blank
    
    Call initAfter
End Sub


' init the filter. use: Call init
Function init()
    If ActiveSheet.AutoFilterMode = False Then
        'ActiveSheet.AutoFilterMode = 0
        'ActiveSheet.UsedRange.AutoFilter
        Range("4:4").AutoFilter
    Else
        ' clear and set filter
        ActiveSheet.AutoFilterMode = False
        'ActiveSheet.UsedRange.AutoFilter
        Range("4:4").AutoFilter
    End If
End Function

Sub initBefore()
    Application.ScreenUpdating = False
    'ActiveSheet.Unprotect
    'ActiveSheet.Protect UserInterfaceOnly:=True
End Sub

Sub initAfter()
    'ActiveSheet.Protect DrawingObjects:=False, Contents:=True, Scenarios:= _
        False, AllowFormattingCells:=True, AllowFormattingColumns:=True, _
        AllowFormattingRows:=True, AllowInsertingColumns:=True, AllowInsertingRows _
        :=True, AllowSorting:=True, AllowFiltering:=True, UserInterfaceOnly:=True
        ' Password:="123",
    Application.ScreenUpdating = True
End Sub
