import numpy
import talib

close = numpy.random.random(100)
upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
print(middle)