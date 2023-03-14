# Author: Fedorych Andrii K25
from Helpers.MatrixGenerator import MatrixGenerator
from Methods.Seidel_Method import *
from Methods.Jacobi_Method import *
from Methods.Thomas_Algorithm import *
from Methods.LU_Gauss import *

if __name__ == '__main__':
    print(f'Author: Fedorych Andrii K25')
    mg = MatrixGenerator()
    n = 5
    solution = np.array([[i] for i in range(n)])

    print("Gauss + Random:")
    A = mg.generate_random_matrix(n, 1, 5)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {Matrix_Gauss(A, b)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

    print("Gauss + Gilbert:")
    A = mg.generate_gilbert_matrix(n)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {Matrix_Gauss(A, b)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

    print("Tridiagonal | Thomas:")
    A = mg.generate_tridiagonal_matrix(n, 5, 10)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {thomas_tridiagonal(A, b)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

    print("Jacobi + Random:")
    A = mg.generate_diagonally_dominant_matrix(n, 5, 10)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {jacobi(A, b, 10e-5)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

    print("Seidel + Random:")

    A = mg.generate_diagonally_dominant_matrix(n, 5, 10)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {seidel(A, b, 10e-9)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

    print("Seidel + Gilbert:")

    A = mg.generate_gilbert_matrix(n)
    b = mg.generate_column_vector(A, solution)
    print(A)
    print(b)
    print(f"Solution: {seidel(A, b, 10e-5)}")
    print(f"Condition number: {np.linalg.cond(A)}")

    print("---------------------------------------------------------------------------------------------------------")

