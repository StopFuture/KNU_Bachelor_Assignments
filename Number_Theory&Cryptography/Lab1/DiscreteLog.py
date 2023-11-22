import copy

from Long.LongNumber import LongNumber

two = LongNumber(2)
one = LongNumber(1)
zero = LongNumber(0)

def bsgs_log(a, g, mod):
    # solving for a^res = g % mod
    a = LongNumber(a)
    g = LongNumber(g)
    mod = LongNumber(mod)
    a %= mod
    g %= mod
    m = LongNumber.sqrt(mod) + one

    a_pow_m = LongNumber.pow_mod(a, m, mod)
    gamma = copy.deepcopy(a_pow_m)
    l1 = {one: a_pow_m}

    i = LongNumber(2)
    while i <= m:
        gamma = LongNumber.mult_mod(gamma, a_pow_m, mod)
        l1.update({i: copy.deepcopy(gamma)})
        i += one


    j = copy.deepcopy(one)
    while j <= m - one:
        tmp = LongNumber.mult_mod(g, LongNumber.pow_mod(a, j, mod), mod)
        for key, value in l1.items():
            if value == tmp:
                return (m * key - j) % mod
        j += one

    return None

def verify(g, h, p, x):
    """
    Verifies a given set of g, h, p and x
    :param g: Generator
    :param h:
    :param p: Prime
    :param x: Computed X
    :return:
    """
    h = LongNumber(h)
    g = LongNumber(g)
    p = LongNumber(p)
    x = LongNumber(x)
    return LongNumber.pow_mod(g, x, p) == h
