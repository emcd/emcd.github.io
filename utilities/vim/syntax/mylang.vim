" Vim Syntax Description
" Language: Mylang

if exists("b:current_syntax")
    finish
endif

let b:current_syntax = "mylang"

" Keywords always have precedence over matches and regions.
" Evaluation goes from most recently defined to least recently defined.
" So, definitions at the bottom of the file have the highest precedence.
" Some guidance that can be drawn from this:
"   * General error conditions should be defined near the top of the file,
"     so that more specific valid conditions can override them.
"   * When matches overlap, more specific ones should be defined lower
"     in the file than more general ones.

" Matchgroups for a region MUST be given BEFORE the starts and ends
" to which they apply.

" Vim Bug: Some assertions are broken in very magic mode?
" Vim Bug: Assertions with optional groups are broken.
" Vim Bug: Lookahead assertions cause overextended highlight.

" General Errors
syntax match mylangError '\v\\.' display
" TODO: Error on word character followed by punctuation.
highlight default link mylangError Error

" Delimiters
syntax match mylangDelimiter "\v[,:]"
syntax match mylangDelimiter "\v(\(\.?|\.?\))"
syntax match mylangDelimiter "\v(\[\~?|\~?\])"
syntax match mylangDelimiter "\v(\{\~?|\~?\})"
highlight default link mylangDelimiter Comment
syntax match mylangClauseDelimiter ':' contained display
highlight default link mylangClauseDelimiter Special

" Operators
syntax match mylangAccessOperator '\v\.\ze(\a|\[)'
highlight default link mylangAccessOperator Operator
syntax match mylangOperator "\v\.{2}\ze\s"
syntax match mylangOperator "\v\.{3}"
syntax match mylangOperator "\v(\+|\-|\*|/)\ze\s"
syntax match mylangOperator "\v\((\+|\*)\)\ze\s"
syntax match mylangOperator "\v\*(\*|\<|\>)\ze\s"
syntax match mylangOperator "\vZ(/|\%)\ze\s"
syntax match mylangOperator "\v(\<|\<\>|\>|\<\=|\=\=|\>\=|\!\=)\ze\s"
syntax match mylangOperator "\v\((\<\>|\=\=|\!\=)\)\ze\s"
syntax match mylangOperator "\vis\?\ze\s"
syntax match mylangOperator "\v(and\??|or\??)\ze\s"
syntax match mylangOperator "\v\((and\??|or\??)\)\ze\s"
syntax match mylangOperator "\vnot\?\ze\s"
syntax match mylangOperator "\vb(\&|\||\^|\<\<|\>\>)\ze\s"
syntax match mylangOperator "\vb\~\ze\s"
highlight default link mylangOperator Operator

" Identifiers
syntax match mylangIdentifier '\v\a((\w|\-)*\a)?' display
highlight default link mylangIdentifier Identifier

" Boolean Literals
syntax keyword mylangBooleanLiteral false true
highlight default link mylangBooleanLiteral Boolean

