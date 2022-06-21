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
    ExtendedRegexLexer, LexerContext,
    bygroups, default, include, words,
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
STDLIB_SYMBOLS = (
    'Dynstring',
)
HEADSTART_SUFFIX = r'(?=\s+)'
HEADEND_SUFFIX = r'(?=(?:\s+|:))'
IDENTIFIER_PATTERN = r'[A-Za-z](?:[\w\-]*[0-9A-Za-z])?'

INITIAL_DELIMITERS_PATTERN  = r'(?:\(\.?|\[~?|\{~?)'
FINAL_DELIMITERS_PATTERN    = r'(?:\.?\)|~?\]|~?\})'
IDENTIFIER_ACCEPTANCE_PATTERN = fr"(?={FINAL_DELIMITERS_PATTERN}|[,:]|\s+)"


def _repeat( rules_name ):
    ''' Tokenizes match into constituent tokens.

        Useful to recurse into groups from
        :py:func:`pygments.lexer.bygroups`. '''

    def callback( lexer, match, context ):
        yield from lexer.get_tokens_unprocessed(
            context = LexerContext(
                match.group( ), 0,
                stack = [ *context.stack, rules_name ] ) )
        context.pos = match.end( )

    return callback


def _repeat_until_error( rules_name ):
    ''' Tokenizes match into constituent tokens until error.

        Useful with includes that may have no '#pop' directives. '''

    def callback( lexer, match, context ):
        for tstart, ttype, ttext in lexer.get_tokens_unprocessed(
            context = LexerContext(
                match.group( ), 0,
                stack = [ *context.stack, rules_name ] )
        ):
            if Error is ttype:
                context.pos = tstart
                break
            yield tstart, ttype, ttext
        context.pos = match.end( )

    return callback


def _repeat_for_count( rules_name, count ):
    ''' Tokenizes match into constituent tokens for specific number of turns.

        Useful with complex expressions with limited repetition. '''

    def callback( lexer, match, context ):
        generator = lexer.get_tokens_unprocessed(
            context = LexerContext(
                match.group( ), 0,
                stack = [ *context.stack, rules_name ] ) )
        for i in range( count ):
            tstart, ttype, ttext = next( generator )
            yield tstart, ttype, ttext
        context.pos = tstart + len( ttext )

    return callback


