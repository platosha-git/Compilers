package main

import (
	"fmt"
	. "lab1/nfa"
	. "lab1/parser"
)

func main() {
	regular := ""
	fmt.Scan(&regular)

	var parser Parser
	tokens := parser.Parse([]rune(regular))

	//1. По регулярному выражению построить НКА
	var nfa NFA
	nfa.Build(tokens)
	nfa.Output()

}
