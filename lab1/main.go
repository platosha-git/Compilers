package main

import (
	"fmt"
	//. "lab001/nfa"
	. "lab1/parser"
)

func main() {
	regular := ""
	fmt.Scan(&regular)

	var parser Parser
	tokens := parser.Parse([]rune(regular))

	for i := 0; i < len(tokens); i++ {
		fmt.Println(tokens[i])
	}

	//1. По регулярному выражению построить НКА
	//var nfa NFA
	//nfa.Build(tokens)

}
