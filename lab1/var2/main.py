from parse import Parser 
from automata import NFA, DFA

def main():
    #inputString = input()
    inputString = "(a|b)*abb"

    parser = Parser()
    regularString = parser.Parse(inputString)

    #1. По регулярному выражению построить НКА
    nfa = NFA()
    nfa.Build(regularString)
    nfa.Output()

    #2. По НКА построить эквивалентный ДКА
    dfa = DFA()
    dfa.Build(nfa)
    dfa.Output()
        

if __name__ == "__main__":
    main()
