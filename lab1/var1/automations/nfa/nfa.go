package nfa

import (
	"fmt"
	. "lab1/base"
	. "lab1/parser"
	"strconv"
)

type NFA struct {
	states         Stack
	ChStates       ChangedStates
	numberOfStates int

	StartState  NodeGraph
	FinalStates map[string]bool

	Alphabet []string
}

func (nfa *NFA) Build(regular []Symbol) {
	charSet := make(map[string]bool)
	nfa.FinalStates = make(map[string]bool)

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
	nfa.states, nfa.StartState = nfa.states.Pop()
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
	nfa.FinalStates[n1.End.Name] = false

	nfa.ChStates.NameConcat = append(nfa.ChStates.NameConcat, n1.End.Name)
	nfa.ChStates.StateConcat = append(nfa.ChStates.StateConcat, n2.Start)

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

	nfa.FinalStates[n1.End.Name] = false
	nfa.FinalStates[n2.End.Name] = false

	nfa.ChStates.NameOr = append(nfa.ChStates.NameOr, n1.End.Name, n2.End.Name)
	nfa.ChStates.StateOr = append(nfa.ChStates.StateOr, s3, s3)

	nfa.addNode(s0, s3)
}

func (nfa *NFA) handleStar() {
	var n1 NodeGraph
	nfa.states, n1 = nfa.states.Pop()

	s0 := nfa.createState()
	s1 := nfa.createState()

	s0.Epsilon = append(s0.Epsilon, n1.Start, s1)

	n1.End.IsEnd = false
	nfa.FinalStates[n1.End.Name] = false

	nfa.ChStates.NameStar = append(nfa.ChStates.NameStar, n1.End.Name)
	nfa.ChStates.StateStar = append(nfa.ChStates.StateStar, s1, n1.Start)

	nfa.addNode(s0, s1)
}

// Helper functions fot handlers
func (nfa *NFA) addNode(start State, end State) {
	newNode := NodeGraph{Start: start, End: end, IsEnd: true}

	nfa.FinalStates[end.Name] = true
	nfa.states = nfa.states.Push(newNode)
}

func (nfa *NFA) initAlphabet(charSet map[string]bool) {
	for key, value := range charSet {
		if value == true {
			nfa.Alphabet = append(nfa.Alphabet, key)
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

func (nfa *NFA) Output() {
	var stateArr []State
	stateArr = append(stateArr, nfa.StartState.Start)

	for i := 0; i < len(stateArr); i++ {
		curState := stateArr[i]

		idx := IdxInStringArray(curState.Name, nfa.ChStates.NameConcat)
		if idx >= 0 {
			curState.Epsilon = nfa.ChStates.StateConcat[idx].Epsilon
			curState.Transitions = nfa.ChStates.StateConcat[idx].Transitions
		}

		idx = IdxInStringArray(curState.Name, nfa.ChStates.NameOr)
		if idx >= 0 {
			curState.Epsilon = append(curState.Epsilon, nfa.ChStates.StateOr[idx])
		}

		idx = IdxInStringArray(curState.Name, nfa.ChStates.NameStar)
		if idx >= 0 {
			curState.Epsilon = append(curState.Epsilon, nfa.ChStates.StateStar[2*idx], nfa.ChStates.StateStar[2*idx+1])
		}

		fmt.Println(i, ") from:", curState.Name)
		fmt.Print("by epsilon to:")

		for i := 0; i < len(curState.Epsilon); i++ {
			epsState := curState.Epsilon[i]
			fmt.Print(epsState.Name + " ")

			idx := IdxInStateArray(epsState, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, epsState)
			}
		}

		fmt.Println()
		for key, value := range curState.Transitions {
			fmt.Println("by ", key, " to ", value.Name)

			idx := IdxInStateArray(value, stateArr)
			if idx < 0 {
				stateArr = append(stateArr, value)
			}
		}
	}
}
