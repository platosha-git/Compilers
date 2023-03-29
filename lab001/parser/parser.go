package parser

import "fmt"

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
	value string
}

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
		idx := idxInDictionary(curSymb)

		if idx < 0 {
			token = Symbol{name: "CHAR", value: string(curSymb)}
		} else {
			name := dictionaryNames[idx]
			token = Symbol{name: name, value: string(curSymb)}
		}

		parser.origSymbols = append(parser.origSymbols, token)
	}
	parser.headSymbol = parser.origSymbols[parser.origSymbolsIdx]
	parser.origSymbolsIdx++
}

func (parser *Parser) handleSymbols() {
	parser.handleConcat()
	if parser.headSymbol.name == "OR" {
		t := parser.headSymbol
		parser.checkAndNext("OR")
		parser.handleSymbols()
		parser.symbols = append(parser.symbols, t)
	}
}

func (parser *Parser) handleConcat() {
	parser.handleStar()
	fmt.Println("IN CONCAT:", parser.headSymbol)
	if parser.headSymbol.value != ")" && parser.headSymbol.value != "|" && parser.headSymbol.value != "" {
		parser.handleConcat()
		parser.symbols = append(parser.symbols, Symbol{"CONCAT", "CONCAT"})
	}
}

func (parser *Parser) handleStar() {
	parser.handleChar()
	if parser.headSymbol.name == "STAR" {
		parser.symbols = append(parser.symbols, parser.headSymbol)
		parser.checkAndNext(parser.headSymbol.name)
	}
}

func (parser *Parser) handleChar() {
	if parser.headSymbol.name == "LP" {
		parser.checkAndNext("LP")
		parser.handleSymbols()
		parser.checkAndNext("RP")
	} else if parser.headSymbol.name == "CHAR" {
		fmt.Println("HERE1")
		parser.symbols = append(parser.symbols, parser.headSymbol)
		parser.checkAndNext("CHAR")
	}
}

func (parser *Parser) checkAndNext(name string) {
	if parser.headSymbol.name == name {
		fmt.Println("LEN = ", len(parser.origSymbols))
		if parser.origSymbolsIdx >= len(parser.origSymbols) {
			parser.headSymbol = Symbol{"NONE", ""}
		} else {
			parser.headSymbol = parser.origSymbols[parser.origSymbolsIdx]
			fmt.Println("IDX = ", parser.origSymbolsIdx)
			fmt.Println("ORIG SYMBS = ", parser.headSymbol)
		}
		parser.origSymbolsIdx++
	}
}
