from ExperimentData import ExperimentData
from ExperimentCalc import *

# data  = ExperimentData()
# g0    = float(input('Input g0: '))
# delta = float(input('Input delta: '))
# data.data = data.filt(g0)
# print('xavg: ', data.avg().data)
# print('sd: ', data.sd().data)
# print('u: ', data.u(delta).data)
# print('ua: ', data.ua().data)
# print('ub: ', data.ub(delta))

dataX = ExperimentData()
dataY = ExperimentData()
res = ExperimentData.primaryReg(dataX, dataY)
print('a: ', res['a'])
print('b: ', res['b'])
