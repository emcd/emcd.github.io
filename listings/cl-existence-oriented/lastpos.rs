use std::io::{stderr, Write};

fn main() {
    let empty_items = vec![];
    let items = vec![42];
    unwrap_print_last_item(items);
    unwrap_print_last_item(empty_items);
}

fn unwrap_print_last_item(items: Vec<i32>) {
    if let Some(last_item) = items.last() {
        writeln!(stderr(), "last item: {}", last_item).ok();
    }
}
