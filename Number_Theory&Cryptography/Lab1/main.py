import time


from ElGamal import ElGamal

from LegendreJacobi import legendre_symbol, jacobi_symbol
from Long.LongComparison import LongComparison
from Long.LongNumber import LongNumber





def time_execution(func, *args):
    start = time.time()
    print(func(*args))
    end = time.time()
    print("Time elapsed:", end - start)


a1 = LongNumber(31350503)
b1 = LongNumber(1)
m1 = LongNumber(32350500)

c1 = LongComparison(a1, b1, m1)
print(a1+b1)

