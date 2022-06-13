# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

#============================================================================#
#                                                                            #
#  Licensed under the Apache License, Version 2.0 (the "License");           #
#  you may not use this file except in compliance with the License.          #
#  You may obtain a copy of the License at                                   #
#                                                                            #
#      http://www.apache.org/licenses/LICENSE-2.0                            #
#                                                                            #
#  Unless required by applicable law or agreed to in writing, software       #
#  distributed under the License is distributed on an "AS IS" BASIS,         #
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  #
#  See the License for the specific language governing permissions and       #
#  limitations under the License.                                            #
#                                                                            #
#============================================================================#

''' Pygments lexer for an unnamed language. '''


# References:
#   https://pygments.org/docs/lexerdevelopment/
#   https://pygments.org/docs/tokens/
#   https://github.com/pygments/pygments/tree/master/pygments/lexers


from pygments.lexer import (
    ExtendedRegexLexer,
    bygroups, include, words,
)
from pygments.token import (
    Comment, Error, Keyword, Name, Number, Operator, Punctuation, String, Text,
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
STDLIB_SYMBOLS = (
    'Dynstring',
)
HEADSTART_SUFFIX = r'(?=\s+)'
HEADEND_SUFFIX = r'(?=(?:\s+|:))'
IDENTIFIER_PATTERN = r'\w(?:[\w\-_]*\w)?'


class MylangLexer( ExtendedRegexLexer ):

    name = '???'
    aliases = [ 'mylang' ]
    filenames = [ '*.mylang' ]

    tokens = {
        'literal': [
            ( r'(?:\+|\-)?\d(?:[\d_]*)?', Number ),
            ( r'"', String.Double, 'interpolatory-text' ),
            ( r"'[^']*'", String.Single ),
        ],
        'interpolatory-text': [
            ( r'"', String.Double, '#pop' ),
            ( r'\{\{', String.Double ),
            ( r'\{', String.Interpol, 'textual-interpolant' ),
            # TODO: Standard escapes.
            ( r'[^"\{]+', String.Double ),
        ],
        'textual-interpolant': [
            ( r'\}', String.Interpol, '#pop' ),
            ( IDENTIFIER_PATTERN, Name.Variable ),
            ( r'\.', Operator ),
            # TODO: Format mini-language.
            ( r'.*"', Error, '#pop' ),
        ],
        'root': [
            ( r'(?s)(^\s*)(#:)(\s+)(.*)(?=^\1\S)',
              bygroups( Text, Comment.Special, Text, Comment.Multiline ) ),
            ( r'\s+', Text ),
            ( words( HEADSTART_KEYWORDS, suffix = HEADSTART_SUFFIX ),
              Keyword.Reserved ),
            ( words( HEADEND_KEYWORDS, suffix = HEADEND_SUFFIX ),
              Keyword.Reserved ),
            ( words( ISOLATED_OPERATORS, suffix = HEADSTART_SUFFIX ),
              Operator ),
            ( words( STDLIB_SYMBOLS, suffix = HEADSTART_SUFFIX ),
              Name.Builtin ),
            include( 'literal' ),
            ( IDENTIFIER_PATTERN, Name.Variable ),
            ( r'[\(\[\{,:\}\]\)]', Punctuation ),
            ( r'\.', Operator ),
            ( r'`', Comment.Preproc, 'compilation-directives' ),
            ( r'.*\n', Text ),
        ],
        'compilation-directives': [
            ( r'`', Comment.Preproc, '#pop' ),
            ( r'\s+', Text ),
            ( f"({IDENTIFIER_PATTERN})" + r'(\s+)(:)(\s+)',
              bygroups( Name.Attribute, Text, Punctuation, Text ),
              'compilation-option-rhs' ),
            ( r'(?:\?)?' + IDENTIFIER_PATTERN, Name.Class ),
            ( r'(?:\+|\-)\w(?:[\w\-]*\w)?', Name.Attribute ),
            ( r'[\(\[\{,:\}\]\)]', Punctuation ),
            ( r'.*(?=`)', Text ),
        ],
        'compilation-option-rhs': [
            ( r',', Punctuation, '#pop' ),
            ( r'`', Comment.Preproc, '#pop:2' ),
            include( 'literal' ),
        ],
    }


__all__ = [ 'MylangLexer' ]
