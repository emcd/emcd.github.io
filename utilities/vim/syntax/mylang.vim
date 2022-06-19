" Vim Syntax Description
" Language: Mylang

if exists("b:current_syntax")
    finish
endif

let b:current_syntax = "mylang"

" Identifiers
syntax match mylangIdentifier "\v\a(\w|\-|_)*\w?" display
highlight link mylangIdentifier Identifier

" Numeric Literals
" TODO: Implement floating-point, complex, and rational.
syntax match mylangNumericLiteral "\v(\+|\-)?\d([\d_]*)?" display
syntax match mylangNumericLiteral "\v(\+|\-)?\\b[01]([01_]*)?" display
syntax match mylangNumericLiteral "\v(\+|\-)?\\o[0-7]([0-7_]*)?" display
syntax match mylangNumericLiteral "\v(\+|\-)?\\x[\da-fA-F_]([\da-fA-F_]*)?" display
highlight link mylangNumericLiteral Number

" Textual Literals
" I  - Interpolatory
" Q  - Quote Delimiters
syntax region mylangQTextualLiteral matchgroup=Comment start=+'+ skip=+\\'+ end=+'+ display contains=mylangTextualEscapeSequence
highlight link mylangQTextualLiteral String
syntax region mylangQITextualLiteral matchgroup=Comment start=+"+ skip=+\\"+ end=+"+ display contains=mylangTextualEscapeSequence,mylangTextualInterpolant
highlight link mylangQITextualLiteral String
syntax match mylangTextualEscapeSequence "\v\\($|\\|\'|\"|a|b|f|n|r|t|v)" contained
" TODO: Implement octal, hexadecimal, and Unicode escapes.
highlight link mylangTextualEscapeSequence SpecialChar
syntax match mylangTextualInterpolant "\v[^\{]\zs\{\a(\w|\-|_)*\w?(\.\a(\w|\-|_)*\w?)*\}" contained contains=mylangIdentifier
" TODO: Implement format mini-language.
" TODO: Use nextgroup to link actual interpolant with interpolation specifiers.
highlight link mylangTextualInterpolant SpecialChar

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
highlight link mylangKeyword Keyword

" Delimiters
syntax match mylangDelimiter "\v[,:]"
syntax match mylangDelimiter "\v(\(\.?|\.?\))"
syntax match mylangDelimiter "\v(\[\~?|\~?\])"
syntax match mylangDelimiter "\v(\{\~?|\~?\})"
highlight link mylangDelimiter Comment

" Unary Prefix Operators
syntax match mylangOperator "\v\.{3}"
syntax match mylangOperator "\v\.\ze\w"
syntax match mylangOperator "\v(^|\s)\zsb\~\ze\s"

" Binary Infix Operators
syntax match mylangOperator "\v\s\zs(\<|\!\=|\>|\>\=|\=\=|\<\=)\ze\s"
syntax match mylangOperator "\v\s\zs(\+|\-|\*|/)\ze\s"
syntax match mylangOperator "\v\s\zs\*(\*|\<|\>)\ze\s"
syntax match mylangOperator "\v\s\zsZ(/|\%)\ze\s"
syntax match mylangOperator "\v\s\zsb(\&|\||\^)\ze\s"

highlight link mylangOperator Operator

" Comments
syntax region mylangRemarkLine start="\v#\s" end="$" display
highlight link mylangRemarkLine Comment
syntax region mylangHelpHeadline matchgroup=SpecialComment start="#:" end="$" contained display transparent
syntax region mylangHelpBlock start="\v^\z(\s*)#:\s+.*" skip="\v^(\z1\s+|$)" end="\v^(\z1\s+)@!"he=s-1,re=s-1 keepend fold contains=mylangHelpHeadline,@Spell
highlight link mylangHelpBlock Comment
