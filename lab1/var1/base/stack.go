package base

type Stack []NodeGraph

func (s Stack) Push(v NodeGraph) Stack {
	return append(s, v)
}

func (s Stack) Pop() (Stack, NodeGraph) {
	l := len(s)

	if l > 0 {
		return s[:l-1], s[l-1]
	}
	return s, s[0]
}
