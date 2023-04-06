class Symbol:
    def __init__(self, desc, value):
        self.desc = desc
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value