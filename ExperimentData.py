import re
from functools import reduce

class ExperimentData():

    def __init__(self, data = None):
        self.data = data if (data) else self.dataInput()

    def dataInput(self):
        text    = input('Please input data: ')
        pattern = '[^ ]+'
        data    = re.findall(pattern, text)
        return list(map(float, data))
    
    def avg(self):
        return reduce(lambda x, y: x + y, self.data) / len(self.data)
    
    def sd(self):  # standard devisions
        data = self.data.copy()
        n    = len(data)
        data.insert(0, 0)
        return (reduce(lambda x, y: x + (y - self.avg()) ** 2, data) / (n - 1)) ** 0.5
    
    def filt(self, g0):
        n = len(self.data)
        s = self.sd()
        return list(filter(lambda x:x if ((x - self.avg()) / s) < g0 else None, self.data))
    
    def ua(self):
        return self.sd() / len(self.data) ** 0.5
    
    def ub(self, delta):
        return delta / 3 ** 0.5
    
    def u(self, delta):
        return (self.ua() ** 2 + self.ub(delta) ** 2) ** 0.5
