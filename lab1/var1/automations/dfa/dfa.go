package dfa

import (
	"fmt"
	. "lab1/automations/nfa"
	. "lab1/base"
	"strconv"
)

type DFA struct {
	startState []State
	stopState  NodeGraph

	chStates ChangedStates

	startStates map[string]bool
	alphabet    []string
}

func (dfa *DFA) Build(nfa NFA) {
	dfa.chStates = nfa.ChStates
	endStateSet := nfa.FinalStates

	startStateSet := make(map[string]bool)
	startStateSet[nfa.StartState.Start.Name] = true

	startState := nfa.StartState.Start
	dfa.alphabet = nfa.Alphabet

	var unionStateArray [][]State
	var newTransitionArray []map[string][]State
	indexStateArray := 0

	epsilonClosure := dfa.getEpsilonClosure(startState)
	unionStateArray = append(unionStateArray, epsilonClosure)

	for indexStateArray < 2 {
		var transition = make(map[string][]State)
		for i := range dfa.alphabet {
			char := dfa.alphabet[i]
			var trans []State
			transition[char] = trans
		}
		epsilonClosure = unionStateArray[indexStateArray]

		for i := 0; i < len(epsilonClosure); i++ {
			for key, value := range epsilonClosure[i].Transitions {
				fmt.Println("eps=", value)
				transition[key] = append(transition[key], value)
			}
		}

		for char, value := range transition {
			if len(value) == 0 {
				continue
			}

			var newState []State
			for i := 0; i < len(value); i++ {
				fmt.Println("val=", value[i])
				epsilonClosure = dfa.getEpsilonClosure(value[i])
				newState = append(newState, epsilonClosure...)
			}

			fmt.Println("NEW STATE")
			for k := 0; k < len(newState); k++ {
				fmt.Print(newState[k].Name)
			}
			fmt.Println()

			transition[char] = newState
			if !isInArray(newState, unionStateArray) {
				unionStateArray = append(unionStateArray, newState)
			}
		}

		newTransitionArray = append(newTransitionArray, transition)
		indexStateArray++
	}

	var resStateArray []State
	for i := 0; i < len(unionStateArray); i++ {
		name := "s" + strconv.Itoa(i)
		trans := make(map[string]State)
		newState := State{Name: name, Transitions: trans, IsEnd: false, IsStart: false}

		resStateArray = append(resStateArray, newState)
	}

	for i := 0; i < len(unionStateArray); i++ {
		if !isdisjoint(endStateSet, unionStateArray[i]) {
			resStateArray[i].IsEnd = true
		}

		if !isdisjoint(startStateSet, unionStateArray[i]) {
			resStateArray[i].IsStart = true
		}
	}

	for i := 0; i < len(newTransitionArray); i++ {
		for key, val := range newTransitionArray[i] {
			if len(val) == 0 {
				continue
			}

			indexOfState := getIndex(unionStateArray, val)
			resStateArray[i].Transitions[key] = resStateArray[indexOfState]
		}
	}

	for i := 0; i < len(resStateArray); i++ {
		if resStateArray[i].IsStart {
			dfa.startState = append(dfa.startState, resStateArray[i])
		}
	}
}

func getIndex(arr [][]State, elem []State) int {
	idx := -1

	//fmt.Println("ARR")
	//for i := 0; i < len(arr); i++ {
	//	for j := 0; j < len(arr[i]); j++ {
	//		fmt.Print(arr[i][j].Name)
	//	}
	//	fmt.Println()
	//}
	//
	//fmt.Println("ELEM")
	//for i := 0; i < len(elem); i++ {
	//	fmt.Print(elem[i].Name)
	//}
	//fmt.Println()
	//fmt.Println()

	for i := 0; i < len(arr); i++ {
		if len(arr[i]) != len(elem) {
			continue
		}

		exist := true
		for j := 0; j < len(elem) && exist; j++ {
			ok1 := IdxInStateArray(elem[j], arr[i])
			ok2 := IdxInStateArray(arr[i][j], elem)
			if ok1 < 0 || ok2 < 0 {
				exist = false
			}
		}

		if exist {
			idx = i
			break
		}
	}

	return idx
}

func isdisjoint(map1 map[string]bool, arr2 []State) bool {
	result := true

	for i := 0; i < len(arr2); i++ {
		curElem := arr2[i].Name
		if map1[curElem] == true {
			result = false
			break
		}
	}

	return result
}

func isInArray(state []State, stArr [][]State) bool {
	answer := false

	for i := 0; i < len(stArr); i++ {
		if len(state) != len(stArr[i]) {
			continue
		}

		for j := 0; j < len(state); j++ {
			idx := IdxInStateArray(state[j], stArr[i])
			if idx >= 0 {
				answer = true
				break
			}
		}
	}

	return answer
}

func (dfa *DFA) _getEpsilonClosureRecur(state State, epsilonClosure *[]State) {
	idx := IdxInStateArray(state, *epsilonClosure)
	if idx >= 0 {
		return
	}

	idx = IdxInStringArray(state.Name, dfa.chStates.NameConcat)
	if idx >= 0 {
		state.Epsilon = dfa.chStates.StateConcat[idx].Epsilon
		state.Transitions = dfa.chStates.StateConcat[idx].Transitions
	}

	idx = IdxInStringArray(state.Name, dfa.chStates.NameOr)
	if idx >= 0 {
		state.Epsilon = append(state.Epsilon, dfa.chStates.StateOr[idx])
	}

	idx = IdxInStringArray(state.Name, dfa.chStates.NameStar)
	if idx >= 0 {
		state.Epsilon = append(state.Epsilon, dfa.chStates.StateStar[2*idx], dfa.chStates.StateStar[2*idx+1])
	}

	*epsilonClosure = append(*epsilonClosure, state)
	for i := range state.Epsilon {
		dfa._getEpsilonClosureRecur(state.Epsilon[i], epsilonClosure)
	}
}

func (dfa *DFA) getEpsilonClosure(state State) []State {
	var epsilonClosure []State
	dfa._getEpsilonClosureRecur(state, &epsilonClosure)
	return epsilonClosure
}

func (dfa *DFA) Output() {

	curStates := dfa.startState

	var usedStates []State
	for len(curStates) > 0 {
		var nextStates []State
		for i := 0; i < len(curStates); i++ {
			usedStates = append(usedStates, curStates[i])
			fmt.Print(curStates[i].Name, " -> ")

			for key, val := range curStates[i].Transitions {
				fmt.Print(key, ": ", val.Name, " ")
				idx := IdxInStateArray(val, usedStates)
				if idx < 0 {
					nextStates = append(nextStates, val)
				}
			}
			fmt.Println()
		}
		curStates = nextStates
	}
}
