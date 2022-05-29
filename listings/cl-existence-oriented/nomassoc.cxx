#include <iostream>
#include <map>
#include <string>

void print_needle_zinit( const std::map<std::string, int>& haystack ) {
    std::map<std::string, int> mutable_haystack( haystack );
    std::cerr << "needle: " << mutable_haystack[ "needle" ] << std::endl;
}

void print_needle_checked( const std::map<std::string, int>& haystack ) {
    std::cerr << "needle: " << haystack.at( "needle" ) << std::endl;
}

void safe_print_needle_zinit( const std::map<std::string, int>& haystack ) {
    if ( haystack.contains( "needle" ) ) { // Requires C++20 std::map.
        std::map<std::string, int> mutable_haystack( haystack );
        std::cerr << "needle: " << mutable_haystack[ "needle" ] << std::endl;
    }
}

void safe_print_needle_checked( const std::map<std::string, int>& haystack ) {
    if ( haystack.contains( "needle" ) ) { // Requires C++20 std::map.
        std::cerr << "needle: " << haystack.at( "needle" ) << std::endl;
    }
}

void unwrap_print_needle( const std::map<std::string, int>& haystack ) {
    const auto wrapped_needle = haystack.find( "needle" );
    if ( wrapped_needle != haystack.end( ) ) {
        std::cerr << "needle: " << wrapped_needle->second << std::endl;
    }
}

int main( ) {
    const std::map<std::string, int> empty_haystack;
    const std::map<std::string, int> haystack { { "needle", 42 } };

    safe_print_needle_zinit( haystack );
    safe_print_needle_zinit( empty_haystack );
    safe_print_needle_checked( haystack );
    safe_print_needle_checked( empty_haystack );
    unwrap_print_needle( haystack );
    unwrap_print_needle( empty_haystack );
    print_needle_zinit( haystack );
    print_needle_zinit( empty_haystack );  // prints: 0
    print_needle_checked( haystack );
    print_needle_checked( empty_haystack );  // raises: std::out_of_range
}
