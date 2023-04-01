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
