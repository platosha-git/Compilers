package nfa

type stack []nodeGraph

func (s stack) Push(v nodeGraph) stack {
	return append(s, v)
}

func (s stack) Pop() (stack, nodeGraph) {
	l := len(s)

	if l > 0 {
		return s[:l-1], s[l-1]
	}
	return s, s[0]
}
