package parser

type Parser struct {
	descSymbols    []Symbol
	descSymbolsIdx int

	regSymbols []Symbol
	curSymbol  Symbol
}

func (parser *Parser) Parse(regular []rune) []Symbol {
	if len(regular) < 1 {
		return nil
	}

	parser.describeSymbols(regular)
	parser.handleSymbols()

	return parser.regSymbols
}

func (parser *Parser) describeSymbols(regular []rune) {
	for _, char := range regular {
		idx := IdxInDictionary(char)

		var descSymbol Symbol
		if idx < 0 {
			descSymbol = Symbol{Desc: "CHAR", Value: string(char)}
		} else {
			desc := DictionaryDescs[idx]
			descSymbol = Symbol{Desc: desc, Value: string(char)}
		}

		parser.descSymbols = append(parser.descSymbols, descSymbol)
	}
	parser.curSymbol = parser.descSymbols[parser.descSymbolsIdx]
	parser.descSymbolsIdx++
}

func (parser *Parser) handleSymbols() {
	if parser.curSymbol.Desc == "LB" {
		parser.handleBrackets()
	} else if parser.curSymbol.Desc == "CHAR" {
		parser.handleInnerPart("CHAR")
	}
	if parser.curSymbol.Desc == "STAR" {
		parser.handleInnerPart("STAR")
	}
	if parser.curSymbol.Value != ")" && parser.curSymbol.Value != "|" && parser.curSymbol.Value != "" {
		parser.handleExternalPart()
	}
	if parser.curSymbol.Desc == "OR" {
		parser.handleOr()
	}
}

func (parser *Parser) handleBrackets() {
	parser.nextSymbol("LB")
	parser.handleSymbols()
	parser.nextSymbol("RB")
}

func (parser *Parser) handleInnerPart(desc string) {
	parser.regSymbols = append(parser.regSymbols, parser.curSymbol)
	parser.nextSymbol(desc)
}

func (parser *Parser) handleExternalPart() {
	parser.handleSymbols()
	parser.regSymbols = append(parser.regSymbols, Symbol{"CONCAT", "CONCAT"})
}

func (parser *Parser) handleOr() {
	t := parser.curSymbol
	parser.nextSymbol("OR")
	parser.handleSymbols()
	parser.regSymbols = append(parser.regSymbols, t)
}

func (parser *Parser) nextSymbol(description string) {
	if parser.curSymbol.Desc == description {
		if parser.descSymbolsIdx >= len(parser.descSymbols) {
			parser.curSymbol = Symbol{"NONE", ""}
		} else {
			parser.curSymbol = parser.descSymbols[parser.descSymbolsIdx]
		}
		parser.descSymbolsIdx++
	}
}
