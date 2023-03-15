Sub UnderlineCardOpenAI()
    Application.ScreenUpdating = False
    Dim StartParagraph As Word.paragraph
    Dim start As Long
    Set StartParagraph = Selection.paragraphs(1)
    StartParagraph.range.Select
    start = Selection.start
    
    Dim TagText As String
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    
    Dim BodyText As String
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.paragraphs(1).Next(2)
    Dim locStart As Long
    Dim locEnd As Long
    Dim paragraphs As String
    paragraphs = "0"
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        BodyText = BodyText & paragraph.range.Text
        paragraphs = paragraphs & "," & CStr(paragraph.range.End)
        Set paragraph = paragraph.Next(1)
    Loop
    
    locEnd = paragraph.Previous(1).range.End

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        MsgBox "Invalid card"
        Exit Sub
    End If
    
    Result = AppleScriptTask("openaipythoninterface.scpt", "openaihandler", TagText & "$$$" & BodyText & "$$$underline$$$n" & "$$$" & paragraphs)
    
    Result = Replace(Result, "[", "")
    Result = Replace(Result, "]", "")
    
    resultArr = Split(Result, "), ")
    UnderlineTextAsRanges resultArr, "Underline", locStart, locEnd
    
    Application.ScreenUpdating = True
End Sub

Sub EmphasizeCardOpenAI()
    Application.ScreenUpdating = False
    Dim StartParagraph As Word.paragraph
    Dim start As Long
    Set StartParagraph = Selection.paragraphs(1)
    StartParagraph.range.Select
    start = Selection.start
    
    Dim TagText As String
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    
    Dim BodyText As String
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.paragraphs(1).Next(2)
    Dim locStart As Long
    Dim locEnd As Long
    Dim paragraphs As String
    paragraphs = "0"
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        BodyText = BodyText & paragraph.range.Text
        paragraphs = paragraphs & "," & CStr(paragraph.range.End)
        Set paragraph = paragraph.Next(1)
    Loop
    
    locEnd = paragraph.Previous(1).range.End

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        MsgBox "Invalid card"
        Exit Sub
    End If

    Dim startLocation As Long
    Dim endLocation As Long
    
    startLocation = locStart
    endLocation = locEnd

    UnderlineText = ""
    Dim range As Word.range
    Set range = ActiveDocument.range(start:=locStart, End:=locEnd)
    
    ' Set formatting conditions
    range.Find.ClearFormatting
    range.Find.Font.Underline = wdUnderlineSingle
    range.Find.Wrap = wdFindStop
    range.Find.Text = ""

    ' Initialize the search
    Dim found As Boolean
    found = range.Find.Execute

    ' Loop through the found underlined phrases
    While found
        If Len(UnderlineText) > 0 Then
            UnderlineText = UnderlineText & ", "
        End If
        
        UnderlineText = UnderlineText & Trim(range.Text)
        
        ' Set the new search range and execute the search again
        range.start = range.End
        range.End = locEnd
        found = range.Find.Execute
    Wend

    If Len(UnderlineText) < 10 Then
        Application.ScreenUpdating = True
        MsgBox "Invalid underlining"
        Exit Sub
    End If
    
    Result = AppleScriptTask("openaipythoninterface.scpt", "openaihandler", TagText & "$$$" & BodyText & "$$$emphasis$$$" & UnderlineText & "$$$" & paragraphs)
    
    Result = Replace(Result, "[", "")
    Result = Replace(Result, "]", "")

    resultArr = Split(Result, "), ")
    UnderlineTextAsRanges resultArr, "Emphasis", startLocation, endLocation
    
    Application.ScreenUpdating = True
End Sub

Sub HighlightCardOpenAI()
    Application.ScreenUpdating = False
    Dim StartParagraph As Word.paragraph
    Dim start As Long
    Set StartParagraph = Selection.paragraphs(1)
    StartParagraph.range.Select
    start = Selection.start
    
    Dim TagText As String
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    
    Dim BodyText As String
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.paragraphs(1).Next(2)
    Dim locStart As Long
    Dim locEnd As Long
    Dim paragraphs As String
    paragraphs = "0"
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        BodyText = BodyText & paragraph.range.Text
        paragraphs = paragraphs & "," & CStr(paragraph.range.End)
        Set paragraph = paragraph.Next(1)
    Loop
    
    locEnd = paragraph.Previous(1).range.End

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        MsgBox "Invalid card"
        Exit Sub
    End If

    Dim startLocation As Long
    Dim endLocation As Long
    
    startLocation = locStart
    endLocation = locEnd

    UnderlineText = ""
    Dim range As Word.range
    Set range = ActiveDocument.range(start:=locStart, End:=locEnd)
    
    ' Set formatting conditions
    range.Find.ClearFormatting
    range.Find.Font.Underline = wdUnderlineSingle
    range.Find.Wrap = wdFindStop
    range.Find.Text = ""

    ' Initialize the search
    Dim found As Boolean
    found = range.Find.Execute

    ' Loop through the found underlined phrases
    While found
        If Len(UnderlineText) > 0 Then
            UnderlineText = UnderlineText & ", "
        End If
        
        UnderlineText = UnderlineText & Trim(range.Text)
        
        ' Set the new search range and execute the search again
        range.start = range.End
        range.End = locEnd
        found = range.Find.Execute
    Wend

    If Len(UnderlineText) < 10 Then
        Application.ScreenUpdating = True
        MsgBox "Invalid underlining"
        Exit Sub
    End If
    
    Result = AppleScriptTask("openaipythoninterface.scpt", "openaihandler", TagText & "$$$" & BodyText & "$$$highlight$$$" & UnderlineText & "$$$" & paragraphs)
    
    Result = Replace(Result, "[", "")
    Result = Replace(Result, "]", "")
    resultArr = Split(Result, "), ")
    UnderlineTextAsRanges resultArr, "Highlight", startLocation, endLocation
    
    Application.ScreenUpdating = True
End Sub

Private Function UnderlineTextAsRanges(DataArr As Variant, style As String, locStart As Long, locEnd As Long)
    Dim rngSearch As Word.range
    Dim found As Boolean
        
    Set rngSearch = ActiveDocument.range(start:=locStart, End:=locEnd)
    
    Dim styleStr As String
    styleStr = style
    If styleStr = "Highlight" Then
        styleStr = "Underline"
    End If
    
    Dim phrase As Variant
    Dim start As Long
    Dim Length As Long
    
    For Each phrase In DataArr
        phrase = Replace(phrase, "(", "")
        phrase = Replace(phrase, ")", "")
        
        phraseSplit = Split(phrase, ", ")
        
        start = CLng(phraseSplit(0))
        Length = CLng(phraseSplit(1))
        
        ' Create a new range for each phrase
        Dim rngPhrase As Word.range
        Set rngPhrase = ActiveDocument.range(start:=locStart + start, End:=locStart + start + Length)
        
        ' MsgBox CStr(locStart + start) & CStr(Length)

        ' Apply the underline style to the range
        If styleStr = "Underline" Then
            rngPhrase.Font.Underline = wdUnderlineSingle
        End If
        
        If styleStr = "Emphasis" Then
            rngPhrase.Font.Bold = True
        End If
        
        If style = "Highlight" Then
            rngPhrase.HighlightColorIndex = wdYellow
            rngPhrase.Font.Size = 11
        End If
    Next phrase
End Function
