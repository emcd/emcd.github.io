#include <iostream>
#include <set>

void unwrap_print_set_element( const std::set<int>& elements ) {
    const auto wrapped_element = elements.cbegin( );
    if ( wrapped_element != elements.cend( ) ) {
        std::cerr << "set element: " << *wrapped_element << std::endl;
    }
}

int main ( ) {
    const std::set<int> nothing;
    const std::set<int> things { 42 };

    unwrap_print_set_element( things );
    unwrap_print_set_element( nothing );
}
