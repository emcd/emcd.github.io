package main

import "fmt"
import "os"

func main() {
	emptyHaystack := make(map[string]int)
	haystack := make(map[string]int)
	haystack["needle"] = 42
	safePrintNeedle(haystack)
	safePrintNeedle(emptyHaystack)
	printNeedle(haystack)
	printNeedle(emptyHaystack) /* prints 0, which is not the needle */
}

func printNeedle(haystack map[string]int) {
	needle, _ := haystack["needle"]
	fmt.Fprintf(os.Stderr, "needle: %d\n", needle)
}

func safePrintNeedle(haystack map[string]int) {
	needle, ok := haystack["needle"]
	if ok {
		fmt.Fprintf(os.Stderr, "needle: %d\n", needle)
	}
}
