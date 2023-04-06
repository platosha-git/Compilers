from state import State
from graph import NodeGraph

class NFA:
    def __init__(self):
        self.states = []
        self.numberOfStates = 0
        
        self.startState = None
        self.finalStates = set()

        self.alphabet = []


    def Build(self, regular):
        charSet = set()

        for symb in regular:
            if symb.desc == 'CHAR':
                self.handleChar(symb)
                charSet.add(symb.value)
            elif symb.desc == 'CONCAT':
                self.handleConcat()
            elif symb.desc == 'OR':
                self.handleOr()
            elif symb.desc == 'STAR':
                self.handleStar()
                            
        self.alphabet = list(charSet)
        self.startState = self.states.pop()


    def handleChar(self, symbol):
        s0 = self.createState()
        s1 = self.createState()

        s0.transitions[symbol.value] = s1

        self.addNode(s0, s1)


    def handleConcat(self):
        n2 = self.states.pop()
        n1 = self.states.pop()

        n1.end.isEnd = False
        if n1.end in self.finalStates:
            self.finalStates.remove(n1.end)

        n1.end.epsilon = n2.start.epsilon
        n1.end.transitions = n2.start.transitions 

        self.addNode(n1.start, n2.end)


    def handleOr(self):
        n2 = self.states.pop()
        n1 = self.states.pop()

        s0 = self.createState()
        s1 = self.createState()

        s0.epsilon = [n1.start, n2.start]
        
        n1.end.epsilon.append(s1)
        n2.end.epsilon.append(s1)

        n1.end.isEnd = False
        n2.end.isEnd = False
        
        if n1.end in self.finalStates:
            self.finalStates.remove(n1.end)
        if n2.end in self.finalStates:
            self.finalStates.remove(n2.end)

        self.addNode(s0, s1)


    def handleStar(self):
        n1 = self.states.pop()

        s0 = self.createState()
        s1 = self.createState()
        
        s0.epsilon = [n1.start]
        s0.epsilon.append(s1)
        
        n1.end.epsilon.extend([s1, n1.start])
        n1.end.isEnd = False
        
        if n1.end in self.finalStates:
            self.finalStates.remove(n1.end)

        self.addNode(s0, s1)


# Helper functions fot handlers
    def addNode(self, start, end):
        newNode = NodeGraph(start, end)
        
        self.finalStates.add(end)
        self.states.append(newNode)


    def createState(self):
        self.numberOfStates += 1
        return State('s' + str(self.numberOfStates))


    def Output(self):
        ind = 0
        state_array = []
        state_array.append(self.startState.start)
        while ind < len(state_array):
            current_state = state_array[ind]
            print(ind, ')', 'from:', current_state)
            print('by epsilon to:', end=' ')
            for eps_state in current_state.epsilon:
                print(eps_state, end=' ')
                if eps_state not in state_array:
                    state_array.append(eps_state)
                    
            print()
            for char, state in current_state.transitions.items():
                print('by', char, 'to', state, end = ' ')
                if state not in state_array:
                    state_array.append(state)
            
            print()

            ind += 1






    def addstate(self, state, state_set): 
        if state in state_set:
            return
        state_set.add(state)
        for eps in state.epsilon:
            self.addstate(eps, state_set)

    def match(self,s):
        if not self.startState:
            print('Build before please')
            return
        
        current_states = set()
        self.addstate(self.startState.start, current_states)
        
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    self.addstate(trans_state, next_states)
           
            current_states = next_states

        for s in current_states:
            if s.isEnd:
                return True
        return False

