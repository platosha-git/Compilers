from symbol import *

class Parser:
    def __init__(self):
        self.descSymbols = []
        self.descSymbolsIdx = 0

        self.regSymbols = []
        self.curSymbol = ''

    
    def Parse(self, string):
        if len(string) < 0:
            return []

        self.describeSymbols(string)
        self.handleSymbols()
        
        return self.regSymbols


    def describeSymbols(self, string):
        for char in string:
            idx = IdxInDictionary(char)

            if idx < 0:
                descSymbol = Symbol('CHAR', char)
            else:
                descSymbol = Symbol(dictionaryDescs[idx], char)
            
            self.descSymbols.append(descSymbol)

        self.curSymbol = self.descSymbols[self.descSymbolsIdx]
        self.descSymbolsIdx += 1
        
        
    def handleSymbols(self):
        self.handleBody()
        if self.curSymbol.desc == 'OR':
            self.handleOr()

    def handleBody(self):
        if self.curSymbol.desc == 'LB':
            self.handleBrackets()
        elif self.curSymbol.desc == 'CHAR':
            self.handleInnerPart('CHAR')
        if self.curSymbol.desc == 'STAR':
            self.handleInnerPart('STAR')
        if self.curSymbol.value not in ')|':
            self.handleExternalPart()

    def handleBrackets(self):
        self.nextSymbol("LB")
        self.handleSymbols()
        self.nextSymbol("RB")

    def handleInnerPart(self, desc):
        self.regSymbols.append(self.curSymbol)
        self.nextSymbol(desc)

    def handleExternalPart(self):
        self.handleBody()
        self.regSymbols.append(Symbol('CONCAT', 'CONCAT'))

    def handleOr(self):
        t = self.curSymbol
        self.nextSymbol('OR')
        self.handleSymbols()
        self.regSymbols.append(t)

    def nextSymbol(self, desc):
        if self.curSymbol.desc == desc:
            if self.descSymbolsIdx >= len(self.descSymbols):
                self.curSymbol = Symbol('NONE', '')
            else:
                self.curSymbol = self.descSymbols[self.descSymbolsIdx]
            self.descSymbolsIdx += 1
