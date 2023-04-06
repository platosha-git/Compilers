class State:
    def __init__(self, name):
        self.name = name
        self.epsilon = [] 
        self.transitions = {} 
        
        self.isEnd = False
        self.isStart = False

    def __str__(self):
        return self.name 