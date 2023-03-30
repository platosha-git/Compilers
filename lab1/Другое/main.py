from parse import Parser 
from automata import NFA, DFA

def build(p):

    parser = Parser()
    tokens = parser.parse(p)
    
    if len(tokens) == 0:
        print('Empty regular expression')
        return None 

    nfa = NFA()
    for i in tokens:
        print(i)   
    nfa.build(tokens)
    
    nfa.print_graph()

    dfa = DFA()
    #dfa.convert_nfa_to_dfa(nfa)
    #dfa.minimization()
    
    return dfa

def main():
    # p = '(0|(1(01*(00)*0)*1)*)*'
    # p = '(a(b|c))*c'
    
    while True:
        p = input('Enter regular expression (or exit): ')
        if p == 'exit':
           break
        
        # p = '(a|b)*abb'

        dfa = build(p)
        #dfa.print_graph()
        break
    
        if dfa is None:
           continue

        s = ''
        while True:
            s = input('Enter string (or back): ')
            if s == 'back':
                break
            res_dfa = dfa.match(s)
            print('pattern = ', p, '; string = ', s, '; res = ', res_dfa)

main()

