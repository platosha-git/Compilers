package main

import (
	"fmt"
)

func main() {
	regular := ""
	fmt.Scan(&regular)

	tokens := Parser.parse([]rune(regular))
	for i := 0; i < len(tokens); i++ {
		fmt.Print(tokens[i].name, tokens[i].value)
	}
	//1. По регулярному выражению построить НКА
	//NFA := nfa.Build(regular)

}
