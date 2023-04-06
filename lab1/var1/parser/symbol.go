package parser

type Symbol struct {
	Desc  string
	Value string
}

var dictionarySymbs = []rune{'(', ')', '*', '|'}
var DictionaryDescs = []string{"LB", "RB", "STAR", "OR"}

func IdxInDictionary(str rune) int {
	for idx, element := range dictionarySymbs {
		if str == element {
			return idx
		}
	}
	return -1
}
