from sys import stderr

def print_last_item( items ):
    print( "last item: {}".format( items[ -1 ] ), file = stderr )

def safe_print_last_item( items ):
    if items: print( "last item: {}".format( items[ -1 ] ), file = stderr )

if '__main__' == __name__:
    empty_items = ( )
    items = ( 42, )
    safe_print_last_item( items )
    safe_print_last_item( empty_items )
    print_last_item( items )
    print_last_item( empty_items )  # raises IndexError