" Numeric Literals
" D - Decimal; B - Binary; X - Hexadecimal
" C - Complex; N - Natural / Nonnegative
" Q - Rational; Z - Integer
" Flpn - Floating-Point Number; Fxpn - Fixed-Point Number
syntax match mylangDCZLiteral "\v[+\-]?\d((\d|_)*\d)?[ij]?" display contains=mylangComplementSign,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCFlpnSubZLiteral,mylangDCFxpnSubZLiteral,mylangDCQDenomLiteral,mylangDCFlpnExpLiteral,mylangDCZImLiteral
syntax match mylangDCFlpnSubZLiteral "\v\.\d((\d|_)*\d)?[ij]?" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCFlpnExpLiteral,mylangDCZImLiteral
syntax match mylangDCFxpnSubZLiteral "\v'\d((\d|_)*\d)?[ij]?" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCZImLiteral
syntax match mylangDCQDenomLiteral "\v/\d((\d|_)*\d)?[ij]?" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCZImLiteral
syntax match mylangDCFlpnExpLiteral "\v[Ee][+\-]?\d((\d|_)*\d)?[ij]?" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCZImLiteral
syntax match mylangDCZImLiteral "\v[+\-]\d((\d|_)*\d)?([ij]|\ze.*[ij])" display contained contains=mylangComplementSign,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCFlpnSubZImLiteral,mylangDCFxpnSubZImLiteral,mylangDCQDenomImLiteral,mylangDCFlpnExpImLiteral
syntax match mylangDCFlpnSubZImLiteral "\v\.\d((\d|_)*\d)?([ij]|\ze.*[ij])" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix nextgroup=mylangDCFlpnExpImLiteral
syntax match mylangDCFxpnSubZImLiteral "\v'\d((\d|_)*\d)?[ij]" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix
syntax match mylangDCQDenomImLiteral "\v/\d((\d|_)*\d)?[ij]" display contained contains=mylangRadixPoint,mylangDecimalDigits,mylangNumericSuffix
syntax match mylangDCFlpnExpImLiteral "\v[Ee][+\-]?\d((\d|_)*\d)?[ij]" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangDecimalDigits,mylangNumericSuffix
syntax match mylangDNZLiteral "\v\d((\d|_)*\d)?N" display contains=mylangDecimalDigits,mylangNumericSuffix
syntax match mylangBCZLiteral "\v[+\-]?\\b[01]([01_]*[01])?[ij]?" display contains=mylangComplementSign,mylangNumericPrefix,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCFlpnSubZLiteral,mylangBCFxpnSubZLiteral,mylangBCQDenomLiteral,mylangBCFlpnExpLiteral,mylangBCZImLiteral
syntax match mylangBCFlpnSubZLiteral "\v\.[01]([01_]*[01])?[ij]?" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCFlpnExpLiteral,mylangBCZImLiteral
syntax match mylangBCFxpnSubZLiteral "\v'[01]([01_]*[01])?[ij]?" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCZImLiteral
syntax match mylangBCQDenomLiteral "\v/[01]([01_]*[01])?[ij]?" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCZImLiteral
syntax match mylangBCFlpnExpLiteral "\v[Pp][+\-]?[01]([01_]*[01])?[ij]?" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCZImLiteral
syntax match mylangBCZImLiteral "\v[+\-][01]([01_]*[01])?([ij]|\ze.*[ij])" display contained contains=mylangComplementSign,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCFlpnSubZImLiteral,mylangBCFxpnSubZImLiteral,mylangBCQDenomImLiteral,mylangBCFlpnExpImLiteral
syntax match mylangBCFlpnSubZImLiteral "\v\.[01]([01_]*[01])?([ij]|\ze.*[ij])" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix nextgroup=mylangBCFlpnExpImLiteral
syntax match mylangBCFxpnSubZImLiteral "\v'[01]([01_]*[01])?[ij]" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix
syntax match mylangBCQDenomImLiteral "\v/[01]([01_]*[01])?[ij]" display contained contains=mylangRadixPoint,mylangBinaryDigits,mylangNumericSuffix
syntax match mylangBCFlpnExpImLiteral "\v[Pp][+\-]?[01]([01_]*[01])?[ij]" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangBinaryDigits,mylangNumericSuffix
syntax match mylangBNZLiteral "\v\\b[01]([01_]*[01])?N" display contains=mylangNumericPrefix,mylangBinaryDigits,mylangNumericSuffix
syntax match mylangXCZLiteral "\v[+\-]?\\x\x((\x|_)*\x)?[ij]?" display contains=mylangComplementSign,mylangNumericPrefix,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCFlpnSubZLiteral,mylangXCFxpnSubZLiteral,mylangXCQDenomLiteral,mylangXCFlpnExpLiteral,mylangXCZImLiteral
syntax match mylangXCFlpnSubZLiteral "\v\.\x((\x|_)*\x)?[ij]?" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCFlpnExpLiteral,mylangXCZImLiteral
syntax match mylangXCFxpnSubZLiteral "\v'\x((\x|_)*\x)?[ij]?" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCZImLiteral
syntax match mylangXCQDenomLiteral "\v/\x((\x|_)*\x)?[ij]?" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCZImLiteral
syntax match mylangXCFlpnExpLiteral "\v[Pp][+\-]?\x((\x|_)*\x)?[ij]?" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCZImLiteral
syntax match mylangXCZImLiteral "\v[+\-]\x((\x|_)*\x)?([ij]|\ze.*[ij])" display contained contains=mylangComplementSign,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCFlpnSubZImLiteral,mylangXCFxpnSubZImLiteral,mylangXCQDenomImLiteral,mylangXCFlpnExpImLiteral
syntax match mylangXCFlpnSubZImLiteral "\v\.\x((\x|_)*\x)?([ij]|\ze.*[ij])" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix nextgroup=mylangXCFlpnExpImLiteral
syntax match mylangXCFxpnSubZImLiteral "\v'\x((\x|_)*\x)?[ij]" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix
syntax match mylangXCQDenomImLiteral "\v/\x((\x|_)*\x)?[ij]" display contained contains=mylangRadixPoint,mylangHexadecimalDigits,mylangNumericSuffix
syntax match mylangXCFlpnExpImLiteral "\v[Pp][+\-]?\x((\x|_)*\x)?[ij]" display contained contains=mylangNumericPowerSign,mylangComplementSign,mylangHexadecimalDigits,mylangNumericSuffix
syntax match mylangXNZLiteral "\v\\x(\x|_)((\x|_)*\x)?N" display contains=mylangNumericPrefix,mylangHexadecimalDigits,mylangNumericSuffix

