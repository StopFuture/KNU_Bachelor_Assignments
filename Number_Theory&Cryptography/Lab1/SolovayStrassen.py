import random

from LegendreJacobi import jacobi_symbol
from Long.LongNumber import LongNumber
import streamlit as st
zero = LongNumber('0')
one = LongNumber('1')
two = LongNumber('2')
three = LongNumber('3')
six = LongNumber('6')
eight = LongNumber('8')
nine = LongNumber('9')
minus_one = LongNumber('-1')
N = LongNumber('10')


def solovei_strassen(a):
    i = N
    while i > zero:
        k = LongNumber(random.randrange(int(a.__str__())))
        st.write("Random number: ", k.__str__())
        if LongNumber.GCD(a, k) > one:
            st.write("GCD isn't one")
            return False
        jacobi = jacobi_symbol(str(k), str(a))

        while jacobi < zero:
            jacobi += a

        if LongNumber.pow_mod(k, (a - one) // two, a) != jacobi % a:
            st.write("Mod comparison failed:", LongNumber.pow_mod(k, (a - one) // two, a), jacobi % a)
            return False
        i -= one
    return True
