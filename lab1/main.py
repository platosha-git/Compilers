import sys
sys.path.append('./parser')
sys.path.append('./automations')

from parse import Parser 
from nfa import NFA
from dfa import DFA

def main():
    #inputString = input("Enter regular string: ")
    inputString = "(a|b)*abb"

    parser = Parser()
    regularString = parser.Parse(inputString)

    #1. По регулярному выражению построить НКА
    nfa = NFA()
    nfa.Build(regularString)
    nfa.OutputGraph('1')

    #2. По НКА построить эквивалентный ДКА
    dfa = DFA(nfa)
    dfa.Build()
    dfa.OutputGraph('2')

    #3. По ДКА построить наименьший КА
    dfa.minimize()
    dfa.OutputGraph('3')  

    #4. Моделировать минимальный КА для входной цепочки
    terminalString = input("Enter terminal string: ")
    #terminalString = "babb"
    result = dfa.model(terminalString)
    print("Result: ", result)


if __name__ == "__main__":
    main()
