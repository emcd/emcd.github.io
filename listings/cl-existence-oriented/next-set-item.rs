use std::collections::HashSet;
use std::io::{stderr, Write};

fn main() {
    let nothing = HashSet::new();
    let mut things = HashSet::new();
    things.insert(42);
    unwrap_print_set_element(things);
    unwrap_print_set_element(nothing);
}

fn unwrap_print_set_element(elements: HashSet<i32>) {
    let mut iterator = elements.iter();
    if let Some(element) = iterator.next() {
        writeln!(stderr(), "set element: {}", element).ok();
    }
}
