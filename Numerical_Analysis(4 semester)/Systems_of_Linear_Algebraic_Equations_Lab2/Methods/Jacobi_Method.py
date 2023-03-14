import numpy as np


def jacobi(matrix, column_vector, eps=10e-9):
    D = np.diag(matrix)
    D_inv = np.diag(1 / D)
    size = matrix.shape[0]
    A_sum = matrix - np.diag(D)
    x_prev = np.zeros((size, 1))
    x_k = (- np.dot(np.dot(D_inv, A_sum), x_prev) + np.dot(D_inv, column_vector))
    i = 0
    while np.linalg.norm(x_k - x_prev) > eps:
        i += 1
        x_prev = x_k
        x_k = (- np.dot(np.dot(D_inv, A_sum), x_k) + np.dot(D_inv, column_vector))
        # print(f'\n Iteration {i} :\n', f'\tx = {x_k}')
    return x_k.reshape(size)