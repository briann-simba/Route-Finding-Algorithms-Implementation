class Vertex():
    def __init__(self, v):
        self.inNeighbours = []
        self.outNeighbours = []
        self.value = v

    def hasOutNeighbour(self, v):
        return (v in self.outNeighbours)

    def hasInNeighbour(self, v):
        return (v in self.inNeighbours)

    def hasNeighbour(self, v):
        return self.hasOutNeighbour(v) or self.hasInNeighbour(v)

    def getOutNeighbours(self):
        return self.outNeighbours

    def getInNeighbours(self):
        return self.inNeighbours
    
    def getNeighbours(self):
        return self.outNeighbours + self.inNeighbours

    def addOutNeighbour(self, v):
        self.outNeighbours.append(v)

    def addInNeighbour(self, v):
        self.inNeighbours.append(v)

    def __str__(self):
        return str(self.value)

