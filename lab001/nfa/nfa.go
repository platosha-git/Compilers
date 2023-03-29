package nfa

import _ "lab001/parser"

type NFA struct {
	alphabet   []string
	stack      []string
	stateCount int

	head     []string
	endState []string
}

func (nfa *NFA) Build() []Symbol {
}
