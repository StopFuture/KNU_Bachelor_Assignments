import streamlit

from Long.LongNumber import LongNumber
from RhoPollard import pollard_rho
import copy

zero = LongNumber('0')
one = LongNumber('1')
two = LongNumber('2')
three = LongNumber('3')
six = LongNumber('6')
eight = LongNumber('8')
nine = LongNumber('9')
minus_one = LongNumber('-1')


def legendre_symbol(A, P):
    a = copy.deepcopy(A)
    p = copy.deepcopy(P)
    factors = []
    if a == one:
        return a
    if a == minus_one:
        return minus_one ** ((p - one) // two)
    if a < zero:
        factors.append(LongNumber('-1'))
        a = a * LongNumber('-1')
    a %= p
    factors += pollard_rho(a)
    factor_powers = {}
    for factor in factors:
        if factor_powers.get(factor):
            factor_powers[factor] += one
        else:
            factor_powers[factor] = LongNumber('1')


    odd_factor_powers = {}
    for key, value in factor_powers.items():
        if value % two != zero:
            odd_factor_powers[key] = value

    result = LongNumber('1')
    two_factor_amount = odd_factor_powers.get(two)
    if two_factor_amount:
        power_result = minus_one ** ((p ** two - one) // eight)
        i = LongNumber('0')
        while i < two_factor_amount:
            result *= power_result
            i += one
        odd_factor_powers.pop(two)

    for key, value in odd_factor_powers.items():
        assert value % two == one
        i = LongNumber('0')
        power_result = minus_one ** (((key - one) // two) * ((p - one) // two))
        legendre = legendre_symbol(p, key)
        while i < value:
            i += one
            result *= power_result * legendre

    return result

def cipolla(n, p):
    n = LongNumber(n)
    p = LongNumber(p)
    is_square = legendre_symbol(n, p) == one
    if is_square:
        selected_a = None
        a_squared_minus_n = None
        for a in range(2, 10):
            a_squared_minus_n = (LongNumber(a) * LongNumber(a) - n)
            while a_squared_minus_n < zero:
                a_squared_minus_n += p

            streamlit.write("A^2 - N", a_squared_minus_n)
            if legendre_symbol(a_squared_minus_n,n) == minus_one:
                selected_a = LongNumber(a)
                break
        streamlit.write("Selected A:", selected_a.__str__())
        streamlit.write("SQRT:", a_squared_minus_n.sqrt())

        u, v = selected_a, LongNumber(1)
        x, y = LongNumber(1), LongNumber(0)
        power = (p + one) // two
        while power > zero:
            if power % two == one:
                x, y = (x * u + y * v * a_squared_minus_n) % p, (x * v + y * u) % p
            u, v = (u * u + v * v * a_squared_minus_n) % p, two * u * v % p
            power //= two

        assert y == zero
        return x
    return None
