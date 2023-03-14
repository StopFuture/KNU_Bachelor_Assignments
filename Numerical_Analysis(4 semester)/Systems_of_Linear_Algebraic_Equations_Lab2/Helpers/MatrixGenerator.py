import numpy as np


class MatrixGenerator:
    def __init__(self):
        pass

    @staticmethod
    def generate_random_matrix(size, min_value=0, max_value=100):
        matrix = np.random.randint(min_value, high=max_value + 1, size=(size, size))
        return matrix

    @staticmethod
    def generate_gilbert_matrix(size):
        H = np.empty([size, size], dtype=float)
        for i in range(size):
            for j in range(size):
                H[i][j] = 1 / ((i + 1) + (j + 1) - 1)
        return H

    def generate_tridiagonal_matrix(self, size, min_value=0, max_value=100):
        matrix = self.generate_random_matrix(size, min_value, max_value)
        for i in range(size):
            for j in range(size):
                if abs(i - j) > 1:
                    matrix[i][j] = 0
        return matrix

    @staticmethod
    def generate_column_vector(matrix, solution):
        return np.dot(matrix, solution)

    def generate_diagonally_dominant_matrix(self, size, min_value=0, max_value=100):
        matrix = self.generate_random_matrix(size, min_value, max_value)
        for i in range(size):
            matrix[i][i] = sum(matrix[i]) - matrix[i][i] + 1

        return matrix


if __name__ == '__main__':
    mt = MatrixGenerator()
    print("Random Matrix")
    print(mt.generate_random_matrix(20, 0, 10))

    print("Gilbert Matrix")
    print(mt.generate_gilbert_matrix(20))

    print("Tridiagonal Matrix")
    print(mt.generate_diagonally_dominant_matrix(18, 0, 10))

'''
print(mt.generate_gilbert_matrix(3))

print(mt.generate_tridiagonal_matrix(5, 8, 101))

matrix1 = mt.generate_random_matrix(2, 5, 10)
x = np.random.randint(0, high=10, size=2)
b1 = mt.generate_column_vector(matrix1, x)
x = None

print(mt.generate_diagonally_dominant_matrix(3, 5, 10))
'''

