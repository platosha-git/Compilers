package parser

var dictionarySymbs = []rune{'(', ')', '*', '|'}
var dictionaryNames = []string{"LP", "RP", "STAR", "OR"}

func idxInDictionary(str rune) int {
	for idx, element := range dictionarySymbs {
		if str == element {
			return idx
		}
	}
	return -1
}

type Symbol struct {
	name  string
	value rune
}

type Parser struct {
	symbols        []Symbol
	origSymbols    []Symbol
	origSymbolsIdx int
}

func (parser *Parser) parse(regular []rune) []Symbol {
	if len(regular) < 1 {
		return nil
	}

	parser.createSymbols(regular)
	return parser.symbols
}

func (parser *Parser) createSymbols(regular []rune) []rune {
	for i := 0; i < len(regular); i++ {
		curSymb := regular[i]

		var token Symbol
		idx := idxInDictionary(curSymb)

		if idx < 0 {
			token = Symbol{name: "CHAR", value: curSymb}
		} else {
			name := dictionaryNames[idx]
			token = Symbol{name: name, value: curSymb}
		}

		append(parser.origSymbols, token)
		parser.origSymbolsIdx++
	}
}
