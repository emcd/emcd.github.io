from pygments.lexer import ExtendedRegexLexer, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)


HEADSTART_KEYWORDS = (
    'elif',
    'for',
    'from',
    'if',
    'let',
    'with', 'with?',
    'while',
)
HEADEND_KEYWORDS = (
    '=',
    'do', 'does',
    'else',
)
ISOLATED_OPERATORS = (
    'is?',
)
HEADSTART_SUFFIX = r'(?=\s+)'
HEADEND_SUFFIX = r'(?=(?:\s+|:))'

class MylangLexer( ExtendedRegexLexer ):

    name = '???'
    aliases = [ 'mylang' ]
    filenames = [ '*.mylang' ]

    tokens = {
        'root': [
            ( r'\s+', Text ),
            ( words( HEADSTART_KEYWORDS, suffix = HEADSTART_SUFFIX ),
              Keyword.Reserved ),
            ( words( HEADEND_KEYWORDS, suffix = HEADEND_SUFFIX ),
              Keyword.Reserved ),
            ( words( ISOLATED_OPERATORS, suffix = HEADSTART_SUFFIX ),
              Operator ),
            ( r'(?:\+|\-)?\d(?:[\d_]*)?', Number ),
            ( r'\w(?:[\w\-_]*\w)?', Name.Variable ),
            ( r'[\(\[\{,:\}\]\)]', Punctuation ),
            ( r'\.', Operator ),
            ( r'`[^`]*`', Comment.Preproc ),
            ( r'"[^"]*"', String.Double ),
            ( r"'[^']*'", String.Single ),
            ( r'.*\n', Text ),
        ]
    }


__all__ = [ 'MylangLexer' ]
