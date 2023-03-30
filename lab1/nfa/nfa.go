package nfa

import (
	"fmt"
	. "lab1/parser"
	"strconv"
)

type nodeGraph struct {
	start state
	end   state
	isEnd bool
}

type NFA struct {
	alphabet   []string
	stack      stack
	stateCount int

	head     nodeGraph
	endState []state
}

func (nfa *NFA) initAlphabet(charSet map[string]bool) {
	for key, value := range charSet {
		if value == true {
			nfa.alphabet = append(nfa.alphabet, key)
		}
	}

}

func (nfa *NFA) Build(tokens []Symbol) {
	charSet := make(map[string]bool)

	for i := 0; i < len(tokens); i++ {
		curToken := tokens[i]

		if curToken.Name == "CHAR" {
			nfa.handleChar(curToken)
			charSet[curToken.Value] = true
		} else if curToken.Name == "CONCAT" {
			nfa.handleConcat()
		} else if curToken.Name == "OR" {
			nfa.handleOr()
		} else if curToken.Name == "STAR" {
			nfa.handleStar()
		}
	}

	nfa.initAlphabet(charSet)
	_, nfa.head = nfa.stack.Pop()
}

func (nfa *NFA) createState() state {
	nfa.stateCount++
	name := "s" + strconv.Itoa(nfa.stateCount)
	newState := state{name: name, transitions: make(map[string]state), isEnd: false, isStart: false}
	return newState
}

func (nfa *NFA) handleChar(symb Symbol) {
	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.transitions[symb.Value] = s1

	curNfa := nodeGraph{start: s0, end: s1, isEnd: true}
	nfa.endState = append(nfa.endState, s1)
	nfa.stack = nfa.stack.Push(curNfa)
}

func idxInArray(st state, stArr []state) int {
	idxToRemove := -1
	for i := 0; i < len(stArr); i++ {
		if stArr[i].name == st.name {
			idxToRemove = i
		}
	}

	return idxToRemove
}

func remove(stArr []state, idx int) []state {
	stArr[idx] = stArr[len(stArr)-1]
	return stArr[:len(stArr)-1]
}

func (nfa *NFA) handleConcat() {
	_, n2 := nfa.stack.Pop()
	_, n1 := nfa.stack.Pop()
	n1.isEnd = false

	idx := idxInArray(n1.end, nfa.endState)
	if idx >= 0 {
		nfa.endState = remove(nfa.endState, idx)
	}

	n1.end.epsilon = n2.start.epsilon
	n1.end.transitions = n2.start.transitions

	curNfa := nodeGraph{start: n1.start, end: n2.end, isEnd: true}
	nfa.endState = append(nfa.endState, n2.end)
	nfa.stack.Push(curNfa)
}

func (nfa *NFA) handleOr() {
	_, n2 := nfa.stack.Pop()
	_, n1 := nfa.stack.Pop()

	s0 := nfa.createState()
	s0.epsilon = append(s0.epsilon, n1.start, n2.start)
	s3 := nfa.createState()

	n1.end.epsilon = append(n1.end.epsilon, s3)
	n2.end.epsilon = append(n2.end.epsilon, s3)

	n1.end.isEnd = false
	n2.end.isEnd = false

	idx := idxInArray(n1.end, nfa.endState)
	if idx >= 0 {
		nfa.endState = remove(nfa.endState, idx)
	}

	idx = idxInArray(n2.end, nfa.endState)
	if idx >= 0 {
		nfa.endState = remove(nfa.endState, idx)
	}

	curNfa := nodeGraph{start: s0, end: s3, isEnd: true}
	nfa.endState = append(nfa.endState, s3)
	nfa.stack.Push(curNfa)
}

func (nfa *NFA) handleStar() {
	_, n1 := nfa.stack.Pop()

	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.epsilon = append(s0.epsilon, n1.start)
	s0.epsilon = append(s0.epsilon, s1)

	n1.end.epsilon = append(n1.end.epsilon, s1, n1.start)
	n1.end.isEnd = false

	idx := idxInArray(n1.end, nfa.endState)
	if idx >= 0 {
		nfa.endState = remove(nfa.endState, idx)
	}

	curNfa := nodeGraph{start: s0, end: s1, isEnd: true}
	nfa.endState = append(nfa.endState, s1)
	nfa.stack.Push(curNfa)
}

func (nfa *NFA) Output() {
	var stateArr []state

	stateArr = append(stateArr, nfa.head.start)
	for i := 0; i < len(stateArr); i++ {
		curState := stateArr[i]
		fmt.Println(i, ") from:", curState.name)
		fmt.Println("by epsilon to:")

		for i := 0; i < len(curState.epsilon); i++ {
			epsState := curState.epsilon[i]
			fmt.Println(epsState)

			idx := idxInArray(epsState, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, epsState)
			}
		}

		fmt.Println("")
		for key, value := range curState.transitions {
			fmt.Print("by ", key, " to ", value.name)

			idx := idxInArray(value, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, value)
			}
		}

		fmt.Println("")

	}
}
