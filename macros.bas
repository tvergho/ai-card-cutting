Attribute VB_Name = "NewMacros"
Function CustomPropExist(WhichDoc As Document, NameOfProp As String) As Boolean
    Dim prop As DocumentProperty
    Dim ret As Boolean
    ret = False
    For Each prop In WhichDoc.CustomDocumentProperties
        If LCase(prop.Name) = LCase(NameOfProp) Then
            ret = True
            Exit For
        End If
    Next
    CustomPropExist = ret
End Function

Public Function getDocumentProperty(NameOfProp As String) As String
    If CustomPropExist(ActiveDocument, NameOfProp) Then
        getDocumentProperty = ActiveDocument.CustomDocumentProperties(NameOfProp).Value
    Else
       getDocumentProperty = ""
    End If
End Function

Public Function URLEncode( _
   StringVal As String, _
   Optional SpaceAsPlus As Boolean = False _
) As String

  Dim StringLen As Long: StringLen = Len(StringVal)

  If StringLen > 0 Then
    ReDim Result(StringLen) As String
    Dim i As Long, CharCode As Integer
    Dim Char As String, Space As String

    If SpaceAsPlus Then Space = "+" Else Space = "%20"

    For i = 1 To StringLen
      Char = Mid$(StringVal, i, 1)
      CharCode = Asc(Char)
      Select Case CharCode
        Case 97 To 122, 65 To 90, 48 To 57, 45, 46, 95, 126
          Result(i) = Char
        Case 32
          Result(i) = Space
        Case 0 To 15
          Result(i) = "%0" & Hex(CharCode)
        Case Else
          Result(i) = "%" & Hex(CharCode)
      End Select
    Next i
    URLEncode = Join(Result, "")
  End If
End Function