class MylangLexer( ExtendedRegexLexer ):

    name = '???'
    aliases = [ 'mylang' ]
    filenames = [ '*.mylang' ]

    tokens = {

        'root': [
            include( 'comment' ),
            include( 'literal' ),
            include( 'operator' ),
            include( 'delimiter' ),
            ( words( HEADSTART_KEYWORDS, suffix = HEADSTART_SUFFIX ),
              Keyword ),
            ( words( HEADEND_KEYWORDS, suffix = HEADEND_SUFFIX ),
              Keyword ),
            ( words( STDLIB_SYMBOLS, suffix = HEADSTART_SUFFIX ),
              Name.Builtin ),
            ( IDENTIFIER_PATTERN, Name.Variable ),
            ( r'`', Comment.Preproc, 'compilation-directives' ),
            ( r'.*\n', Text ),
        ],

        'comment': [
            ( r'(?s)(^\s*)(#:)(\s+.*?)(?=^\1\S)',
              bygroups( Text, Comment.Special, Comment.Multiline ) ),
            ( r'(?s)(^\s*)(#{2,}:)(\s+.*?)(?=^\1\S)',
              bygroups( Text, Comment, Comment.Multiline ) ),
            ( r'\s+', Text ),
            include( 'comment line' ),
        ],
        'comment line': [
            ( r'(#\s)(.*)$', bygroups( Comment.Special, Comment ) ),
            ( r'#{2,}\s+.*$', Comment ),
        ],

        'delimiter': [
            ( r'[,:]', Punctuation ),
            ( INITIAL_DELIMITERS_PATTERN, Punctuation ),
            ( FINAL_DELIMITERS_PATTERN, Punctuation ),
        ],

        'literal': [
            ( '(false|true)', Keyword.Constant ),
            include( 'compact sequence literal' ),
            include( 'number literal' ),
            include( 'unicode literal' ),
        ],
        'compact sequence literal': [
            include( 'bytes literal' ),
            include( 'text literal' ),
        ],

        'bytes literal': [
            include( 'nonescapable noninterpolative bytes literal' ),
            include( 'nonescapable interpolative bytes literal' ),
            include( 'escapable noninterpolative bytes literal' ),
            include( 'escapable interpolative bytes literal' ),
        ],

        'nonescapable noninterpolative bytes literal': [
            ( r"(?s)(^\s*)([^\n]*?)(\\B)(\\\\)(\\')(:)(.*?$)(.*?)(?=^\1\S)",
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Affix,
                String.Escape,
                String.Other,
                String.Affix,
                _repeat( 'bytes literal caput' ),
                _repeat( 'nonescapable noninterpolative bytes literal corpus' )
              )
            ),
            ( r"(\\B)(\\\\)(''')",
              bygroups( String.Affix, String.Escape, String.Delimiter ),
              'nonescapable noninterpolative triquote bytes literal' ),
            ( r"(\\B)(\\\\)(')",
              bygroups( String.Affix, String.Escape, String.Delimiter ),
              'nonescapable noninterpolative uniquote bytes literal' ),
        ],
        'nonescapable noninterpolative bytes literal corpus': [
            include( 'suggestive interpolation' ),
            ( r"[^{}]+", String.Heredoc ),
            default( '#pop' ),
        ],
        'nonescapable noninterpolative triquote bytes literal': [
            ( "'''", String.Delimiter, '#pop' ),
            include( 'suggestive interpolation' ),
            ( r"(?s).*?(?='''|\{|\})", String.Single ),
            ( '.', Error, '#pop' ),
        ],
        'nonescapable noninterpolative uniquote bytes literal': [
            ( "'", String.Delimiter, '#pop' ),
            include( 'suggestive interpolation' ),
            ( r"[^'{}]+", String.Single ),
            ( '.', Error, '#pop' ),
        ],

        'nonescapable interpolative bytes literal': [
            ( r'(?s)(^\s*)([^\n]*?)(\\B)(\\\\)(\\")(:)(.*?$)(.*?)(?=^\1\S)',
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Affix,
                String.Escape,
                String.Other,
                String.Affix,
                _repeat( 'bytes literal caput' ),
                _repeat( 'nonescapable interpolative bytes literal corpus' )
              )
            ),
            ( r'(\\B)(\\\\)(""")',
              bygroups( String.Affix, String.Escape, String.Delimiter ),
              'nonescapable interpolative triquote bytes literal' ),
            ( r'(\\B)(\\\\)(")',
              bygroups( String.Affix, String.Escape, String.Delimiter ),
              'nonescapable interpolative uniquote bytes literal' ),
        ],
        'nonescapable interpolative bytes literal corpus': [
            include( 'active interpolation' ),
            ( r'[^{}]+', String.Heredoc ),
            default( '#pop' ),
        ],
        'nonescapable interpolative triquote bytes literal': [
            ( '"""', String.Delimiter, '#pop' ),
            include( 'active interpolation' ),
            ( r'(?s).*?(?="""|\{|\})', String.Double ),
            ( '.', Error, '#pop' ),
        ],
        'nonescapable interpolative uniquote bytes literal': [
            ( '"', String.Delimiter, '#pop' ),
            include( 'active interpolation' ),
            ( r'[^"{}]+', String.Double ),
            ( '.', Error, '#pop' ),
        ],

        'escapable noninterpolative bytes literal': [
            ( r"(?s)(^\s*)([^\n]*?)(\\B)(\\')(:)(.*?$)(.*?)(?=^\1\S)",
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Affix,
                String.Other,
                String.Affix,
                _repeat( 'bytes literal caput' ),
                _repeat( 'escapable noninterpolative bytes literal corpus' )
              )
            ),
            ( r"(\\B)(''')",
              bygroups( String.Affix, String.Delimiter ),
              'escapable noninterpolative triquote bytes literal' ),
            ( r"(\\B)(')",
              bygroups( String.Affix, String.Delimiter ),
              'escapable noninterpolative uniquote bytes literal' ),
        ],
        'escapable noninterpolative bytes literal corpus': [
            include( 'byteswise escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"[^\\{}]+", String.Heredoc ),
            default( '#pop' ),
        ],
        'escapable noninterpolative triquote bytes literal': [
            ( "'''", String.Delimiter, '#pop' ),
            include( 'byteswise escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"(?s).*?(?='''|\\|\{|\})", String.Single ),
            ( '.', Error, '#pop' ),
        ],
        'escapable noninterpolative uniquote bytes literal': [
            ( "'", String.Delimiter, '#pop' ),
            include( 'byteswise escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"[^'\\{}]+", String.Single ),
            ( '.', Error, '#pop' ),
        ],

        'escapable interpolative bytes literal': [
            ( r'(?s)(^\s*)([^\n]*?)(\\B)(\\")(:)(.*?$)(.*?)(?=^\1\S)',
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Affix,
                String.Other,
                String.Affix,
                _repeat( 'bytes literal caput' ),
                _repeat( 'escapable interpolative bytes literal corpus' )
              )
            ),
            ( r'(\\B)(""")',
              bygroups( String.Affix, String.Delimiter ),
              'escapable interpolative triquote bytes literal' ),
            ( r'(\\B)(")',
              bygroups( String.Affix, String.Delimiter ),
              'escapable interpolative uniquote bytes literal' ),
        ],
        'escapable interpolative bytes literal corpus': [
            include( 'byteswise escape sequence' ),
            include( 'active interpolation' ),
            ( r'[^\\{}]+', String.Heredoc ),
            default( '#pop' ),
        ],
        'escapable interpolative triquote bytes literal': [
            ( '"""', String.Delimiter, '#pop' ),
            include( 'byteswise escape sequence' ),
            include( 'active interpolation' ),
            ( r'(?s).*?(?="""|\\|\{|\})', String.Double ),
            ( '.', Error, '#pop' ),
        ],
        'escapable interpolative uniquote bytes literal': [
            ( '"', String.Delimiter, '#pop' ),
            include( 'byteswise escape sequence' ),
            include( 'active interpolation' ),
            ( r'[^"\\{}]+', String.Double ),
            ( '.', Error, '#pop' ),
        ],

        'text literal': [
            include( 'nonescapable noninterpolative text literal' ),
            include( 'nonescapable interpolative text literal' ),
            include( 'escapable noninterpolative text literal' ),
            include( 'escapable interpolative text literal' ),
        ],

        'nonescapable noninterpolative text literal': [
            ( r"(?s)(^\s*)([^\n]*?)(\\\\)(\\')(:)(.*?$)(.*?)(?=^\1\S)",
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Escape,
                String.Other,
                String.Affix,
                _repeat( 'text literal caput' ),
                _repeat( 'nonescapable noninterpolative text literal corpus' )
              )
            ),
            ( r"(\\\\)(''')",
              bygroups( String.Escape, String.Delimiter ),
              'nonescapable noninterpolative triquote text literal' ),
            ( r"(\\\\)(')",
              bygroups( String.Escape, String.Delimiter ),
              'nonescapable noninterpolative uniquote text literal' ),
        ],
        'nonescapable noninterpolative text literal corpus': [
            include( 'suggestive interpolation' ),
            ( r"[^{}]+", String.Heredoc ),
            default( '#pop' ),
        ],
        'nonescapable noninterpolative triquote text literal': [
            ( "'''", String.Delimiter, '#pop' ),
            include( 'suggestive interpolation' ),
            ( "(?s).*?(?='''|\{|\})", String.Single ),
            ( '.', Error, '#pop' ),
        ],
        'nonescapable noninterpolative uniquote text literal': [
            ( "'", String.Delimiter, '#pop' ),
            include( 'suggestive interpolation' ),
            ( r"[^'{}]+", String.Double ),
            ( '.', Error, '#pop' ),
        ],

        'nonescapable interpolative text literal': [
            ( r'(?s)(^\s*)([^\n]*?)(\\\\)(\\")(:)(.*?$)(.*?)(?=^\1\S)',
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Escape,
                String.Other,
                String.Affix,
                _repeat( 'text literal caput' ),
                _repeat( 'nonescapable interpolative text literal corpus' )
              )
            ),
            ( r'(\\\\)(""")',
              bygroups( String.Escape, String.Delimiter ),
              'nonescapable interpolative triquote text literal' ),
            ( r'(\\\\)(")',
              bygroups( String.Escape, String.Delimiter ),
              'nonescapable interpolative uniquote text literal' ),
        ],
        'nonescapable interpolative text literal corpus': [
            include( 'active interpolation' ),
            ( r'[^{}]+', String.Heredoc ),
            default( '#pop' ),
        ],
        'nonescapable interpolative triquote text literal': [
            ( '"""', String.Delimiter, '#pop' ),
            include( 'active interpolation' ),
            ( r'(?s).*?(?="""|\{|\})', String.Double ),
            ( '.', Error, '#pop' ),
        ],
        'nonescapable interpolative uniquote text literal': [
            ( '"', String.Delimiter, '#pop' ),
            include( 'active interpolation' ),
            ( r'[^"{}]+', String.Double ),
            ( '.', Error, '#pop' ),
        ],

        'escapable noninterpolative text literal': [
            ( r"(?s)(^\s*)([^\n]*?)(\\')(:)(.*?$)(.*?)(?=^\1\S)",
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Other,
                String.Affix,
                _repeat( 'text literal caput' ),
                _repeat( 'escapable noninterpolative text literal corpus' )
              )
            ),
            ( "'''", String.Delimiter,
              'escapable noninterpolative triquote text literal' ),
            ( "'", String.Delimiter,
              'escapable noninterpolative uniquote text literal' ),
        ],
        'escapable noninterpolative text literal corpus': [
            include( 'textual escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"[^\\{}]+", String.Heredoc ),
            default( '#pop' ),
        ],
        'escapable noninterpolative triquote text literal': [
            ( "'''", String.Delimiter, '#pop' ),
            include( 'textual escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"(?s).*?(?='''|\\|\{|\})", String.Single ),
            ( '.', Error, '#pop' ),
        ],
        'escapable noninterpolative uniquote text literal': [
            ( "'", String.Delimiter, '#pop' ),
            include( 'textual escape sequence' ),
            include( 'suggestive interpolation' ),
            ( r"[^'\\{}]+", String.Single ),
            ( '.', Error, '#pop' ),
        ],

        'escapable interpolative text literal': [
            ( r'(?s)(^\s*)([^\n]*?)(\\")(:)(.*?$)(.*?)(?=^\1\S)',
              bygroups(
                Text,
                _repeat( 'root' ),
                String.Other,
                String.Affix,
                _repeat( 'text literal caput' ),
                _repeat( 'escapable interpolative text literal corpus' )
              )
            ),
            ( '"""', String.Delimiter,
              'escapable interpolative triquote text literal' ),
            ( '"', String.Delimiter,
              'escapable interpolative uniquote text literal' ),
        ],
        'escapable interpolative text literal corpus': [
            include( 'textual escape sequence' ),
            include( 'active interpolation' ),
            ( r'[^\\{}]+', String.Heredoc ),
            default( '#pop' ),
        ],
        'escapable interpolative triquote text literal': [
            ( '"""', String.Delimiter, '#pop' ),
            include( 'textual escape sequence' ),
            include( 'active interpolation' ),
            ( r'(?s).*?(?="""|\\|\{|\})', String.Double ),
            ( '.', Error, '#pop' ),
        ],
        'escapable interpolative uniquote text literal': [
            ( '"', String.Delimiter, '#pop' ),
            include( 'textual escape sequence' ),
            include( 'active interpolation' ),
            ( r'[^"\\{}]+', String.Double ),
            ( '.', Error, '#pop' ),
        ],

        'bytes literal caput': [
            ( '$', Text, '#pop' ),
            ( r'\s+', Text ),
            ( r'(\|&?|[:><])([0-9](?:[0-9_]*[0-9])?)?(=)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator
              ),
              'bytes corpus modification specifiers' ),
            ( r'(<)([0-9](?:[0-9_]*[0-9])?)(\|=)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator
              ),
              'bytes corpus modification specifier' ),
            ( r'\|&', Operator ),
            ( r'(<)([0-9](?:[0-9_]*[0-9])?)(\|)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator )
              ),
            ( r'([:><])([0-9](?:[0-9_]*[0-9])?)',
              bygroups( Operator, _repeat_until_error( 'decimal digits' ) ) ),
            include( 'comment line' ),
        ],
        'bytes corpus modification specifiers': [
            ( r'''\\(\\|e|n|r|t)''', String.Escape ),
            ( r'(\\x)([0-9A-Fa-f]{2})',
              bygroups( String.Escape, Number.Hex ) ),
            include( 'nominative c zero escape sequence' ),
            ( r'\S+?(?=\\|\s|$)', String ),
            default( '#pop' ),
        ],
        'bytes corpus modification specifier': [
            ( r'''\\(\\|e|n|r|t)''', String.Escape, '#pop' ),
            ( r'(\\x)([0-9A-Fa-f]{2})',
              bygroups( String.Escape, Number.Hex ), '#pop' ),
            ( r'\\C0<.*?>',
              _repeat_for_count( 'nominative c zero escape sequence', 1 ),
              '#pop' ),
            ( r'\S', String, '#pop' ),
        ],

        'text literal caput': [
            ( '$', Text, '#pop' ),
            ( r'\s+', Text ),
            ( r'(\|&?|[:><])([0-9](?:[0-9_]*[0-9])?)?(=)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator
              ),
              'text corpus modification specifiers' ),
            ( r'(<)([0-9](?:[0-9_]*[0-9])?)(\|=)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator
              ),
              'text corpus modification specifier' ),
            ( r'\|&', Operator ),
            ( r'(<)([0-9](?:[0-9_]*[0-9])?)(\|)',
              bygroups(
                  Operator,
                  _repeat_until_error( 'decimal digits' ),
                  Operator )
              ),
            ( r'([:><])([0-9](?:[0-9_]*[0-9])?)',
              bygroups( Operator, _repeat_until_error( 'decimal digits' ) ) ),
            include( 'comment line' ),
        ],
        'text corpus modification specifiers': [
            ( r'''\\(\\|e|n|r|t)''', String.Escape ),
            include( 'unicode escape sequence' ),
            include( 'nominative c zero escape sequence' ),
            ( r'\S+?(?=\\|\s|$)', String ),
            default( '#pop' ),
        ],
        'text corpus modification specifier': [
            ( r'''\\(\\|e|n|r|t)''', String.Escape, '#pop' ),
            ( r'\\U(?:<.*?>|.*?\|)',
              _repeat_for_count( 'unicode escape sequence', 1 ), '#pop' ),
            ( r'\\C0<.*?>',
              _repeat_for_count( 'nominative c zero escape sequence', 1 ),
              '#pop' ),
            ( r'\S', String, '#pop' ),
        ],

        # TODO? Special coloring of ANSI SGR sequences.
        'byteswise escape sequence': [
            ( r'''\\(\\|'|"|e|n|r|t|$)''', String.Escape ),
            ( r'(\\x)([0-9A-Fa-f]{2})',
              bygroups( String.Escape, Number.Hex ) ),
            include( 'nominative c zero escape sequence' ),
        ],
        'textual escape sequence': [
            ( r'''\\(\\|'|"|e|n|r|t|$)''', String.Escape ),
            include( 'unicode escape sequence' ),
            include( 'nominative c zero escape sequence' ),
        ],
        'unicode escape sequence': [
            ( r'(\\U)(?:(10|0?[0-9A-Fa-f])(_?))?([0-9A-Fa-f]{1,4})(\|)',
              bygroups(
                  String.Escape, Number.Hex, Punctuation,
                  Number.Hex, String.Escape ) ),
            include( 'nominative unicode literal' ),
            ( r'(\\U)(.*?)(\|)',
              bygroups( String.Escape, Error, String.Escape ) ),
        ],

        'active interpolation': [
            ( r'(\{\{|\}\})', String.Interpol ),
            ( r'(\{)(\s*)', bygroups( String.Interpol, Text ),
              ( 'active interpolation close',
                'ulterior interpolant initiation'
              ) ),
        ],
        'active interpolation close': [
            ( r'\}', String.Interpol, '#pop' ),
            ( '[^}]+', Error ),
        ],
        # Suggestive interpolations are not part of the language standard.
        # Convenience to mark portions of non-interpolative compact sequences
        # that could be separately interpolated with a format function.
        'suggestive interpolation': [
            ( r'(\{\{|\}\})', Comment ),
            ( r'(\{)(\s*)', bygroups( Comment, Text ),
              ( 'suggestive interpolation close',
                'ulterior interpolant initiation'
              ) ),
        ],
        'suggestive interpolation close': [
            ( r'\}', Comment, '#pop' ),
            ( '[^}]+', Error ),
        ],

        'ulterior interpolant initiation': [
            ( IDENTIFIER_PATTERN, Name.Variable,
              ( '#pop', 'ulterior interpolant continuation' ) ),
            # TODO? Literal compact sequences and numbers.
            default( '#pop' ),
        ],
        'ulterior interpolant continuation': [
            include( 'identifier cascade' ),
            ( '(!)([Hh])(:)',
              bygroups( String.Interpol, String.Affix, String.Interpol ),
              ( '#pop', 'interpolant format specification' ) ),
            ( r'(!)([Hhr])', bygroups( String.Interpol, String.Affix ),
              '#pop' ),
            ( ':', String.Interpol,
              ( '#pop', 'interpolant format specification' ) ),
            default( '#pop' ),
        ],
        'interpolant format specification': [
            ( r'(?:(.)?([<>^]))?([+\- ])?(#)?(0)?',
              bygroups(
                  String,
                  Operator,         # [<>^]
                  Operator,         # [+\- ]
                  Operator,         # #
                  String.Affix      # 0
              ),
              ( '#pop', 'minimum interpolation capacity' ) ),
        ],
        'minimum interpolation capacity': [
            ( '[1-9][0-9]*', Number,
              ( '#pop', 'numeric presentation specifier' ) ),
            ( r'\{', String.Interpol,
              ( '#pop',
                'numeric presentation specifier',
                'interior interpolant initiation'
              ) ),
            default( ( '#pop', 'numeric presentation specifier' ) ),
        ],
        'numeric presentation specifier': [
            ( '[@_,]', Punctuation, ( '#pop', 'numeric precision' ) ),
            default( ( '#pop', 'numeric precision' ) ),
        ],
        'numeric precision': [
            ( r'(\.)([1-9][0-9]*)', bygroups( Punctuation, Number ),
              ( '#pop', 'class dependent interpolation format specifier' ) ),
            ( r'(\.)(\{)', bygroups( Punctuation, String.Interpol ),
              ( '#pop',
                'class dependent interpolation format specifier',
                'interior interpolant initiation'
              ) ),
            default(
                ( '#pop', 'class dependent interpolation format specifier' )
            ),
        ],
        'class dependent interpolation format specifier': [
            ( '([Ff])(&#)', bygroups( String.Affix, String.Affix ),
              ( '#pop', 'number base specification' ) ),
            ( '([EFGefg%])([Xbdx])?', bygroups( String.Affix, String.Affix ),
              '#pop' ),
            ( '[Xbdx]', String.Affix, '#pop' ),
            ( '&#', String.Affix, ( '#pop', 'number base specification' ) ),
            default( '#pop' ),
        ],
        'number base specification': [
            ( '(?:[2-9]|[12][0-9]|3[0-6])', Number,
              ( '#pop', 'number base capital specifier' ) ),
            ( r'\{', String.Interpol,
              ( '#pop',
                'number base capital specifier',
                'interior interpolant initiation'
              ) ),
            default( '#pop' ),
        ],
        'number base capital specifier': [
            ( r'\^', String.Affix, '#pop' ),
            default( '#pop' ),
        ],

        'interior interpolant initiation': [
            ( IDENTIFIER_PATTERN, Name.Variable,
              ( '#pop', 'interior interpolant continuation' ) ),
            # TODO? Literal compact sequences and numbers.
            default( ( '#pop', 'interior interpolant finalization' ) ),
        ],
        'interior interpolant continuation': [
            include( 'identifier cascade' ),
            default( ( '#pop', 'interior interpolant finalization' ) ),
        ],
        'interior interpolant finalization': [
            ( r'\}', String.Interpol, '#pop' ),
            ( '[^}]+', Error ),
        ],
        'identifier cascade': [
            ( r'\s+', Text ),
            ( r'(\.)' + f"({IDENTIFIER_PATTERN})",
              bygroups( Operator, Name.Variable ) ),
            # TODO: Add support for indices on identifiers.
        ],

        'number literal': [
            ( '[0-9]+(?=(?:[0-9_]*[0-9])?N)', Number, 'decimal n literal' ),
            ( r'([+\-]?)([0-9]+)',
              bygroups( Operator, Number ),
              'decimal z literal' ),
            ( r'(\\b)([01]+)(?=(?:[01_]*[01])?N)',
              bygroups( String.Affix, Number.Bin ),
              'binary n literal' ),
            ( r'([+\-]?)(\\b)([01]+)',
              bygroups( Operator, String.Affix, Number.Bin ),
              'binary z literal' ),
            ( r'(\\x)([0-9A-Fa-f]+)(?=(?:[0-9A-Fa-f_]*[0-9A-Fa-f])?N)',
              bygroups( String.Affix, Number.Hex ),
              'hexadecimal n literal' ),
            ( r'([+\-]?)(\\x)([0-9A-Fa-f]+)',
              bygroups( Operator, String.Affix, Number.Hex ),
              'hexadecimal z literal' ),
            include( 'nominative c zero escape sequence' ),
        ],

        'decimal z literal': [
            include( 'decimal digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'decimal flpn postradix literal' ) ),
            ( r'([Ee])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'decimal flpn exponent literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'decimal fxpn postradix literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'decimal q denominator literal' ) ),
            ( r'[+\-](?=[0-9](?:.*[0-9])?[ij])', Operator,
              ( '#pop', 'decimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'decimal flpn postradix literal': [
            include( 'decimal digits' ),
            ( r'([Ee])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'decimal flpn exponent literal' ) ),
            ( r'[+\-](?=[0-9](?:.*[0-9])?[ij])', Operator,
              ( '#pop', 'decimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'decimal flpn exponent literal': [
            include( 'decimal digits' ),
            ( r'[+\-](?=[0-9](?:.*[0-9])?[ij])', Operator,
              ( '#pop', 'decimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'decimal fxpn postradix literal': [
            include( 'decimal digits' ),
            ( r'[+\-](?=[0-9](?:.*[0-9])?[ij])', Operator,
              ( '#pop', 'decimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'decimal q denominator literal': [
            include( 'decimal digits' ),
            ( r'[+\-](?=[0-9](?:.*[0-9])?[ij])', Operator,
              ( '#pop', 'decimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'decimal z im literal': [
            include( 'decimal digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'decimal flpn postradix im literal' ) ),
            ( r'([Ee])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'decimal flpn exponent im literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'decimal fxpn postradix im literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'decimal q denominator im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'decimal flpn postradix im literal': [
            include( 'decimal digits' ),
            ( r'([Ee])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'decimal flpn exponent im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'decimal flpn exponent im literal': [
            include( 'decimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'decimal fxpn postradix im literal': [
            include( 'decimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'decimal q denominator im literal': [
            include( 'decimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'decimal n literal': [
            include( 'decimal digits' ),
            ( 'N', String.Affix, '#pop' ),
            default( '#pop' ),
        ],

        'binary z literal': [
            include( 'binary digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'binary flpn postradix literal' ) ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'binary flpn exponent literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'binary fxpn postradix literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'binary q denominator literal' ) ),
            ( r'[+\-](?=[01](?:.*[01])?[ij])', Operator,
              ( '#pop', 'binary z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'binary flpn postradix literal': [
            include( 'binary digits' ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'binary flpn exponent literal' ) ),
            ( r'[+\-](?=[01](?:.*[01])?[ij])', Operator,
              ( '#pop', 'binary z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'binary flpn exponent literal': [
            include( 'binary digits' ),
            ( r'[+\-](?=[01](?:.*[01])?[ij])', Operator,
              ( '#pop', 'binary z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'binary fxpn postradix literal': [
            include( 'binary digits' ),
            ( r'[+\-](?=[01](?:.*[01])?[ij])', Operator,
              ( '#pop', 'binary z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'binary q denominator literal': [
            include( 'binary digits' ),
            ( r'[+\-](?=[01](?:.*[01])?[ij])', Operator,
              ( '#pop', 'binary z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'binary z im literal': [
            include( 'binary digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'binary flpn postradix im literal' ) ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'binary flpn exponent im literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'binary fxpn postradix im literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'binary q denominator im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'binary flpn postradix im literal': [
            include( 'binary digits' ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'binary flpn exponent im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'binary flpn exponent im literal': [
            include( 'binary digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'binary fxpn postradix im literal': [
            include( 'binary digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'binary q denominator im literal': [
            include( 'binary digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'binary n literal': [
            include( 'binary digits' ),
            ( 'N', String.Affix, '#pop' ),
            default( '#pop' ),
        ],

        'hexadecimal z literal': [
            include( 'hexadecimal digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'hexadecimal flpn postradix literal' ) ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'hexadecimal flpn exponent literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'hexadecimal fxpn postradix literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'hexadecimal q denominator literal' ) ),
            ( r'[+\-](?=[0-9A-Fa-f](?:.*[0-9A-Fa-f])?[ij])', Operator,
              ( '#pop', 'hexadecimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'hexadecimal flpn postradix literal': [
            include( 'hexadecimal digits' ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'hexadecimal flpn exponent literal' ) ),
            ( r'[+\-](?=[0-9A-Fa-f](?:.*[0-9A-Fa-f])?[ij])', Operator,
              ( '#pop', 'hexadecimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'hexadecimal flpn exponent literal': [
            include( 'hexadecimal digits' ),
            ( r'[+\-](?=[0-9A-Fa-f](?:.*[0-9A-Fa-f])?[ij])', Operator,
              ( '#pop', 'hexadecimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'hexadecimal fxpn postradix literal': [
            include( 'hexadecimal digits' ),
            ( r'[+\-](?=[0-9A-Fa-f](?:.*[0-9A-Fa-f])?[ij])', Operator,
              ( '#pop', 'hexadecimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'hexadecimal q denominator literal': [
            include( 'hexadecimal digits' ),
            ( r'[+\-](?=[0-9A-Fa-f](?:.*[0-9A-Fa-f])?[ij])', Operator,
              ( '#pop', 'hexadecimal z im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            default( '#pop' ),
        ],
        'hexadecimal z im literal': [
            include( 'hexadecimal digits' ),
            ( r'\.', String.Other,
              ( '#pop', 'hexadecimal flpn postradix im literal' ) ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
              ( '#pop', 'hexadecimal flpn exponent im literal' ) ),
            ( "'", String.Other,
              ( '#pop', 'hexadecimal fxpn postradix im literal' ) ),
            ( '/', String.Other,
              ( '#pop', 'hexadecimal q denominator im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'hexadecimal flpn postradix im literal': [
            include( 'hexadecimal digits' ),
            ( r'([Pp])([+\-]?)', bygroups( String.Other, Operator ),
             ( '#pop', 'hexadecimal flpn exponent im literal' ) ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'hexadecimal flpn exponent im literal': [
            include( 'hexadecimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'hexadecimal fxpn postradix im literal': [
            include( 'hexadecimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'hexadecimal q denominator im literal': [
            include( 'hexadecimal digits' ),
            ( '[ij]', String.Other, '#pop' ),
            ( '.', Error, '#pop' ),
        ],
        'hexadecimal n literal': [
            include( 'hexadecimal digits' ),
            ( 'N', String.Affix, '#pop' ),
            default( '#pop' ),
        ],

        # C0 Control Codes
        #   https://en.wikipedia.org/wiki/C0_and_C1_control_codes
        #   https://unicode.org/charts/PDF/U0000.pdf
        'nominative c zero escape sequence': [
            ( r'(\\C0<)({})(>)'.format(
                '|'.join( (
                    'NUL', 'SUB',
                    'SOH', 'STX', 'ETX', 'EOT', 'ETB', 'EM',
                    'ENQ', 'ACK', 'NAK', 'SYN', 'CAN',
                    'BEL', 'ESC',
                    'BS', 'HT', 'LF', 'VT', 'FF', 'CR',
                    'SO', 'SI',
                    'DLE', 'DC1', 'DC2', 'DC3', 'DC4',
                    'FS', 'GS', 'RS', 'US',
                ) ) ),
              bygroups( String.Escape, Name.Entity, String.Escape ) ),
            ( r'(\\C0<)(.*?)(>)',
              bygroups( String.Escape, Error, String.Escape ) ),
        ],

        'unicode literal': [
            ( r'(\\U)(?:(10|0?[0-9A-Fa-f])(_?))?([0-9A-Fa-f]{1,4})',
              bygroups( String.Escape, Number.Hex, Punctuation, Number.Hex ) ),
            include( 'nominative unicode literal' ),
        ],
        'nominative unicode literal': [
            ( r'(\\U<)([0-9A-Za-z](?:[0-9A-Za-z ]*[0-9A-Za-z])?)(>)',
              bygroups( String.Escape, Name.Entity, String.Escape ) ),
            ( r'(\\U<)(.*?)(>)',
              bygroups( String.Escape, Error, String.Escape ) ),
        ],

        'decimal digits': [
            ( r'[0-9]+', Number ),
            ( r'_+(?=[^0-9])', Error ),
            ( r'_+', Punctuation ),
        ],
        'binary digits': [
            ( r'[01]+', Number.Bin ),
            ( r'_+(?=[^01])', Error ),
            ( r'_+', Punctuation ),
        ],
        'hexadecimal digits': [
            ( r'[0-9A-Fa-f]+', Number.Hex ),
            ( r'_+(?=[^0-9A-Fa-f])', Error ),
            ( r'_+', Punctuation ),
        ],

        'operator': [
            ( r'(?:\.{3})', Operator ),
            ( r'(?:\.{2})' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:\.)(?=[\w\[])', Operator ),
            ( r'(?:\+|\-|\*|/)' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:\((?:\+|\*)\))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:\*(?:\*|<|>))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:Z(?:/|\%))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:<|<>|>|<=|==|>=|!=)' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:\((?:<>|==|!=)\))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:!?is\?)' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:and\??|or\??|not\?)' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:\((?:and\??|or\??)\))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:b(?:&|\||\^|<<|>>))' + HEADSTART_SUFFIX, Operator ),
            ( r'(?:b~)' + HEADSTART_SUFFIX, Operator ),
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
