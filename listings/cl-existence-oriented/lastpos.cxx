#include <iostream>
#include <vector>

void print_last_item( const std::vector<int>& items ) {
    std::cerr << "last item: " << items.back( ) << std::endl;
}

void safe_print_last_item( const std::vector<int>& items ) {
    if ( !items.empty( ) ) {
        std::cerr << "last item: " << items.back( ) << std::endl;
    }
}

int main( ) {
    const std::vector<int> empty_items;
    const std::vector<int> items { 42 };

    safe_print_last_item( items );
    safe_print_last_item( empty_items );
    print_last_item( items );
    print_last_item( empty_items );  // undefined behavior
}