Sub UnderlineCardOpenAI()
    Application.ScreenUpdating = False
    
    Dim SelectionStart As Long
    Dim SelectionEnd As Long
    Dim TagText As String
    Dim BodyText As String
    Dim results As String
    
    Dim NextParagraph As paragraph
        
    If Selection.start <> Selection.Paragraphs(1).range.start Then Selection.Paragraphs(1).range.Select
    If Selection.End <> Selection.Paragraphs(1).range.End Then Selection.Paragraphs(1).range.Select
    
    SelectionStart = Selection.start
    SelectionEnd = Selection.End
    TagText = Selection.Text
    
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)

    BodyText = Selection.Paragraphs(1).Next(2).range.Text

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    results = AppleScriptTask("getUnderlines.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$underline")
    results = Replace(results, "[\""", "")
    results = Replace(results, "\""]", "")
    
    resultArr = Split(results, "\"", \""")
    UnderlineText resultArr, "Underline"
    
    Application.ScreenUpdating = True
End Sub

Sub FormatCardOpenAI()
    Dim StartParagraph As Word.paragraph
    Dim start As Long
    Set StartParagraph = Selection.Paragraphs(1)
    start = Selection.start
    
    UnderlineCardOpenAI
    
    StartParagraph.range.Select
    Selection.start = start
    
    EmphasizeCardOpenAI
End Sub

Sub HighlightCardOpenAI()
    Application.ScreenUpdating = False
    
    Dim SelectionStart As Long
    Dim SelectionEnd As Long
    Dim TagText As String
    Dim BodyText As String
    Dim results As String
    
    Dim NextParagraph As paragraph
        
    If Selection.start <> Selection.Paragraphs(1).range.start Then Selection.Paragraphs(1).range.Select
    If Selection.End <> Selection.Paragraphs(1).range.End Then Selection.Paragraphs(1).range.Select
    
    SelectionStart = Selection.start
    SelectionEnd = Selection.End
    TagText = Selection.Text
    
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)

    BodyText = Selection.Paragraphs(1).Next(2).range.Text
    
    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    results = AppleScriptTask("getUnderlines.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$highlight")
    results = Replace(results, "[\""", "")
    results = Replace(results, "\""]", "")
    
    resultArr = Split(results, "\"", \""")
    UnderlineText resultArr, "Highlight"
    
    Application.ScreenUpdating = True
End Sub

Sub UnderlineCardOpenAIV2()
    Application.ScreenUpdating = False
    Dim TagText As String
    Dim BodyText As String
    Dim range As Word.range
    
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.Paragraphs(1).Next(2)
    Dim locStart As Long
    Dim locEnd As Long
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        BodyText = BodyText & paragraph.range.Text & "\n"
        Set paragraph = paragraph.Next(1)
    Loop
    
    locEnd = paragraph.Previous(1).range.End

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    Result = AppleScriptTask("getUnderlinesInChunks.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$underline")
    Result = Replace(Result, "['", "")
    Result = Replace(Result, "']", "")
    
    resultArr = Split(Result, "', '")
    UnderlineTextV2 resultArr, "Underline", locStart, locEnd
    
    Application.ScreenUpdating = True
End Sub

Sub EmphasizeCardOpenAIV2()
    Application.ScreenUpdating = False
    Dim TagText As String
    Dim BodyText As String
    Dim range As Word.range
    
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.Paragraphs(1).Next(2)
    
    Dim locStart As Long
    Dim locEnd As Long
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        Set range = paragraph.range.Duplicate
        range.Select
        Dim SelectionEnd As Long
        SelectionEnd = Selection.End
        
        range.Find.ClearFormatting
        range.Find.Replacement.ClearFormatting
        range.Find.Text = ""
        range.Find.Replacement.Text = ""
        range.Find.Font.Underline = wdUnderlineSingle
        range.Find.Wrap = wdFindStop
        
        Do While range.Find.Execute = True And i < 5
            BodyText = BodyText & " " & range.Text
            range.start = range.End
            range.End = SelectionEnd
        Loop
        
        Set paragraph = paragraph.Next(1)
        BodyText = BodyText & "\n"
    Loop
    
    locEnd = paragraph.Previous(1).range.End

    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    Result = AppleScriptTask("getUnderlinesInChunks.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$underline")
    Result = Replace(Result, "['", "")
    Result = Replace(Result, "']", "")
    
    resultArr = Split(Result, "', '")
    UnderlineTextV2 resultArr, "Emphasis", locStart, locEnd
    
    Application.ScreenUpdating = True
End Sub

Sub HighlightCardOpenAIV3()
    Application.ScreenUpdating = False
    Dim TagText As String
    Dim BodyText As String
    Dim range As Word.range
    
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.Paragraphs(1).Next(2)
    Dim locStart As Long
    Dim locEnd As Long
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        BodyText = BodyText & paragraph.range.Text & "\n"
        Set paragraph = paragraph.Next(1)
    Loop
    
    locEnd = paragraph.Previous(1).range.End
    
    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    Result = AppleScriptTask("getUnderlinesInChunks.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$highlight")
    Result = Replace(Result, "['", "")
    Result = Replace(Result, "']", "")
    
    resultArr = Split(Result, "', '")
    UnderlineTextV2 resultArr, "Highlight", locStart, locEnd
    Application.ScreenUpdating = True
End Sub

Sub HighlightCardOpenAIV4()
    Application.ScreenUpdating = False
    Dim TagText As String
    Dim BodyText As String
    Dim range As Word.range
    
    TagText = Selection.Text
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)
    BodyText = ""
    
    Dim paragraph As Word.paragraph
    Set paragraph = Selection.Paragraphs(1).Next(2)
    
    Dim locStart As Long
    Dim locEnd As Long
    
    locStart = paragraph.range.start
    
    Do While paragraph.OutlineLevel <> 1 And paragraph.OutlineLevel <> 2 And paragraph.OutlineLevel <> 3 And paragraph.OutlineLevel <> 4
        Set range = paragraph.range.Duplicate
        range.Select
        Dim SelectionEnd As Long
        SelectionEnd = Selection.End
        
        range.Find.ClearFormatting
        range.Find.Replacement.ClearFormatting
        range.Find.Text = ""
        range.Find.Replacement.Text = ""
        range.Find.Font.Underline = wdUnderlineSingle
        range.Find.Wrap = wdFindStop
        
        Do While range.Find.Execute = True And i < 5
            BodyText = BodyText & " " & range.Text
            range.start = range.End
            range.End = SelectionEnd
        Loop
        
        Set paragraph = paragraph.Next(1)
        BodyText = BodyText & "\n"
    Loop
    
    locEnd = paragraph.Previous(1).range.End
    
    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    Result = AppleScriptTask("getUnderlinesInChunks.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$highlight")
    Result = Replace(Result, "['", "")
    Result = Replace(Result, "']", "")
    
    resultArr = Split(Result, "', '")
    UnderlineTextV2 resultArr, "Highlight", locStart, locEnd
    Application.ScreenUpdating = True
End Sub

Sub HighlightCardOpenAIV2()
    Application.ScreenUpdating = False
    
    Dim SelectionStart As Long
    Dim SelectionEnd As Long
    Dim TagText As String
    Dim BodyText As String
    Dim results As String
    
    Dim NextParagraph As paragraph
        
    TagText = Selection.Text
    
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)

    BodyText = ""
    Selection.Paragraphs(1).Next(2).range.Select
    
    Dim range As Word.range
    SelectionStart = Selection.start
    SelectionEnd = Selection.End
    
    Set range = Selection.Paragraphs(1).range.Duplicate
    
    range.Find.ClearFormatting
    range.Find.Replacement.ClearFormatting
    range.Find.Text = ""
    range.Find.Replacement.Text = ""
    range.Find.Font.Underline = wdUnderlineSingle
    range.Find.Wrap = wdFindStop
    
    Do While range.Find.Execute = True And i < 5
        BodyText = BodyText & " " & range.Text
        range.start = range.End
        range.End = SelectionEnd
    Loop
        
    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    results = AppleScriptTask("getUnderlines.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$highlight")
    results = Replace(results, "[\""", "")
    results = Replace(results, "\""]", "")
    
    resultArr = Split(results, "\"", \""")
    UnderlineText resultArr, "Highlight", True
    
    Application.ScreenUpdating = True
End Sub

Sub EmphasizeCardOpenAI()
    Application.ScreenUpdating = False
    
    Dim SelectionStart As Long
    Dim SelectionEnd As Long
    Dim TagText As String
    Dim BodyText As String
    Dim results As String
    
    Dim NextParagraph As paragraph
        
    If Selection.start <> Selection.Paragraphs(1).range.start Then Selection.Paragraphs(1).range.Select
    If Selection.End <> Selection.Paragraphs(1).range.End Then Selection.Paragraphs(1).range.Select
    
    
    TagText = Selection.Text
    
    TagText = Replace(TagText, "\n", "")
    TagText = Trim(TagText)

    BodyText = ""
    Selection.Paragraphs(1).Next(2).range.Select
    
    Dim range As Word.range
    SelectionStart = Selection.start
    SelectionEnd = Selection.End
    
    Set range = Selection.Paragraphs(1).range.Duplicate
    
    range.Find.ClearFormatting
    range.Find.Replacement.ClearFormatting
    range.Find.Text = ""
    range.Find.Replacement.Text = ""
    range.Find.Font.Underline = wdUnderlineSingle
    range.Find.Wrap = wdFindStop
    
    Do While range.Find.Execute = True And i < 5
        BodyText = BodyText & " " & range.Text
        range.start = range.End
        range.End = SelectionEnd
    Loop
        
    If Len(TagText) > 200 Then
        Application.ScreenUpdating = True
        Exit Sub
    End If
    
    results = AppleScriptTask("getUnderlines.scpt", "myapplescripthandler", TagText & "$$$" & "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" & "$$$" & BodyText & "$$$emphasis")
    results = Replace(results, "[\""", "")
    results = Replace(results, "\""]", "")
    
    resultArr = Split(results, "\"", \""")
    UnderlineText resultArr, "Emphasis"
    
    Application.ScreenUpdating = True
End Sub

Private Function UnderlineTextV2(DataArr As Variant, style As String, locStart As Long, locEnd As Long)
        Dim rngSearch As Word.range
        Dim found As Boolean
         
        Set rngSearch = ActiveDocument.range(start:=locStart, End:=locEnd)
        
        Dim styleStr As String
        styleStr = style
        If styleStr = "Highlight" Then
            styleStr = "Underline"
        End If
        
        For Each phrase In DataArr
            Dim p As String
            Dim oldLoc As Long
            p = Trim(phrase)
            oldLoc = rngSearch.start
            
            If Len(phrase) > 250 Then
                p = Left$(phrase, 250)
            End If
            
            If Len(p) < 3 Then
                rngSearch.End = rngSearch.start + 200
            End If
            
            With rngSearch.Find
                .ClearFormatting
                .Replacement.ClearFormatting
                .Text = p
                With .Replacement
                    .Font.Underline = wdUnderlineSingle
                    .Text = p
                End With
                .Wrap = wdFindStop
                .MatchCase = False
                .MatchWholeWord = ((Len(p) > 1 And Len(p) < 3) Or (Len(p) = 1 And phrase = LCase(phrase)))
                .MatchFuzzy = True
                found = .Execute(Replace:=wdReplaceOne)
            End With
    
            If found Then
                ' MsgBox "found " & p
                If style = "Highlight" Then
                    rngSearch.HighlightColorIndex = wdYellow
                    rngSearch.Font.Size = 11
                Else
                     rngSearch.style = styleStr
                End If

                rngSearch.End = locEnd
                
                If Len(p) < 6 Then
                    rngSearch.start = oldLoc
                Else
                    rngSearch.MoveStart Count:=-100
                    If rngSearch.start < locStart Then
                        rngSearch.start = locStart
                    End If
                End If
            Else
                ' MsgBox "not found " & p
                ' For highlighting, iterate through each subword
                If style = "Highlight" Then
                    pArr = Split(p, " ")
                    For i = LBound(pArr) To UBound(pArr) - 1
                        'combine subwords that are too short
                        If Len(pArr(i)) < 4 Then
                            pArr(i) = pArr(i) & " " & pArr(i + 1)
                        End If
                    Next i
                    
                    For Each subP In pArr
                        If Len(subP) > 0 Then
                            'Look right around the last highlighted location
                            rngSearch.start = oldLoc - 50
                            rngSearch.End = oldLoc + 200
                            
                            Dim myRange As Word.range
                            Set myRange = ActiveDocument.range(start:=rngSearch.start, End:=rngSearch.End)
                            
                            With myRange.Find
                                .ClearFormatting
                                .Replacement.ClearFormatting
                                .Text = subP
                                With .Replacement
                                    .Font.Underline = wdUnderlineSingle
                                    .Text = subP
                                End With
                                .Wrap = wdFindStop
                                .MatchCase = False
                                .MatchWholeWord = ((Len(p) > 1 And Len(p) < 3) Or (Len(p) = 1 And phrase = LCase(phrase)))
                                .MatchFuzzy = True
                                found = .Execute(Replace:=wdReplaceOne)
                            End With
                            
                            If found Then
                                myRange.HighlightColorIndex = wdYellow
                                myRange.Font.Size = 11
                                oldLoc = myRange.start
                            Else
                                rngSearch.start = oldLoc
                                rngSearch.End = locEnd
                            End If
                        End If
                    Next subP
                Else
                    ' Retain the old search parameters
                    rngSearch.start = oldLoc
                    rngSearch.End = locEnd
                End If
            End If
        Next phrase
    End Function


Private Function UnderlineText(DataArr As Variant, style As String, Optional ByVal forceCurParagraph As Boolean = False)
        Dim rngSearch As Word.range
        Dim locStart As Long
        Dim locEnd As Long
        If style <> "Emphasis" And forceCurParagraph = False Then
            Set rngSearch = Selection.Paragraphs(1).Next(2).range.Duplicate
            locStart = Selection.Paragraphs(1).Next(2).range.start
            locEnd = Selection.Paragraphs(1).Next(2).range.End
            Selection.Paragraphs(1).Next(2).range.Select
        Else
            Set rngSearch = Selection.Paragraphs(1).range.Duplicate
            locStart = Selection.Paragraphs(1).range.start
            locEnd = Selection.Paragraphs(1).range.End
            Selection.Paragraphs(1).range.Select
        End If
        
        Dim found As Boolean
        
        Dim styleStr As String
        styleStr = style
        
        If styleStr = "Highlight" Then
            styleStr = "Underline"
        End If
        
        For Each phrase In DataArr
            Dim p As String
            Dim oldLoc As Long
            p = Trim(phrase)
            oldLoc = rngSearch.start
            
            If Len(phrase) > 250 Then
                p = Left$(phrase, 250)
            End If
            
            If Len(p) < 3 Then
                rngSearch.End = rngSearch.start + 200
            End If
            
            
            With rngSearch.Find
                .ClearFormatting
                .Replacement.ClearFormatting
                .Text = p
                With .Replacement
                    .Font.Underline = wdUnderlineSingle
                    .Text = p
                End With
                .Wrap = wdFindStop
                .MatchCase = False
                .MatchWholeWord = ((Len(p) > 1 And Len(p) < 3) Or (Len(p) = 1 And phrase = LCase(phrase)))
                .MatchFuzzy = True
                found = .Execute(Replace:=wdReplaceOne)
            End With
    
            If found Then
                If style = "Highlight" Then
                    rngSearch.HighlightColorIndex = wdYellow
                    rngSearch.Font.Size = 11
                Else
                     rngSearch.style = styleStr
                End If
                rngSearch.MoveStart Count:=-50
                rngSearch.End = locEnd
                
                If Len(p) < 6 Then
                    rngSearch.start = oldLoc
                End If
            Else
                If style = "Highlight" Then
                    pArr = Split(p, " ")
                    For i = LBound(pArr) To UBound(pArr) - 1
                        If Len(pArr(i)) < 4 Then
                            pArr(i) = pArr(i) & " " & pArr(i + 1)
                        End If
                    Next i
                    For Each subP In pArr
                        If Len(subP) > 0 Then
                            rngSearch.start = oldLoc - 50
                            rngSearch.End = oldLoc + 200
                            
                            Dim myRange As Word.range
                            Set myRange = ActiveDocument.range(start:=rngSearch.start, End:=rngSearch.End)
                            
                            With rngSearch.Find
                                .ClearFormatting
                                .Replacement.ClearFormatting
                                .Text = subP
                                With .Replacement
                                    .Font.Underline = wdUnderlineSingle
                                    .Text = subP
                                End With
                                .Wrap = wdFindStop
                                .MatchCase = False
                                .MatchWholeWord = ((Len(p) > 1 And Len(p) < 3) Or (Len(p) = 1 And phrase = LCase(phrase)))
                                .MatchFuzzy = True
                                found = .Execute(Replace:=wdReplaceOne)
                            End With
                            
                            If found Then
                                rngSearch.HighlightColorIndex = wdYellow
                                rngSearch.Font.Size = 11
                                
                                oldLoc = rngSearch.start
                            Else
                                rngSearch.start = oldLoc
                                rngSearch.End = locEnd
                            End If
                        End If
                    Next subP
                Else
                    rngSearch.start = oldLoc
                    rngSearch.End = locEnd
                End If
            End If
        Next phrase
    End Function
