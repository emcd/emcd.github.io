use std::collections::HashMap;
use std::io::{stderr, Write};

fn main() {
    let empty_haystack = HashMap::new();
    let mut haystack = HashMap::new();
    haystack.insert("needle", 42);
    unwrap_print_needle(haystack);
    unwrap_print_needle(empty_haystack);
}

fn unwrap_print_needle(haystack: HashMap<&str, i32>) {
    if let Some(needle) = haystack.get("needle") {
        writeln!(stderr(), "needle: {}", needle).ok();
    }
}
