from sympy import *


class Newton:

    def __init__(self, function=lambda x: x, x_0=0.0, left_border=-1.0, right_border=1.0, accuracy=1e-8):
        self.function = function
        self.derivative = None

        self.x_0 = x_0
        self.left_border = left_border
        self.right_border = right_border
        self.accuracy = accuracy

        self.answer = None
        self.iteration = None

    def calc_derivative(self, function=lambda x: 0):
        x = symbols('x')
        self.derivative = lambdify(x, function(x).diff(x))

    def calculate(self):
        try:
            self.calc_derivative(self.function)

            delta = self.function(self.x_0) / self.derivative(self.x_0)

            iteration = 0
            while delta >= self.accuracy:

                delta = self.function(self.x_0) / self.derivative(self.x_0)
                self.x_0 = self.x_0 - delta

                iteration += 1

            self.iteration = iteration
            self.answer = self.x_0
            if self.answer > self.right_border or self.answer < self.left_border:
                self.name()
                print(f"Answer doesn't belong to the [{self.left_border}, {self.right_border}], but founded.")
                self.display()
            else:
                self.name()
                self.display()
        except:
            self.name()
            print("Undefined")
            print("--------------------------")
        return

    @staticmethod
    def name():
        print("Newton Method:")

    def display(self):
        print("Answer: ", self.answer)
        print("Iteration", self.iteration)
        print("--------------------------")

# newton = Newton(lambda x: 5*x, 1000, -1, 0.5, 1e-8)
# newton.calculate()

