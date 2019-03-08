import re
from functools import reduce
from decimal import *

def float2int(num):
    text    = str(num).replace('.', '')
    pattern = '^0*[1-9]\d*'
    return int(re.findall(pattern , text)[0]) if (re.match(pattern, text)) else 0

def sgnDigit(num):
    text     = str(num)
    pattern  = '^0*([1-9]\d*)\.?(\d*)'
    pattern2 = '^(0)\.0*([1-9]\d*)'
    if re.match(pattern, text):
        return reduce(lambda x, y: len(x) + len(y), re.findall(pattern , text)[0])
    elif re.match(pattern2, text):
        return len(re.findall(pattern2 , text)[0][1])
    else:
        return 1

class expDec():

    def __init__(self, data, exp = 1):
        getcontext().prec = 20
        self.exp  = exp
        self.data = Decimal(str(data))

    def __str__(self):
        return str(self.data)

    def __add__(self, other):
        other = other if (isinstance(other, expDec)) else expDec(other, 0)
        if self.data == 0 or other.data == 0:
            return expDec(self.data + other.data)
        else:
            if self.exp and other.exp:
                qS = len(re.findall('\.\d+$', str(self.data))[0]) if (re.findall('\.\d+$', str(self.data))) else 0
                qO = len(re.findall('\.\d+$', str(other.data))[0]) if (re.findall('\.\d+$', str(other.data))) else 0
                return expDec((self.data + other.data).quantize(self.data if (qS < qO) else other.data))
            elif self.exp:
                return expDec((self.data + other.data).quantize(self.data))
            elif other.exp:
                return expDec((self.data + other.data).quantize(other.data))
            else:
                return expDec(self.data + other.data, 0)


    def __sub__(self, other):
        other = other if (isinstance(other, expDec)) else expDec(other, 0)
        if self.data == 0 or other.data == 0:
            return expDec(self.data + other.data)
        else:
            if self.exp and other.exp:
                qS = len(re.findall('\.\d+', str(self.data))[0]) if (re.findall('\.\d+', str(self.data))) else 0
                qO = len(re.findall('\.\d+', str(other.data))[0]) if (re.findall('\.\d+', str(other.data))) else 0
                return expDec((self.data - other.data).quantize(self.data if (qS < qO) else other.data))
            elif self.exp:
                return expDec((self.data - other.data).quantize(self.data))
            elif other.exp:
                return expDec((self.data - other.data).quantize(other.data))
            else:
                return expDec(self.data - other.data, 0)

    def __mul__(self, other):
        other = other if (isinstance(other, expDec)) else expDec(other, 0)
        zerofixer = Decimal('1.000000000000000000000000000000000000000')
        if self.exp and other.exp:
            sgn = min(sgnDigit(self.data), sgnDigit(other.data))
            getcontext().prec = sgn + 1
            self.data = self.data * 1
            other.data = other.data * 1
            if int(str(self.data)[0]) * int(str(other.data)[0]) >= 10:
                getcontext().prec = sgn + 1
            else:
                getcontext().prec = sgn
            res = self.data * other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        elif self.exp:
            sgn = sgnDigit(self.data)
            getcontext().prec = sgn
            res = self.data * other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        elif other.exp:
            sgn = sgnDigit(other.data)
            getcontext().prec = sgn
            res = self.data * other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        else:
            return expDec(self.data * other.data, 0)

    def __truediv__(self, other):
        other      = other if (isinstance(other, expDec)) else expDec(other, 0)
        zerofixer  = Decimal('1.000000000000000000000000000000000000000')
        if self.exp and other.exp:
            sgn     = min(sgnDigit(self.data), sgnDigit(other.data))
            getcontext().prec = sgn + 1
            self.data  = self.data * 1
            other.data = other.data * 1
            pattern = '^0*[1-9]\d*\.?\d*$'
            check   = (float2int(self.data) % float2int(other.data) == 0) and (not re.findall(pattern , str(self.data))) and (not re.findall(pattern , str(other.data)))
            getcontext().prec = ((sgn - 1) if (sgn > 1) else 1) if (check) else sgn
            res     = self.data / other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        elif self.exp:
            sgn = sgnDigit(self.data)
            getcontext().prec = sgn
            res = self.data / other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        elif other.exp:
            sgn = sgnDigit(other.data)
            getcontext().prec = sgn
            res = self.data / other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        else:
            return expDec(self.data / other.data, 0)

    def __pow__(self, other):
        other = other if (isinstance(other, expDec)) else expDec(other, 0)
        zerofixer  = Decimal('1.000000000000000000000000000000000000000')
        if self.exp:
            sgn = sgnDigit(self.data)
            getcontext().prec = sgn
            res = self.data ** other.data * zerofixer
            getcontext().prec = 20
            return expDec(res)
        else:
            return expDec(self.data ** other.data, 0)
