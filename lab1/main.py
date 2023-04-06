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
    print()

    #3. По ДКА построить наименьший КА
    dfa.minimization()
    dfa.Output()  
    print()

    #4. Моделировать минимальный КА для входной цепочки
    #terminalString = input()
    terminalString = "babb"
    result = dfa.model(terminalString)
    print("result: ", result)


if __name__ == "__main__":
    main()
