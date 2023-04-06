package base

type State struct {
	Name        string
	Epsilon     []State
	Transitions map[string]State
	IsEnd       bool
	IsStart     bool
}

type ChangedStates struct {
	NameOr  []string
	StateOr []State

	NameStar  []string
	StateStar []State

	NameConcat  []string
	StateConcat []State
}

func IdxInStateArray(st State, stArr []State) int {
	idxToRemove := -1
	for i := 0; i < len(stArr); i++ {
		if stArr[i].Name == st.Name {
			idxToRemove = i
			break
		}
	}

	return idxToRemove
}

func IdxInStringArray(name string, nameArray []string) int {
	idxInArray := -1
	for i := 0; i < len(nameArray); i++ {
		if nameArray[i] == name {
			idxInArray = i
			break
		}
	}

	return idxInArray
}

func RemoveDuplicates(states []State) {
	for i := 0; i < len(states)-1; i++ {
		for j := i + 1; j < len(states); j++ {
			if states[i].Name == states[j].Name {
				states = append(states[:j], states[j+1:]...)
			}
		}
	}
}

