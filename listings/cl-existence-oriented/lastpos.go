package main

import "fmt"
import "os"

func main() {
	items := []int{42}
	emptyItems := []int{}
	safePrintLastItem(items)
	safePrintLastItem(emptyItems)
	printLastItem(items)
	printLastItem(emptyItems) /* panics */
}

func printLastItem(items []int) {
	fmt.Fprintf(os.Stderr, "last item: %d\n", items[len(items)-1])
}

func safePrintLastItem(items []int) {
	count := len(items)
	if count > 0 {
		lastItem := items[count-1]
		fmt.Fprintf(os.Stderr, "last item: %d\n", lastItem)
	}
}
