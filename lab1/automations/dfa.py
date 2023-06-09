import os
from state import State
from graph import NodeGraph

class DFA:
    def __init__(self, nfa): 
        self.states = nfa.states
        self.numberOfStates = nfa.numberOfStates

        self.startState = nfa.startState.start
        self.startStatesSet = set()

        self.startStates = set([nfa.startState.start])
        self.finalStates = nfa.finalStates

        self.alphabet = nfa.alphabet


    def Build(self):
        epsilonClosure = list(self.defineClosure(self.startState))
        
        unionStates = []
        unionStates.append(set(epsilonClosure))

        idx = 0
        newTransitions = []

        while idx < len(unionStates):
            newTransition = {char: [] for char in self.alphabet}
            epsilonClosure = list(unionStates[idx])

            for i in range(len(epsilonClosure)):
                for char, value in epsilonClosure[i].transitions.items():
                    newTransition[char].append(value)

            for char, value in newTransition.items():
                if len(value) == 0:
                    continue
                
                newState = []
                for i in range(len(value)):
                    epsilonClosure = list(self.defineClosure(value[i]))
                    newState.extend(epsilonClosure)

                newTransition[char] = newState
                if set(newState) not in unionStates:
                    unionStates.append(set(newState))


            newTransitions.append(newTransition)
            idx += 1
        
        resStates = [State('s' + str(i)) for i in range(len(unionStates))]
        
        self.correctExtremeStates(unionStates, resStates)
        self.defineTransitions(newTransitions, unionStates, resStates)
        self.defineStartStates(resStates)


    def correctExtremeStates(self, unionStates, resStates):
        for i in range(len(unionStates)):
            if not self.finalStates.isdisjoint(unionStates[i]):
                resStates[i].isEnd = True

            if not self.startStates.isdisjoint(unionStates[i]):
                resStates[i].isStart = True


    def defineTransitions(self, newTransitions, unionStates, resStates):
        for i in range(len(newTransitions)):
            for char, union_state in newTransitions[i].items():
                if len(union_state) == 0:
                    continue
                index_of_state = unionStates.index(set(union_state))
                resStates[i].transitions[char] = resStates[index_of_state]


    def defineStartStates(self, resStates):
        for i in range(len(resStates)):
            if resStates[i].isStart:
                self.startStatesSet.add(resStates[i])


#Helper functions for build cycle
    def defineClosureRecur(self, state, epsilonClosure):
        if state in epsilonClosure:
                return
        epsilonClosure.add(state)
        for eps in state.epsilon:
            self.defineClosureRecur(eps, epsilonClosure)


    def defineClosure(self, state):
        epsilonClosure = set()
        self.defineClosureRecur(state, epsilonClosure)
        return epsilonClosure


    def OutputGraph(self, step):
        file = open(step + ".gv", "w")
        file.write("digraph G {\nrankdir = LR;\n")

        curStates = self.startStatesSet
        usedStates = set()
        while curStates != set():
            nextStates = set()
            
            for state in curStates:
                usedStates.add(state)
                for key, value in state.transitions.items():
                    transStr = '"' + str(state) + '"' + " -> " + '"' + str(value) + '"[label="' + str(key) + '"];\n'
                    file.write(transStr)
                    if value not in usedStates:
                        nextStates.add(value)
            curStates = nextStates

        file.write("}\n")
        file.close()

        os.system("dot -Tpng " + step + ".gv -o" + step + ".png")
        os.system("xdg-open " + step + ".png")


#Minimizations functions
    def minimize(self):
        inv, states = self.getStates()

        f, notF = self.firstReverse(states)
        
        rStates = [f, notF]
        queue, dStates = self.firstDetermine(rStates)
        
        self.secondReverse(rStates, inv, queue, dStates)
        self.secondDetermine(rStates, inv)

        
    def getStates(self):
        inv = {}

        current_states = self.startStatesSet
        usedStates = set()

        while current_states != set():
            next_states = set()

            for state in current_states:
                usedStates.add(state)
                
                for c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    
                    if trans_state not in inv:
                        inv[trans_state] = {char: [] for char in self.alphabet}
                    
                    inv[trans_state][c].append(state)
                    
                    if trans_state not in usedStates:
                        next_states.add(trans_state)
            
            current_states = next_states
        return inv, list(usedStates)


    def firstReverse(self, usedStates):
        f = set(); notF = set()
        for state in usedStates:
            if state.isEnd:
                f.add(state)
            else:
                notF.add(state)

        return f, notF


    def firstDetermine(self, rStates):
        queue = []
        dStates = {}

        for i in range(len(rStates)):
            for char in self.alphabet:
                queue.append([i, char])
            for state in rStates[i]:
                dStates[state] = i

        return queue, dStates


    def secondReverse(self, rStates, inv, queue, dStates):
        while len(queue) > 0:
            c, a = queue.pop()
            involved = {}

            for q in rStates[c]:
                if q not in inv:
                    continue
                for r in inv[q][a]:
                    i = dStates[r]
                    
                    if i not in involved:
                        involved[i] = set()
                    involved[i].add(r)
            
            for i in involved:
                if len(list(involved[i])) < len(list(rStates[i])):
                    rStates.append(set())
                    j = len(rStates) - 1
                    
                    for r in involved[i]:
                        rStates[i].remove(r)
                        rStates[j].add(r)
                    
                    if len(list(rStates[j])) > len(list(rStates[i])):
                        rStates[j], rStates[i] = rStates[i], rStates[j]

                    for r in rStates[j]:
                        dStates[r] = j

                    for char in self.alphabet:
                        queue.append([j, char])


    def secondDetermine(self, rStates, inv):
        for i in range(len(rStates)):
            similarStates = list(rStates[i])
            if len(similarStates) <= 1:
                continue

            keepState = similarStates[0]
            for q in similarStates:
                if q.isStart and q.isEnd:
                    keepState = q
                    break

                if q.isStart or q.isEnd:
                    keepState = q    

            for q in similarStates:
                if q == keepState:
                    continue            
                for char in inv[q]:
                    for st in inv[q][char]:
                        st.transitions[char] = keepState
 

#Functions for modeling by terminal string
    def model(self, string):
        curStates = self.startStatesSet
        
        for symbol in string:
            nextStates = set()

            for state in curStates:
                if symbol in state.transitions.keys():
                    nextStates.add(state.transitions[symbol])
           
            curStates = nextStates

        for state in curStates:
            if state.isEnd:
                return True
        return False
