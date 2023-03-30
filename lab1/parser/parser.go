package parser

type Parser struct {
	symbols        []Symbol
	origSymbols    []Symbol
	origSymbolsIdx int
	headSymbol     Symbol
}

func (parser *Parser) Parse(regular []rune) []Symbol {
	if len(regular) < 1 {
		return nil
	}

	parser.createSymbols(regular)
	parser.handleSymbols()

	return parser.symbols
}

func (parser *Parser) createSymbols(regular []rune) {
	for i := 0; i < len(regular); i++ {
		curSymb := regular[i]

		var token Symbol
		idx := IdxInDictionary(curSymb)

		if idx < 0 {
			token = Symbol{Name: "CHAR", Value: string(curSymb)}
		} else {
			name := DictionaryNames[idx]
			token = Symbol{Name: name, Value: string(curSymb)}
		}

		parser.origSymbols = append(parser.origSymbols, token)
	}
	parser.headSymbol = parser.origSymbols[parser.origSymbolsIdx]
	parser.origSymbolsIdx++
}

func (parser *Parser) handleSymbols() {
	parser.handleConcat()
	if parser.headSymbol.Name == "OR" {
		t := parser.headSymbol
		parser.checkAndNext("OR")
		parser.handleSymbols()
		parser.symbols = append(parser.symbols, t)
	}
}

func (parser *Parser) handleConcat() {
	parser.handleStar()
	if parser.headSymbol.Value != ")" && parser.headSymbol.Value != "|" && parser.headSymbol.Value != "" {
		parser.handleConcat()
		parser.symbols = append(parser.symbols, Symbol{"CONCAT", "CONCAT"})
	}
}

func (parser *Parser) handleStar() {
	parser.handleChar()
	if parser.headSymbol.Name == "STAR" {
		parser.symbols = append(parser.symbols, parser.headSymbol)
		parser.checkAndNext(parser.headSymbol.Name)
	}
}

func (parser *Parser) handleChar() {
	if parser.headSymbol.Name == "LP" {
		parser.checkAndNext("LP")
		parser.handleSymbols()
		parser.checkAndNext("RP")
	} else if parser.headSymbol.Name == "CHAR" {
		parser.symbols = append(parser.symbols, parser.headSymbol)
		parser.checkAndNext("CHAR")
	}
}

func (parser *Parser) checkAndNext(name string) {
	if parser.headSymbol.Name == name {
		if parser.origSymbolsIdx >= len(parser.origSymbols) {
			parser.headSymbol = Symbol{"NONE", ""}
		} else {
			parser.headSymbol = parser.origSymbols[parser.origSymbolsIdx]
		}
		parser.origSymbolsIdx++
	}
}
