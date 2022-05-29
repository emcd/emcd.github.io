def format_title_sentinels( base, variant = None, version = None ):
    output = [ base ]
    if variant is not None:
        output.append( f"[{variant}]" )
    if version is not None:
        output.append( f"({version})" )
    return ' '.join( output )

def format_title_args_dict( base, **nomargs ):
    output = [ base ]
    if 'variant' in nomargs:
        output.append( "[{}]".format( nomargs[ 'variant' ] ) )
    if 'version' in nomargs:
        output.append( "({})".format( nomargs[ 'version' ] ) )
    return ' '.join( output )

if '__main__' == __name__:
    from functools import partial as partial_function
    from sys import stderr
    eprint = partial_function( print, file = stderr )
    eprint( format_title_sentinels( 'Hello, world!' ) )
    eprint( format_title_sentinels( 'Hello, world!', variant = 'Python' ) )
    eprint( format_title_sentinels( 'Hello, world!', version = '1.0' ) )
    eprint( format_title_sentinels(
        'Hello, world!', variant = 'Python', version = '1.0' ) )
    # prints: Hello, world!
    eprint( format_title_sentinels( 'Hello, world!', variant = None ) )
    eprint( format_title_args_dict( 'Hello, world!' ) )
    eprint( format_title_args_dict( 'Hello, world!', variant = 'Python' ) )
    eprint( format_title_args_dict( 'Hello, world!', version = '1.0' ) )
    eprint( format_title_args_dict(
        'Hello, world!', variant = 'Python', version = '1.0' ) )
    # prints: Hello, world! [None]
    eprint( format_title_args_dict( 'Hello, world!', variant = None ) )
