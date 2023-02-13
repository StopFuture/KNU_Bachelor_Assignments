import random
import sympy
from sympy import *


class Relaxation:
    def __init__(self, function=lambda x: x, lambda_=0.5, left_border=-1.0, right_border=1.0, accuracy=1e-8):

        self.lambda_ = lambda_
        self.function = function

        self.derivative = None
        self.calc_derivative(self.function)

        self.left_border = left_border
        self.right_border = right_border
        self.accuracy = accuracy

        self.x_0 = random.uniform(self.left_border, self.right_border)
        self.alpha = (self.lambda_ - 1) / abs(self.derivative(self.x_0)) if abs(self.derivative(self.x_0)) != 0 else 0
        # print(self.alpha)

        self.answer = None
        self.iteration = None

    def calc_derivative(self, function=lambda x: 0):
        x = symbols('x')
        self.derivative = lambdify(x, function(x).diff(x))

    def calculate(self):
        try:
            x_0 = random.uniform(self.left_border, self.right_border)
            x_1 = x_0 + self.alpha * self.function(x_0)
            iteration = 0

            while abs(x_1 - x_0) > self.accuracy:
                x_0 = x_1
                x_1 = x_0 + self.alpha * self.function(x_0)

                iteration += 1

            self.answer = x_0
            self.iteration = iteration

            return self.display()
        except:
            self.name()
            print("Undefined")
            print("--------------------------")
        return

    @staticmethod
    def name():
        print("Relaxation Method:")

    def display(self):
        print("Relaxation/Simple iteration:")
        print("Answer: ", self.answer)
        print("Iteration", self.iteration)
        print("--------------------------")
# relax = Relaxation(lambda x: 5 + x, 0.0001, -10, 2, 1e-8)
# relax.calculate()