syntax match mylangNumericPowerSign "\v[EPep]" contained
highlight default link mylangNumericPowerSign SpecialChar
syntax match mylangNumericPrefix "\v\\[bx]" contained
highlight default link mylangNumericPrefix Special
syntax match mylangNumericSuffix "\v[Nij]" contained
highlight default link mylangNumericSuffix SpecialChar
syntax match mylangRadixPoint "\v[\.'/]" contained
highlight default link mylangRadixPoint Delimiter

syntax match mylangEscapeSequenceNoninitializer /\m[^\\]/ contained display
highlight default link mylangEscapeSequenceNoninitializer String
syntax cluster mylangByteswiseEscapeSequence contains=mylangCompactEscapeSequence,mylangC0EscapeSequence,mylangHexadecimalByteEscapeSequence
syntax cluster mylangTextualEscapeSequence contains=mylangCompactEscapeSequence,mylangC0EscapeSequence,@mylangUnicodeEscapeSequence
syntax match mylangCompactEscapeSequence +\v\\(\\|'|"|e|n|r|t|$)+ contained display
highlight default link mylangCompactEscapeSequence SpecialChar
syntax match mylangSubcompactEscapeSequence +\v\\(\\|e|n|r|t)+ contained display
highlight default link mylangSubcompactEscapeSequence SpecialChar
syntax match mylangHexadecimalByteEscapeSequence '\\x\x\x' contained display
highlight default link mylangHexadecimalByteEscapeSequence SpecialChar
" TODO? Special coloring of ANSI SGR sequences.
syntax region mylangC0EscapeSequence matchgroup=SpecialChar start="\\C0<" end=">" display contains=mylangC0Code
highlight default link mylangC0EscapeSequence Error
syntax match mylangC0Code '\v(NUL|SOH|STX|ETX|EOT|ENQ|ACK|BEL|BS|HT|LF|VT|FF|CR|SO|SI|DLE|DC1|DC2|DC3|DC4|NAK|SYN|ETB|CAN|EM|SUB|ESC|FS|GS|RS|US)' contained
highlight default link mylangC0Code Keyword
syntax cluster mylangUnicodeEscapeSequence contains=mylangQuantUnicodeEscapeSequence,mylangNomUnicodeEscapeSequence
syntax region mylangQuantUnicodeEscapeSequence matchgroup=SpecialChar start='\v\\U' end='\v\|' contained display contains=mylangQuantUnicodeEscapeData
highlight default link mylangQuantUnicodeEscapeSequence Error
syntax match mylangQuantUnicodeEscapeData '\v(10|0?\x)?_?\x{1,4}\ze\|' contained display keepend contains=mylangHexadecimalDigits
highlight default link mylangQuantUnicodeEscapeData Comment
syntax region mylangNomUnicodeEscapeSequence matchgroup=SpecialChar start='\\U<' end='>' display contains=mylangUnicodePointName
highlight default link mylangNomUnicodeEscapeSequence Error
syntax match mylangUnicodePointName '\v[0-9A-Za-z]([0-9A-Za-z ]*[0-9A-Za-z])?' contained display
highlight default link mylangUnicodePointName Keyword

syntax match mylangInterpolationError '\v.*\}' contained
highlight default link mylangInterpolationError Error
syntax match mylangInteriorInterpolantIdentifierCascade '\v\.\a((\w|\-)*\a)?' contained display contains=mylangAccessOperator,mylangIdentifier nextgroup=mylangInteriorInterpolantIdentifierCascade
" TODO: Add support for indices on identifiers.
syntax match mylangInteriorInterpolant '\v\a((\w|\-)*\a)?' contained display contains=mylangIdentifier nextgroup=mylangInteriorInterpolantIdentifierCascade

syntax match mylangNumberBaseCapitalSpecifier '\V^' contained display
highlight default link mylangNumberBaseCapitalSpecifier Special
syntax region mylangNumberBaseSpecifier matchgroup=Special start='\V&#{' end='\V}' contained extend contains=mylangInteriorInterpolant,mylangInterpolationError nextgroup=mylangNumberBaseCapitalSpecifier
syntax match mylangNumberBaseSpecifier '\v\&\#(3[0-6]|[12][0-9]|[2-9])\ze[^0-9]' contained display contains=mylangDecimalDigits nextgroup=mylangNumberBaseCapitalSpecifier
highlight default link mylangNumberBaseSpecifier Special
syntax match mylangClassDependentInterpolationFormatSpecifier '\v[Xbdx]' contained display
syntax match mylangClassDependentInterpolationFormatSpecifier '\v[EFGefg%][Xbdx]?' contained display
syntax match mylangClassDependentInterpolationFormatSpecifier '\v[Ff]\ze(\&\#)' contained display nextgroup=mylangNumberBaseSpecifier
highlight default link mylangClassDependentInterpolationFormatSpecifier SpecialChar
syntax region mylangNumericPrecision matchgroup=Special start='\V.{' end='\V}' contained extend contains=mylangInteriorInterpolant,mylangInterpolationError nextgroup=mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
syntax match mylangNumericPrecision '\v\.[1-9][0-9]*' contained display nextgroup=mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangNumericPrecision Number
syntax match mylangNumericPresentationSpecifier '\v[@_,]' contained display nextgroup=mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangNumericPresentationSpecifier SpecialChar
syntax region mylangMinimumInterpolationCapacity matchgroup=Special start='\V{' end='\V}' contained extend contains=mylangInteriorInterpolant,mylangInterpolationError nextgroup=mylangNumericPresentationSpecifier,mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
syntax match mylangMinimumInterpolationCapacity '\v[1-9][0-9]*' contained display nextgroup=mylangNumericPresentationSpecifier,mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangMinimumInterpolationCapacity Number
syntax match mylangInterpolationSpecifiers1 '\v[+\- ]?\#?0?' contained display nextgroup=mylangMinimumInterpolationCapacity,mylangNumericPresentationSpecifier,mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangInterpolationSpecifiers1 SpecialChar
syntax match mylangInterpolationAlignmentSpecifier '\v[<>^]' contained display nextgroup=mylangInterpolationSpecifiers1,mylangMinimumInterpolationCapacity,mylangNumericPresentationSpecifier,mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangInterpolationAlignmentSpecifier SpecialChar
syntax match mylangInterpolationAlignmentInjector '\v.\ze[<>^]' contained display nextgroup=mylangInterpolationAlignmentSpecifier
highlight default link mylangInterpolationAlignmentInjector String
syntax match mylangInterpolantFormatSpecification '\V:' contained display nextgroup=mylangInterpolationAlignmentInjector,mylangInterpolationAlignmentSpecifier,mylangInterpolationSpecifiers1,mylangMinimumInterpolationCapacity,mylangNumericPresentationSpecifier,mylangNumericPrecision,mylangClassDependentInterpolationFormatSpecifier,mylangNumberBaseSpecifier
highlight default link mylangInterpolantFormatSpecification SpecialChar
syntax match mylangInterpolantRenditionForm '\V!r' contained display
syntax match mylangInterpolantRenditionForm '\v\![Hh]' contained display nextgroup=mylangInterpolantFormatSpecification
highlight default link mylangInterpolantRenditionForm SpecialChar
syntax match mylangInterpolantIdentifierCascade '\v\.\a((\w|\-)*\a)?' contained display contains=mylangAccessOperator,mylangIdentifier nextgroup=mylangInterpolantIdentifierCascade,mylangInterpolantRenditionForm,mylangInterpolantFormatSpecification
" TODO: Add support for indices on identifiers.
syntax match mylangInterpolant '\v\a((\w|\-)*\a)?' contained display contains=mylangIdentifier nextgroup=mylangInterpolantIdentifierCascade,mylangInterpolantRenditionForm,mylangInterpolantFormatSpecification

syntax region mylangSuggestiveInterpolation matchgroup=Comment start='\V{' skip='\v[{}][<>^]' end='\V}' contained keepend contains=mylangInterpolant,mylangInterpolationError
syntax match mylangSuggestiveInterpolation '\v(\{\{|\}\})' contained
highlight default link mylangSuggestiveInterpolation Comment
syntax region mylangActiveInterpolation matchgroup=Special start='\V{' skip='\v[{}][<>^]' end='\V}' contained keepend contains=mylangInterpolant,mylangInterpolationError
syntax match mylangActiveInterpolation '\v(\{\{|\}\})' contained
highlight default link mylangActiveInterpolation Special

" Unicode
syntax match mylangQuantUnicodeLiteral '\v\\U(10|0?\x)?_?\x{1,4}' display keepend contains=mylangHexadecimalDigits
highlight default link mylangQuantUnicodeLiteral SpecialChar

" Numeric Digits
syntax match mylangDecimalDigits '\v\d((\d|_)*\d)?' display contained contains=mylangNumericSeparator
highlight default link mylangDecimalDigits Number
syntax match mylangBinaryDigits '\v[01]([01_]*[01])?' display contained contains=mylangNumericSeparator
highlight default link mylangBinaryDigits Number
syntax match mylangHexadecimalDigits '\v\x((\x|_)*\x)?' display contained contains=mylangNumericSeparator
highlight default link mylangHexadecimalDigits Number

syntax match mylangNumericSeparator '_' contained
highlight default link mylangNumericSeparator Ignore

syntax match mylangComplementSign "\v[+\-]" contained
highlight default link mylangComplementSign SpecialChar

" Keywords
syntax match mylangKeyword "\v\=\ze\s" display
syntax keyword mylangKeyword do does
syntax keyword mylangKeyword elif else
syntax keyword mylangKeyword for
syntax keyword mylangKeyword from
syntax keyword mylangKeyword if
syntax keyword mylangKeyword let
syntax keyword mylangKeyword with
syntax match mylangKeyword "\vwith\?\ze\s" display
syntax keyword mylangKeyword while
highlight default link mylangKeyword Keyword

" Compact Sequences
" CSeq - Compact Sequence
" E - Escapable; NE - Non-escapable
" I - Interpolative; NI - Non-interpolative
" Q - with Quote Delimiters

syntax match mylangCSeqSpecializer /\v\\B|\\\\/ contained display
highlight default link mylangCSeqSpecializer Special

syntax cluster mylangTextCorpusModificationSpecifier contains=mylangC0EscapeSequence,@mylangUnicodeEscapeSequence,mylangSubcompactEscapeSequence,mylangEscapeSequenceNoninitializer
syntax match mylangTextCorpusModificationSpecifierSequence /\m\(\\U<.\{-}>\|\S\)\+/ contained display contains=@mylangTextCorpusModificationSpecifier
syntax cluster mylangBytesCorpusModificationSpecifier contains=mylangC0EscapeSequence,mylangHexadecimalByteEscapeSequence,mylangSubcompactEscapeSequence,mylangEscapeSequenceNoninitializer
syntax match mylangBytesCorpusModificationSpecifierSequence /\m\S\+/ contained display contains=@mylangBytesCorpusModificationSpecifier

syntax match mylangPostlinearTextInjectorSpecification /\v\<\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits nextgroup=mylangTextCorpusModificationSpecifierSequence
syntax match mylangPostlinearTextInjectorSpecification /\v\<(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangTextCorpusModificationSpecifierSequence
syntax match mylangPostlinearTextInjectorSpecification /\v\<\d((\d|_)*\d)?\|/ contained display contains=mylangDecimalDigits
syntax match mylangPostlinearTextInjectorSpecification /\v\<\d((\d|_)*\d)?\|\=/ contained display contains=mylangDecimalDigits nextgroup=@mylangTextCorpusModificationSpecifier
highlight default link mylangPostlinearTextInjectorSpecification Operator
syntax match mylangPrelinearTextInjectorSpecification /\v\>\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits
syntax match mylangPrelinearTextInjectorSpecification /\v\>(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangTextCorpusModificationSpecifierSequence
highlight default link mylangPrelinearTextInjectorSpecification Operator
syntax match mylangPostcorporalTextTerminatorSpecification /\v\:\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits
syntax match mylangPostcorporalTextTerminatorSpecification /\v\:(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangTextCorpusModificationSpecifierSequence
highlight default link mylangPostcorporalTextTerminatorSpecification Operator
syntax match mylangInterlinearTextSeparatorSpecification /\m|&/ contained display
syntax match mylangInterlinearTextSeparatorSpecification /\v\|\&?(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangTextCorpusModificationSpecifierSequence
highlight default link mylangInterlinearTextSeparatorSpecification Operator
syntax cluster mylangTextLiteralClauseModifier contains=mylangInterlinearTextSeparatorSpecification,mylangPostcorporalTextTerminatorSpecification,mylangPrelinearTextInjectorSpecification,mylangPostlinearTextInjectorSpecification
syntax match mylangTextLiteralCaputPostDelimiter '\v(\s.*)?$' contained display keepend contains=@mylangTextLiteralClauseModifier,@mylangCommentLine
highlight default link mylangTextLiteralCaputPostDelimiter Error
syntax match mylangTextLiteralClauseDelimiter /\v(\\\\)?\\['"]:/ contained display contains=mylangCSeqSpecializer,mylangClauseDelimiter nextgroup=mylangTextLiteralCaputPostDelimiter
highlight default link mylangTextLiteralClauseDelimiter String
syntax match mylangTextLiteralCaputPreDelimiter /\m.*\ze\\['"]:/ contained display contains=TOP nextgroup=mylangTextLiteralClauseDelimiter
syntax match mylangTextLiteralCaputPreDelimiter /\m.*\ze\\\\\\['"]:/ contained display contains=TOP nextgroup=mylangTextLiteralClauseDelimiter
" Note: Need two forms due to Vim bug with optional groups in lookaheads.

syntax match mylangPostlinearBytesInjectorSpecification /\v\<\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits nextgroup=mylangBytesCorpusModificationSpecifierSequence
syntax match mylangPostlinearBytesInjectorSpecification /\v\<(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangBytesCorpusModificationSpecifierSequence
syntax match mylangPostlinearBytesInjectorSpecification /\v\<\d((\d|_)*\d)?\|/ contained display contains=mylangDecimalDigits
syntax match mylangPostlinearBytesInjectorSpecification /\v\<\d((\d|_)*\d)?\|\=/ contained display contains=mylangDecimalDigits nextgroup=@mylangBytesCorpusModificationSpecifier
highlight default link mylangPostlinearBytesInjectorSpecification Operator
syntax match mylangPrelinearBytesInjectorSpecification /\v\>\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits
syntax match mylangPrelinearBytesInjectorSpecification /\v\>(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangBytesCorpusModificationSpecifierSequence
highlight default link mylangPrelinearBytesInjectorSpecification Operator
syntax match mylangPostcorporalBytesTerminatorSpecification /\v\:\d((\d|_)*\d)?/ contained display contains=mylangDecimalDigits
syntax match mylangPostcorporalBytesTerminatorSpecification /\v\:(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangBytesCorpusModificationSpecifierSequence
highlight default link mylangPostcorporalBytesTerminatorSpecification Operator
syntax match mylangInterlinearBytesSeparatorSpecification /\m|&/ contained display
syntax match mylangInterlinearBytesSeparatorSpecification /\v\|\&?(\d((\d|_)*\d)?)?\=/ contained display contains=mylangDecimalDigits nextgroup=mylangBytesCorpusModificationSpecifierSequence
highlight default link mylangInterlinearBytesSeparatorSpecification Operator
syntax cluster mylangBytesLiteralClauseModifier contains=mylangInterlinearBytesSeparatorSpecification,mylangPostcorporalBytesTerminatorSpecification,mylangPrelinearBytesInjectorSpecification,mylangPostlinearBytesInjectorSpecification
syntax match mylangBytesLiteralCaputPostDelimiter '\v(\s.*)?$' contained display keepend contains=@mylangBytesLiteralClauseModifier,@mylangCommentLine
highlight default link mylangBytesLiteralCaputPostDelimiter Error
syntax match mylangBytesLiteralClauseDelimiter /\v\\B(\\\\)?\\['"]:/ contained display contains=mylangCSeqSpecializer,mylangClauseDelimiter nextgroup=mylangBytesLiteralCaputPostDelimiter
highlight default link mylangBytesLiteralClauseDelimiter String
syntax match mylangBytesLiteralCaputPreDelimiter /\m.*\ze\\B\(\\\\\)\?\\['"]:/ contained display contains=TOP nextgroup=mylangBytesLiteralClauseDelimiter

syntax region mylangQEITextLiteral matchgroup=String start=/\\\@<!"/ skip=/\\"/ end=/"/ display contains=@mylangTextualEscapeSequence,mylangActiveInterpolation
syntax region mylangQEITextLiteral matchgroup=String start=/\\\@<!"""/ skip=/\\"/ end=/"""/ display contains=@mylangTextualEscapeSequence,mylangActiveInterpolation
highlight default link mylangQEITextLiteral Ignore

syntax region mylangQENITextLiteral matchgroup=String start=/\\\@<!'/ skip=/\\'/ end=/'/ display contains=@mylangTextualEscapeSequence,mylangSuggestiveInterpolation
syntax region mylangQENITextLiteral matchgroup=String start=/\\\@<!'''/ skip=/\\'/ end=/'''/ display contains=@mylangTextualEscapeSequence,mylangSuggestiveInterpolation
highlight default link mylangQENITextLiteral Ignore

syntax region mylangQNEITextLiteral matchgroup=String start=/\\\\"/ end=/"/ display contains=mylangActiveInterpolation
syntax region mylangQNEITextLiteral matchgroup=String start=/\\\\"""/ end=/"""/ display contains=mylangActiveInterpolation
highlight default link mylangQNEITextLiteral Ignore

syntax region mylangQNENITextLiteral matchgroup=String start=/\\\\'/ end=/'/ display contains=mylangSuggestiveInterpolation
syntax region mylangQNENITextLiteral matchgroup=String start=/\\\\'''/ end=/'''/ display contains=mylangSuggestiveInterpolation
highlight default link mylangQNENITextLiteral Ignore

syntax region mylangEITextLiteralClause start=/\v.*\\":.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,@mylangTextualEscapeSequence,mylangActiveInterpolation
syntax region mylangEITextLiteralClause start=/\v^\z(\s*).*\\":.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,@mylangTextualEscapeSequence,mylangActiveInterpolation
highlight default link mylangEITextLiteralClause String

syntax region mylangENITextLiteralClause start=/\v.*\\':.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,@mylangTextualEscapeSequence,mylangSuggestiveInterpolation
syntax region mylangENITextLiteralClause start=/\v^\z(\s*).*\\':.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,@mylangTextualEscapeSequence,mylangSuggestiveInterpolation
highlight default link mylangENITextLiteralClause String

syntax region mylangNEITextLiteralClause start=/\v.*\\\\\\":.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,mylangActiveInterpolation
syntax region mylangNEITextLiteralClause start=/\v^\z(\s*).*\\\\\\":.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,mylangActiveInterpolation
highlight default link mylangNEITextLiteralClause String

syntax region mylangNENITextLiteralClause start=/\v.*\\\\\\':.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,mylangSuggestiveInterpolation
syntax region mylangNENITextLiteralClause start=/\v^\z(\s*).*\\\\\\':.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangTextLiteralCaputPreDelimiter,mylangSuggestiveInterpolation
highlight default link mylangNENITextLiteralClause String

syntax region mylangQEIBytesLiteral matchgroup=String start=/\\B"/ skip=/\\"/ end=/"/ display contains=@mylangByteswiseEscapeSequence,mylangActiveInterpolation
syntax region mylangQEIBytesLiteral matchgroup=String start=/\\B"""/ skip=/\\"/ end=/"""/ display contains=@mylangByteswiseEscapeSequence,mylangActiveInterpolation
highlight default link mylangQEIBytesLiteral Ignore

syntax region mylangQENIBytesLiteral matchgroup=String start=/\\B'/ skip=/\\'/ end=/'/ display contains=@mylangByteswiseEscapeSequence,mylangSuggestiveInterpolation
syntax region mylangQENIBytesLiteral matchgroup=String start=/\\B'''/ skip=/\\'/ end=/'''/ display contains=@mylangByteswiseEscapeSequence,mylangSuggestiveInterpolation
highlight default link mylangQENIBytesLiteral Ignore

syntax region mylangQNEIBytesLiteral matchgroup=String start=/\\B\\\\"/ end=/"/ display contains=mylangActiveInterpolation
syntax region mylangQNEIBytesLiteral matchgroup=String start=/\\B\\\\"""/ end=/"""/ display contains=mylangActiveInterpolation
highlight default link mylangQNEIBytesLiteral Ignore

syntax region mylangQNENIBytesLiteral matchgroup=String start=/\\B\\\\'/ end=/'/ display contains=mylangSuggestiveInterpolation
syntax region mylangQNENIBytesLiteral matchgroup=String start=/\\B\\\\'''/ end=/'''/ display contains=mylangSuggestiveInterpolation
highlight default link mylangQNENIBytesLiteral Ignore

syntax region mylangEIBytesLiteralClause start=/\v.*\\B\\":.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,@mylangByteswiseEscapeSequence,mylangActiveInterpolation
syntax region mylangEIBytesLiteralClause start=/\v^\z(\s*).*\\B\\":.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,@mylangByteswiseEscapeSequence,mylangActiveInterpolation
highlight default link mylangEIBytesLiteralClause String

syntax region mylangENIBytesLiteralClause start=/\v.*\\B\\':.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,@mylangByteswiseEscapeSequence,mylangSuggestiveInterpolation
syntax region mylangENIBytesLiteralClause start=/\v^\z(\s*).*\\B\\':.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,@mylangByteswiseEscapeSequence,mylangSuggestiveInterpolation
highlight default link mylangENIBytesLiteralClause String

syntax region mylangNEIBytesLiteralClause start=/\v.*\\B\\\\\\":.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,mylangActiveInterpolation
syntax region mylangNEIBytesLiteralClause start=/\v^\z(\s*).*\\B\\\\\\":.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,mylangActiveInterpolation
highlight default link mylangNEIBytesLiteralClause String

syntax region mylangNENIBytesLiteralClause start=/\v.*\\B\\\\\\':.*$/ skip=/\v^(\s+|$)/ end=/\v^(\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,mylangSuggestiveInterpolation
syntax region mylangNENIBytesLiteralClause start=/\v^\z(\s*).*\\B\\\\\\':.*$/ skip=/\v^(\z1\s+|$)/ end=/\v^(\z1\s+)@!/he=s-1,re=s-1 keepend fold contains=mylangBytesLiteralCaputPreDelimiter,mylangSuggestiveInterpolation
highlight default link mylangNENIBytesLiteralClause String

" Comments
syntax cluster mylangCommentLine contains=mylangDocumentationLine,mylangCommentLine
syntax region mylangDocumentationLine matchgroup=SpecialComment start="\v#\s" end="$" display
highlight default link mylangDocumentationLine Comment
syntax region mylangCommentLine start="\v#{2,}\s" end="$" display
highlight default link mylangCommentLine Comment
syntax region mylangDocumentationCapital matchgroup=SpecialComment start="#:" end="$" contained display transparent
syntax region mylangDocumentationClause start="\v^\z(\s*)#:(\s+.*|$)" skip="\v^(\z1\s+|$)" end="\v^(\z1\s+)@!"he=s-1,re=s-1 keepend fold contains=mylangDocumentationCapital,@Spell
highlight default link mylangDocumentationClause Comment
syntax region mylangCommentClause start="\v^\z(\s*)#{2,}:(\s+.*|$)" skip="\v^(\z1\s+|$)" end="\v^(\z1\s+)@!"he=s-1,re=s-1 keepend fold contains=@Spell
highlight default link mylangCommentClause Comment
