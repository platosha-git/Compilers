package nfa

import (
	"fmt"
	. "lab1/base"
	. "lab1/parser"
	"strconv"
)

type NFA struct {
	states         Stack
	chStates       ChangedStates
	numberOfStates int

	startState  NodeGraph
	finalStates map[string]bool

	alphabet []string
}

func (nfa *NFA) Build(regular []Symbol) {
	charSet := make(map[string]bool)
	nfa.finalStates = make(map[string]bool)

	for i := 0; i < len(regular); i++ {
		curSymbol := regular[i]

		switch curSymbol.Desc {
		case "CHAR":
			nfa.handleChar(curSymbol)
			charSet[curSymbol.Value] = true
		case "OR":
			nfa.handleOr()
		case "STAR":
			nfa.handleStar()
		case "CONCAT":
			nfa.handleConcat()
		}
	}

	nfa.initAlphabet(charSet)
	nfa.states, nfa.startState = nfa.states.Pop()
}

func (nfa *NFA) handleChar(symbol Symbol) {
	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.Transitions[symbol.Value] = s1

	nfa.addNode(s0, s1)
}

func (nfa *NFA) handleConcat() {
	var n1, n2 NodeGraph
	nfa.states, n2 = nfa.states.Pop()
	nfa.states, n1 = nfa.states.Pop()

	n1.IsEnd = false
	nfa.finalStates[n1.End.Name] = false

	nfa.chStates.NameConcat = append(nfa.chStates.NameConcat, n1.End.Name)
	nfa.chStates.StateConcat = append(nfa.chStates.StateConcat, n2.Start)

	nfa.addNode(n1.Start, n2.End)
}

func (nfa *NFA) handleOr() {
	var n1, n2 NodeGraph
	nfa.states, n2 = nfa.states.Pop()
	nfa.states, n1 = nfa.states.Pop()

	s0 := nfa.createState()
	s3 := nfa.createState()

	s0.Epsilon = append(s0.Epsilon, n1.Start, n2.Start)

	n1.End.IsEnd = false
	n2.End.IsEnd = false

	nfa.finalStates[n1.End.Name] = false
	nfa.finalStates[n2.End.Name] = false

	nfa.chStates.NameOr = append(nfa.chStates.NameOr, n1.End.Name, n2.End.Name)
	nfa.chStates.StateOr = append(nfa.chStates.StateOr, s3, s3)

	nfa.addNode(s0, s3)
}

func (nfa *NFA) handleStar() {
	var n1 NodeGraph
	nfa.states, n1 = nfa.states.Pop()

	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.Epsilon = append(s0.Epsilon, n1.Start, s1)

	n1.End.IsEnd = false
	nfa.finalStates[n1.End.Name] = false

	nfa.chStates.NameStar = append(nfa.chStates.NameStar, n1.End.Name)
	nfa.chStates.StateStar = append(nfa.chStates.StateStar, s1, n1.Start)

	nfa.addNode(s0, s1)
}

// Helper functions fot handlers
func (nfa *NFA) addNode(start State, end State) {
	newNode := NodeGraph{Start: start, End: end, IsEnd: true}

	nfa.finalStates[end.Name] = true
	nfa.states = nfa.states.Push(newNode)
}

func (nfa *NFA) initAlphabet(charSet map[string]bool) {
	for key, value := range charSet {
		if value == true {
			nfa.alphabet = append(nfa.alphabet, key)
		}
	}
}

func (nfa *NFA) createState() State {
	nfa.numberOfStates++
	name := "s" + strconv.Itoa(nfa.numberOfStates)

	trans := make(map[string]State)
	newState := State{Name: name, Transitions: trans, IsEnd: false, IsStart: false}

	return newState
}

func idxInStateArray(st State, stArr []State) int {
	idxToRemove := -1
	for i := 0; i < len(stArr); i++ {
		if stArr[i].Name == st.Name {
			idxToRemove = i
			break
		}
	}

	return idxToRemove
}

func idxInStringArray(name string, nameArray []string) int {
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
	var stateArr []State
	stateArr = append(stateArr, nfa.startState.Start)

	for i := 0; i < len(stateArr); i++ {
		curState := stateArr[i]

		idx := idxInStringArray(curState.Name, nfa.chStates.NameConcat)
		if idx >= 0 {
			curState.Epsilon = nfa.chStates.StateConcat[idx].Epsilon
			curState.Transitions = nfa.chStates.StateConcat[idx].Transitions
		}

		idx = idxInStringArray(curState.Name, nfa.chStates.NameOr)
		if idx >= 0 {
			curState.Epsilon = append(curState.Epsilon, nfa.chStates.StateOr[idx])
		}

		idx = idxInStringArray(curState.Name, nfa.chStates.NameStar)
		if idx >= 0 {
			curState.Epsilon = append(curState.Epsilon, nfa.chStates.StateStar[2*idx], nfa.chStates.StateStar[2*idx+1])
		}

		fmt.Println(i, ") from:", curState.Name)
		fmt.Print("by epsilon to:")

		for i := 0; i < len(curState.Epsilon); i++ {
			epsState := curState.Epsilon[i]
			fmt.Print(epsState.Name + " ")

			idx := idxInStateArray(epsState, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, epsState)
			}
		}

		fmt.Println()
		for key, value := range curState.Transitions {
			fmt.Println("by ", key, " to ", value.Name)

			idx := idxInStateArray(value, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, value)
			}
		}
	}
}
