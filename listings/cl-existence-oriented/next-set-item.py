from sys import stderr

def print_set_element( elements ):
    element = next( iter( elements ) )
    print( f"set element: {element}", file = stderr )

def safe_print_set_element( elements ):
    if elements:
        element = next( iter( elements ) )
        print( f"set element: {element}", file = stderr )

if '__main__' == __name__:
    nothing = frozenset( )
    things = frozenset( { 42 } )
    safe_print_set_element( things )
    safe_print_set_element( nothing )
    print_set_element( things )
    print_set_element( nothing )  # raises StopIteration
