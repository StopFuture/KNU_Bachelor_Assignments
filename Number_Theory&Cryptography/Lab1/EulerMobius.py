from Long.LongNumber import LongNumber
from RhoPollard import pollard_rho
import streamlit as st
zero = LongNumber('0')
one = LongNumber('1')


@st.cache_data
def euler_phi_function(n):
    n = LongNumber(n)
    factors = pollard_rho(n)
    factor_powers: dict[LongNumber, LongNumber] = {}
    for factor in factors:
        factor_power = factor_powers.get(factor, LongNumber('0'))
        factor_powers.update({factor: factor_power + one})

    result = LongNumber('1')
    for factor, power in factor_powers.items():
        result *= (factor ** (power - one)) * (factor - one)
    return result


@st.cache_data
def mobius_mu_function(n):
    n = LongNumber(n)
    factors = pollard_rho(n)
    factor_powers: dict[LongNumber, int] = {}
    for factor in factors:
        factor_power = factor_powers.get(factor, 0)
        if factor_power > 0:
            return LongNumber(0)
        factor_powers.update({factor: factor_power + 1})
    return LongNumber(-1)**LongNumber(len(factors))
