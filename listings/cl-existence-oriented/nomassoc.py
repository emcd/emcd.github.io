from sys import stderr

def print_needle( haystack ):
    print( "needle: {}".format( haystack[ 'needle' ], file = stderr ) )

def print_needle_sentinel( haystack ):
    needle = haystack.get( 'needle' )
    if needle is not None:
        print( f"needle: {needle}", file = stderr )

def print_needle_if_exists( haystack ):
    if 'needle' in haystack:
        print( "needle: {}".format( haystack[ 'needle' ], file = stderr ) )

if '__main__' == __name__:
    empty_haystack = { }
    haystack = dict( needle = 42 )
    evil_haystack = dict( needle = None )
    print_needle_sentinel( haystack )
    print_needle_sentinel( evil_haystack )  # does not print
    print_needle_sentinel( empty_haystack )
    print_needle_if_exists( haystack )
    print_needle_if_exists( evil_haystack )  # prints: None
    print_needle_if_exists( empty_haystack )
    print_needle( haystack )
    print_needle( evil_haystack )
    print_needle( empty_haystack )  # raises KeyError
