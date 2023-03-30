package nfa

import (
	"fmt"
	. "lab1/parser"
	"strconv"
)

type NFA struct {
	alphabet   []string
	stack      stack
	stateCount int

	head     nodeGraph
	endState map[string]bool
}

func (nfa *NFA) initAlphabet(charSet map[string]bool) {
	for key, value := range charSet {
		if value == true {
			nfa.alphabet = append(nfa.alphabet, key)
		}
	}

}

var keyName []string
var keyState []state

func (nfa *NFA) Build(tokens []Symbol) {
	charSet := make(map[string]bool)
	nfa.endState = make(map[string]bool)

	for i := 0; i < len(tokens); i++ {
		curToken := tokens[i]

		if curToken.Desc == "CHAR" {
			nfa.handleChar(curToken)
			charSet[curToken.Value] = true
		} else if curToken.Desc == "CONCAT" {
			nfa.handleConcat()
		} //else if curToken.Name == "OR" {
		//	nfa.handleOr()
		//} // else if curToken.Name == "STAR" {
		//	nfa.handleStar()
		//}
	}

	nfa.initAlphabet(charSet)
	nfa.stack, nfa.head = nfa.stack.Pop()
}

func (nfa *NFA) createState() state {
	nfa.stateCount++
	name := "s" + strconv.Itoa(nfa.stateCount)
	trans := make(map[string]state)
	newState := state{name: name, transitions: trans, isEnd: false, isStart: false}
	return newState
}

func (nfa *NFA) handleChar(symb Symbol) {
	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.transitions[symb.Value] = s1

	curNfa := nodeGraph{start: s0, end: s1, isEnd: true}
	nfa.endState[s1.name] = true
	//nfa.endState = append(nfa.endState, s1)
	nfa.stack = nfa.stack.Push(curNfa)
}

func idxInArray(st state, stArr []state) int {
	idxToRemove := -1
	for i := 0; i < len(stArr); i++ {
		if stArr[i].name == st.name {
			idxToRemove = i
			break
		}
	}

	return idxToRemove
}

func remove(stArr []state, idx int) []state {
	stArr[idx] = stArr[len(stArr)-1]
	return stArr[:len(stArr)-1]
}

func (nfa *NFA) handleConcat() {
	var n1, n2 nodeGraph
	nfa.stack, n2 = nfa.stack.Pop()
	nfa.stack, n1 = nfa.stack.Pop()

	n1.isEnd = false

	//idx := idxInArray(n1.end, nfa.endState)
	//if idx >= 0 {
	nfa.endState[n1.end.name] = false
	//nfa.endState = remove(nfa.endState, idx)
	//}

	keyName = append(keyName, n1.end.name)
	keyState = append(keyState, n2.start)

	n1.end.epsilon = n2.start.epsilon
	n1.end.transitions = n2.start.transitions

	curNfa := nodeGraph{start: n1.start, end: n2.end, isEnd: true}
	nfa.endState[n2.end.name] = true
	//nfa.endState = append(nfa.endState, n2.end)
	nfa.stack = nfa.stack.Push(curNfa)
}

//func (nfa *NFA) handleOr() {
//	_, n2 := nfa.stack.Pop()
//	_, n1 := nfa.stack.Pop()
//
//	s0 := nfa.createState()
//	s0.epsilon = append(s0.epsilon, n1.start, n2.start)
//	s3 := nfa.createState()
//
//	n1.end.epsilon = append(n1.end.epsilon, s3)
//	n2.end.epsilon = append(n2.end.epsilon, s3)
//
//	n1.end.isEnd = false
//	n2.end.isEnd = false
//
//	idx := idxInArray(n1.end, nfa.endState)
//	if idx >= 0 {
//		nfa.endState = remove(nfa.endState, idx)
//	}
//
//	idx = idxInArray(n2.end, nfa.endState)
//	if idx >= 0 {
//		nfa.endState = remove(nfa.endState, idx)
//	}
//
//	curNfa := nodeGraph{start: s0, end: s3, isEnd: true}
//	nfa.endState = append(nfa.endState, s3)
//	nfa.stack = nfa.stack.Push(curNfa)
//}

//func (nfa *NFA) handleStar() {
//	_, n1 := nfa.stack.Pop()
//
//	s0 := nfa.createState()
//	s1 := nfa.createState()
//
//	s0.epsilon = append(s0.epsilon, n1.start)
//	s0.epsilon = append(s0.epsilon, s1)
//
//	n1.end.epsilon = append(n1.end.epsilon, s1, n1.start)
//	n1.end.isEnd = false
//
//	idx := idxInArray(n1.end, nfa.endState)
//	if idx >= 0 {
//		nfa.endState = remove(nfa.endState, idx)
//	}
//
//	curNfa := nodeGraph{start: s0, end: s1, isEnd: true}
//	nfa.endState = append(nfa.endState, s1)
//	nfa.stack = nfa.stack.Push(curNfa)
//}

func idxNameInArray(name string, nameArray []string) int {
	idxInArray := -1
	for i := 0; i < len(nameArray); i++ {
		if nameArray[i] == name {
			idxInArray = i
			break
		}
	}

	return idxInArray
}

func (nfa *NFA) Output() {
	var stateArr []state
	stateArr = append(stateArr, nfa.head.start)

	for i := 0; i < len(stateArr); i++ {
		curState := stateArr[i]

		idx := idxNameInArray(curState.name, keyName)
		if idx >= 0 {
			curState.epsilon = keyState[idx].epsilon
			curState.transitions = keyState[idx].transitions
		}

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

		for key, value := range curState.transitions {
			fmt.Println("by ", key, " to ", value.name)

			idx := idxInArray(value, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, value)
			}
		}
	}
}
