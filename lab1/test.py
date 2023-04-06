import sys
sys.path.append('./parser')
sys.path.append('./automations')

from parse import Parser 
from nfa import NFA
from dfa import DFA
from copy import deepcopy


def build(p):
    parser = Parser()
    tokens = parser.Parse(p)

    nfa = NFA()
    nfa.Build(tokens)

    dfa = DFA(nfa)
    dfa.Build()
    dfa_min = deepcopy(dfa)
    dfa_min.minimize()
    
    return nfa, dfa, dfa_min

def test():
    num_tests = 0
    test_array = [
        {'pattern': '(0|(1(01*(00)*0)*1)*)*',
         'string_array': [(['0', '00', '11', '000', '011', '110', '0000', '0011', '0110', '1001', '1100', '1111', '00000'], True),
                          (['01', '01010', '0111100111', '100', 'abas'], False)]
        },
        {'pattern': '(a(b|c))*c',
         'string_array': [(['abc', 'abababababc', 'acc', 'c'], True),
                          (['aaaa', 'baba', 'abb', 'ababababa', 'bbbbb'], False)]
        },
        {'pattern': '(ab|a)(bc|c)',
         'string_array': [(['abc', 'abbc', 'ac'], True),
                          (['acb', 'bc'], False)]
        },
        {'pattern': '(ab)c|abc',
         'string_array': [(['abc'], True),
                          (['ab', 'fda', 'bac'], False)]
        },
        {'pattern': '(a*)(a|aa)',
         'string_array': [(['a', 'aaa'], True),
                          (['b', 'baa'], False)]
        },
        {'pattern': '(a|b)c|a(b|c)',
         'string_array': [(['ab', 'bc', 'ac'], True),
                          (['accc', 'bca'], False)]
        },
        {'pattern': 'ab*bc',
         'string_array': [(['abbc', 'abbbbbc'], True),
                          (['aacc', 'ac'], False)]
        },
        {'pattern': '(a|ab)',
         'string_array': [(['ab', 'a'], True),
                          (['aa', 'b'], False)]
        },
        {'pattern': '(a|ab)(b*)',
         'string_array': [(['ab', 'abbbbbbb'], True),
                          (['baa', 'aaa'], False)]
        },
        {'pattern': '((a|ab)(c|bcd))(d*)',
         'string_array': [(['abcd', 'acd'], True),
                          (['aaaa', 'abba'], False)]
        },
        {'pattern': 'a',
         'string_array': [(['a'], True),
                          (['aaaa', 'ba'], False)]
        },
        {'pattern': 'a*',
         'string_array': [(['a', 'aaaaa', ''], True),
                          (['bbb', 'ba', 'abbb'], False)]
        },
        {'pattern': 'a|b',
         'string_array': [(['a', 'b'], True),
                          (['bbb', 'ab', 'abbb'], False)]
        },
        {'pattern': '(aaabbaaabb)*|b',
         'string_array': [(['aaabbaaabb', 'aaabbaaabbaaabbaaabb', 'b'], True),
                          (['ababa', 'aa', 'abbb'], False)]
        }
    ]
    
    error = False
    for test in test_array:
        nfa, dfa, dfa_min = build(test['pattern'])
        for pattern_test_array in test['string_array']:
            string_array = pattern_test_array[0]
            expected = pattern_test_array[1]
            for string in string_array:
                num_tests += 1
                res = dfa.model(string)
                if res != expected:
                    error = True
                    print('[Error dfa]', 'pattern = ', test['pattern'], '; string = ', string, '; res = ', res, '; expected = ', expected)
                res = nfa.model(string)
                if res != expected:
                    error = True
                    print('[Error nfa]', 'pattern = ', test['pattern'], '; string = ', string, '; res = ', res, '; expected = ', expected)
                res = dfa_min.model(string)
                if res != expected:
                    error = True
                    print('[Error dfa_min]', 'pattern = ', test['pattern'], '; string = ', string, '; res = ', res, '; expected = ', expected)
    
    if not error:
        print('Ran', num_tests, 'test for', len(test_array), 'patterns')
        print('All tests passed')

test()
