package main

import (
	. "lab1/automations/dfa"
	. "lab1/automations/nfa"
	. "lab1/parser"
)

func main() {
	inputString := "(a|b)*abb"
	// fmt.Scan(&inputString)

	var parser Parser
	regularString := parser.Parse([]rune(inputString))

	//1. По регулярному выражению построить НКА
	var nfa NFA
	nfa.Build(regularString)
	nfa.Output()

	var dfa DFA
	dfa.Build(nfa)
	dfa.Output()
}
