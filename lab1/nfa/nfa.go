package nfa

type tempNFA struct {
	alphabet   []string
	stack      []string
	stateCount []string
}

type tran struct {
	state     set.IntSet
	symbol    byte
	destState set.IntSet
}

type state struct {
	value  set.IntSet
	marked bool
}
