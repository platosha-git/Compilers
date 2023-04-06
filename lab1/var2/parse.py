from symbol import Symbol

class ParseError(Exception):pass

class Parser:
    def __init__(self):
        self.descSymbols = []
        self.descSymbolsIdx = 0

        self.regSymbols = []
        self.symbols_dict = {'(':'LB', ')':'RB', '*':'STAR', '|':'OR'}

    
    def Parse(self, string):
        if len(string) < 0:
            return []

        self.describeSymbols(string)
        self.handleSymbols()
        
        return self.regSymbols

    def describeSymbols(self, pattern):
        for c in pattern:
            if c not in self.symbols_dict.keys(): # CHAR
                token = Symbol('CHAR', c)
            else:
                token = Symbol(self.symbols_dict[c], c)
            self.descSymbols.append(token)

        self.lookahead = self.descSymbols[self.descSymbolsIdx]
        self.descSymbolsIdx += 1
        
        

    
    def handleSymbols(self):
        self.handle_concat()
        if self.lookahead.name == 'OR':
            t = self.lookahead
            self.check_and_next('OR')
            self.handleSymbols()
            self.regSymbols.append(t)

    def handle_concat(self):
        self.handle_star()
        if self.lookahead.value not in ')|':
            self.handle_concat()
            self.regSymbols.append(Symbol('CONCAT', 'CONCAT'))
    
    def handle_star(self):
        self.handle_char()
        if self.lookahead.name == 'STAR':
            self.regSymbols.append(self.lookahead)
            self.check_and_next(self.lookahead.name)

    def handle_char(self):
        if self.lookahead.name == 'LB':
            self.check_and_next('LB')
            self.handleSymbols()
            self.check_and_next('RB')
        elif self.lookahead.name == 'CHAR':
            self.regSymbols.append(self.lookahead)
            self.check_and_next('CHAR')

    def check_and_next(self, name):
        if self.lookahead.name == name:
            if self.descSymbolsIdx >= len(self.orig_symbols):
                self.lookahead = Symbol('NONE', '')
            else:
                self.lookahead = self.descSymbols[self.descSymbolsIdx]
            self.descSymbolsIdx += 1

        elif self.lookahead.name != name:
            raise ParseError
