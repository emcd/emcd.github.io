from pygments.lexer import ExtendedRegexLexer, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Operator,
    Punctuation,
    String,
    Text,
)


KEYWORDS = (
    '=',
    'do', 'does',
    'elif',
    'else',
    'for',
    'from',
    'if',
    'let',
    'moreover',
    'with', 'with?',
    'while',
)

ISOLATED_OPERATORS = (
    'is?',
)

class MylangLexer( ExtendedRegexLexer ):

    name = '???'
    aliases = [ 'mylang' ]
    filenames = [ '*.mylang' ]

    tokens = {
        'root': [
            ( r'\s+', Text ),
            ( words( KEYWORDS, suffix = r'[\s:]' ), Keyword.Reserved ),
            ( words( ISOLATED_OPERATORS, suffix = r'\s' ), Operator.Word ),
            ( r'[\w\-_]+', Name.Variable ),
            ( r'[\(\[,:\]\)]', Punctuation ),
            ( r'\.', Operator ),
            ( r'`[^`]*`', Comment.Preproc ),
            ( r'"[^"]*"', String.Double ),
            ( r"'[^']*'", String.Single ),
            ( r'.*\n', Text ),
        ]
    }

__all__ = [ 'MylangLexer' ]
