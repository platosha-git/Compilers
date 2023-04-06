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
        union_state_array = []
        new_transition_array = []
        index_state_array = 0

        epsilon_closure = list(self.get_epsilon_closure(self.startState))
        union_state_array.append(set(epsilon_closure))

        while index_state_array < len(union_state_array):
            transition = {char: [] for char in self.alphabet}
            epsilon_closure = list(union_state_array[index_state_array])

            for i in range(len(epsilon_closure)): # переходы по символам алфавита в эпсилон окрестности
                for char, value in epsilon_closure[i].transitions.items():
                    transition[char].append(value)
            for char, value in transition.items(): # добавление новых состояний в таблицу
                if len(value) == 0:
                    continue
                
                new_state = []
                for i in range(len(value)):
                    epsilon_closure = list(self.get_epsilon_closure(value[i]))
                    new_state.extend(epsilon_closure)

                transition[char] = new_state
                if set(new_state) not in union_state_array:
                    union_state_array.append(set(new_state))


            new_transition_array.append(transition)
            index_state_array += 1
        
        res_state_array = [State('s' + str(i)) for i in range(len(union_state_array))]
        
        for i in range(len(union_state_array)):
            if not self.finalStates.isdisjoint(union_state_array[i]): # имеют пересечение
                res_state_array[i].isEnd = True

            if not self.startStates.isdisjoint(union_state_array[i]): # имеют пересечение
                res_state_array[i].isStart = True

        for i in range(len(new_transition_array)):
            for char, union_state in new_transition_array[i].items():
                if len(union_state) == 0:
                    continue
                index_of_state = union_state_array.index(set(union_state))
                res_state_array[i].transitions[char] = res_state_array[index_of_state]
                
        for i in range(len(res_state_array)):
            if res_state_array[i].isStart:
                self.startStatesSet.add(res_state_array[i])


    def Output(self):
        current_states = self.startStatesSet
        used_states = set()
        while current_states != set():
            next_states = set()
            for state in current_states:
                used_states.add(state)
                print(state, end = '-> ')
                for key, value in state.transitions.items():
                    print(key, end = ': ')
                    print(value, end = ' ')
                    if value not in used_states:
                        next_states.add(value)
                print()
            current_states = next_states

    def _get_epsilon_closure_recur(self, state, epsilon_closure):
        if state in epsilon_closure:
                return
        epsilon_closure.add(state)
        for eps in state.epsilon:
            self._get_epsilon_closure_recur(eps, epsilon_closure)

    def get_epsilon_closure(self, state):
        epsilon_closure = set()
        self._get_epsilon_closure_recur(state, epsilon_closure)
        return epsilon_closure



    def _get_inv(self):
        inv = {}

        current_states = self.startStatesSet
        used_states = set()
        while current_states != set():
            next_states = set()
            for state in current_states:
                used_states.add(state)
                for c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    
                    if trans_state not in inv:
                        inv[trans_state] = {char: [] for char in self.alphabet}
                    inv[trans_state][c].append(state)
                    if trans_state not in used_states:
                        next_states.add(trans_state)
            current_states = next_states

        return inv, list(used_states)

    def minimization(self):
        if not self.startStatesSet:
            print('Build before please')
            return

        inv, used_states = self._get_inv()

        f = set(); not_f = set()
        for state in used_states:
            if state.isEnd:
                f.add(state)
            else:
                not_f.add(state)
        p = [f, not_f]
        queue = []
        class_ = {}
        for i in range(len(p)):
            for char in self.alphabet:
                queue.append([i, char])
            for state in p[i]:
                class_[state] = i
        while len(queue) > 0:
            c, a = queue.pop()
            involved = {}
            for q in p[c]:
                if q not in inv:
                    continue
                for r in inv[q][a]:
                    i = class_[r]
                    if i not in involved:
                        involved[i] = set()
                    involved[i].add(r)
            
            for i in involved:
                if len(list(involved[i])) < len(list(p[i])):
                    p.append(set())
                    j = len(p) - 1
                    for r in involved[i]:
                        p[i].remove(r)
                        p[j].add(r)
                    if len(list(p[j])) > len(list(p[i])):
                        p[j], p[i] = p[i], p[j]

                    for r in p[j]:
                        class_[r] = j

                    for char in self.alphabet:
                        queue.append([j, char])
    
        for i in range(len(p)):
            similar_state_arr = list(p[i])
            if len(similar_state_arr) <= 1:
                continue

            keep_state = similar_state_arr[0]
            for q in similar_state_arr:
                if q.isStart and q.isEnd:
                    keep_state = q
                    break

                if q.isStart or q.isEnd:
                    keep_state = q    

            for q in similar_state_arr:
                if q == keep_state:
                    continue            
                for char in inv[q]:
                    for st in inv[q][char]:
                        st.transitions[char] = keep_state
 

    def match(self,s):
        if not self.startStatesSet:
            print('Build before please')
            return
        
        current_states = self.startStatesSet
        for c in s:
            next_states = set()
            for state in current_states:
                if c in state.transitions.keys():
                    trans_state = state.transitions[c]
                    next_states.add(trans_state)
           
            current_states = next_states

        for s in current_states:
            if s.isEnd:
                return True
        return False
