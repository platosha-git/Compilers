package nfa

import _ "lab1/parser"

type NFA struct {
	alphabet   []string
	stack      []string
	stateCount int

	head     []string
	endState []string
}

func (nfa *NFA) Build() []Symbol {
}
