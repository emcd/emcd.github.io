import platform.posix.*

val stderr = fdopen(2, "w")

fun main() {
    eprintln(format_title("Hello, world!"))
    eprintln(format_title("Hello, world!", variant = "Kotlin"))
    eprintln(format_title("Hello, world!", version = "1.0"))
    eprintln(format_title(
        "Hello, world!", variant = "Kotlin", version = "1.0"
    ))
}

fun eprintln(message: String) {
    fprintf(stderr, message + "\n")
    fflush(stderr)
}

fun format_title(
    base: String, variant: String? = null, version: String? = null
): String {
    val output = mutableListOf(base)
    if (variant != null) {
        variant.length  // Compilation error if not wrapped in null check.
        output.add("[$variant]")
    }
    if (version != null) {
        output.add("($version)")
    }
    return output.joinToString(separator = " ")
}
