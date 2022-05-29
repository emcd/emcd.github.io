use std::io::{stderr, Write};

fn main() {
    writeln!(
        stderr(), "{}",
        format_title("Hello, world!", None, None)
    ).ok();
    writeln!(
        stderr(), "{}",
        format_title("Hello, world!", Some("Rust"), None)
    ).ok();
    writeln!(
        stderr(), "{}",
        format_title("Hello, world!", None, Some("1.0"))
    ).ok();
    writeln!(
        stderr(), "{}",
        format_title("Hello, world!", Some("Rust"), Some("1.0"))
    ).ok();
}

fn format_title(base: &str, variant: Option<&str>, version: Option<&str>) -> String {
    let mut output: Vec<String> = vec![base.to_string()];
    if let Some(data) = variant {
        output.push(format!("[{}]", data));
    }
    if let Some(data) = version {
        output.push(format!("({})", data));
    }
    output.join(" ")
}
