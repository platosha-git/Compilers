import sys
sys.path.append('./parser')
sys.path.append('./automations')

from parse import Parser 
from nfa import NFA
from dfa import DFA

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
    dfa = DFA(nfa)
    dfa.Build()
    dfa.Output()
        

if __name__ == "__main__":
    main()
