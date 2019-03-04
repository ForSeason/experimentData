from ExperimentData import ExperimentData

data  = ExperimentData()
g0    = float(input('Input g0: '))
delta = float(input('Input delta: '))
data.data = data.filt(g0)
print('xavg: ', data.avg())
print('u: ', data.u(delta))
