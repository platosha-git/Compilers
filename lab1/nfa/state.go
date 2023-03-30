package nfa

type state struct {
	epsilon     []state
	transitions map[string]state
	name        string
	isEnd       bool
	isStart     bool
}
