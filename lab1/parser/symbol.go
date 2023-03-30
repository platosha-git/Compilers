package parser

type Symbol struct {
	Name  string
	Value string
}

var dictionarySymbs = []rune{'(', ')', '*', '|'}
var DictionaryNames = []string{"LP", "RP", "STAR", "OR"}

func IdxInDictionary(str rune) int {
	for idx, element := range dictionarySymbs {
		if str == element {
			return idx
		}
	}
	return -1
}
