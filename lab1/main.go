package main

import (
	"fmt"
	. "lab1/nfa"
	. "lab1/parser"
)

func main() {
	inputString := ""
	fmt.Scan(&inputString)

	var parser Parser
	regularString := parser.Parse([]rune(inputString))

	//1. По регулярному выражению построить НКА
	var nfa NFA
	nfa.Build(regularString)
	nfa.Output()

}
