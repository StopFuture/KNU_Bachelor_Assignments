class Dichotomy:
    def __init__(self, function=lambda x: x, left_border=-1, right_border=1, accuracy=1e-8):
        self.function = function
        self.left_border = left_border
        self.right_border = right_border
        self.accuracy = accuracy
        self.answer = None
        self.iteration = None

    def calculate(self):
        right = self.right_border
        left = self.left_border
        accuracy = self.accuracy
        function = self.function
        iteration = 0

        while right - left > accuracy:
            mid = (right + left) / 2
            if function(right) * function(mid) <= 0:
                left = mid
            else:
                right = mid

            iteration += 1
        self.answer = (left + right) / 2
        self.iteration = iteration

        return self.display()

    def display(self):
        print("Dichotomy:")
        print("Answer: ", self.answer)
        print("Iteration", self.iteration)
        print("--------------------------")

# dichotomy = Dichotomy(lambda x: 6*x + 1, -100, 100, 1e-8)
# dichotomy.calculate()

