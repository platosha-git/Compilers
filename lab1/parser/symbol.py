dictionarySymbs = ['(', ')', '*', '|']
dictionaryDescs = ['LB', 'RB', 'STAR', 'OR']

class Symbol:
    def __init__(self, desc, value):
        self.desc = desc
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value

def IdxInDictionary(char):
    for idx in range(len(dictionarySymbs)):
        if char == dictionarySymbs[idx]:
            return idx
    return -1