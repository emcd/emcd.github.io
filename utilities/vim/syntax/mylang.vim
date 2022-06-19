" Vim Syntax Description
" Language: Mylang

if exists("b:current_syntax")
    finish
endif

let b:current_syntax = "mylang"

syntax iskeyword a-z

" Keywords
syntax match mylangKeyword "\v\=(\s+)\@=" display
syntax keyword mylangKeyword do does
syntax keyword mylangKeyword elif else
syntax keyword mylangKeyword for
syntax keyword mylangKeyword from
syntax keyword mylangKeyword if
syntax keyword mylangKeyword let
syntax keyword mylangKeyword with
syntax match mylangKeyword "\vwith\?(\s+)\@=" display
syntax keyword mylangKeyword while
highlight link mylangKeyword Keyword

" Delimiters
syntax match mylangDelimiter ","
syntax match mylangDelimiter "\v(\(\.?|\.?\))"
syntax match mylangDelimiter "\v(\[\~?|\~?\])"
syntax match mylangDelimiter "\v(\{\~?|\~?\})"
highlight link mylangDelimiter Delimiter

" Prefix Unary Operators
syntax match mylangOperator "\v\.{3}"
syntax match mylangOperator "\v\.\ze\w"
syntax match mylangOperator "\v(^|\s)\zsb\~\ze\s"

" Infix Binary Operators
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
