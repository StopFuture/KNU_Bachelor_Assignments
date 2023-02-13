from Methods.Newton import *
from Methods.Dichotomy import *
from Methods.Relaxation import *

if __name__ == "__main__":
    # init
    function = lambda x: x**2 - 4
    lambda_ = 0.0001
    accuracy = 1e-8
    left_border = 0.5
    right_border = 5
    x_0 = 100

    # test
    dichotomy = Dichotomy(function, left_border, right_border, accuracy)
    dichotomy.calculate()

    newton = Newton(function, x_0, left_border, right_border, accuracy)
    newton.calculate()

    relax = Relaxation(function, lambda_, left_border, right_border, accuracy)
    relax.calculate()
