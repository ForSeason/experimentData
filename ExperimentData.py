import re
from functools import reduce
from ExperimentCalc import *

class ExperimentData():

    def __init__(self, data = None):
        self.data = data if (data) else self.dataInput()

    def dataInput(self):
        text    = input('Please input data: ')
        return list(map(expDec, text.split()))
    
    def avg(self):
        res = reduce(lambda x, y: x + y, [x / len(self.data) for x in self.data])
        return expDec(res.data.quantize(self.data[0].data))
    
    def sd(self):  # standard devisions
        # data = self.data.copy()
        # n    = len(data)
        # data.insert(0, expDec(0, 0))
        # return (reduce(lambda x, y: x + (y - self.avg()) ** 2, data) / (n - 1)) ** 0.5
        return (reduce(lambda x, y: x + y,[(x - self.avg()) ** 2 for x in self.data]) / (len(self.data) - 1)) ** 0.5
    
    def filt(self, g0):
        n = len(self.data)
        s = self.sd()
        return list(filter(lambda x:x if ((x - self.avg()) / s).data < g0 else None, self.data))
    
    def ua(self):
        return self.sd() / len(self.data) ** 0.5
    
    def ub(self, delta):
        return delta / 3 ** 0.5
    
    def u(self, delta):
        return (self.ua() ** 2 + self.ub(delta) ** 2) ** '0.5'

    def primaryReg(iData, dData):   #i for independent, d for dependent
        idData = ExperimentData(list(map(lambda x, y: x * y, iData.data, dData.data)))
        i2Data = ExperimentData(list(map(lambda x: x ** 2, iData.data)))
        d2Data = ExperimentData(list(map(lambda x: x ** 2, dData.data)))
        lxy = idData.avg() - iData.avg() * dData.avg()
        lxx = i2Data.avg() - iData.avg() ** 2
        lyy = d2Data.avg() - dData.avg() ** 2
        a = lxy / lxx
        b = dData.avg() - a * iData.avg()
        r = lxy / (lxx * lyy) ** 0.5
        return {'a': a, 'b': b, 'r': r}
