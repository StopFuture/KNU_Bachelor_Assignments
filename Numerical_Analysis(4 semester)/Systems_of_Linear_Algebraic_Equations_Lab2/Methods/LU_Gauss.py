import scipy.linalg
import numpy as np


def LU_Gauss(matrix, column_vector):
    P, L, U = scipy.linalg.lu(matrix)
    L = np.dot(P, L)

    L_1 = np.linalg.inv(L)
    y = np.dot(L_1, column_vector)
    U_1 = np.linalg.inv(U)
    ans = np.dot(U_1, y)
    return ans


def Matrix_Gauss(matrix, column_vector):
    k = -1
    size = len(matrix)
    p = 0
    A_k = matrix.copy()
    b = column_vector.copy()
    while k != size - 1:
        k += 1
        max_ = np.argmax(np.abs(A_k[k:, k]), axis=0)
        if max_ == 0:
            p += 1
        P_kl = np.eye(size, dtype=int)
        P_kl[[k, max_ + k], :] = P_kl[[max_ + k, k], :]
        P_kl_A = np.dot(P_kl, A_k)
        M_k = np.eye(size, dtype=float)
        if P_kl_A[k, k] == 0 :
            break
        M_k[k, k] = 1 / P_kl_A[k, k]
        M_k[k+1:, k] = - P_kl_A[k+1:, k] / P_kl_A[k, k]
        A_k = np.dot(M_k, P_kl_A)
        b = np.dot(M_k, np.dot(P_kl, b))
    x = np.array([0.0 for _ in range(size)])
    for i in range(0, size)[::-1]:
        x[i] = b[i] - np.sum(A_k[i, i + 1:] * x[i + 1:])

    return x




