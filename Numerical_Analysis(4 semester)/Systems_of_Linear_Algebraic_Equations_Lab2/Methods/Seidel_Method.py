import numpy as np
from numpy.linalg import inv, norm


def seidel(a, b, eps=10e-9):
    n = a.shape[0]
    d = np.triu(np.tril(a))

    h, g = np.eye(n) - np.dot(inv(d), a), np.dot(inv(d), b)
    x0 = np.zeros(n)

    x, x_prev = np.zeros(n), x0

    for i in range(n):
        x[i] = sum(h[i, j] * x[j] for j in range(i)) + \
            sum(h[i, j] * x_prev[j] for j in range(i, n)) + g[i]

    iteration = 0
    while norm(x - x_prev) >= eps:
        iteration += 1

        x_prev = np.copy(x)

        for i in range(n):
            x[i] = sum(h[i, j] * x[j] for j in range(i)) + \
                sum(h[i, j] * x_prev[j] for j in range(i, n)) + g[i]
        # print(f'\n Iteration {iteration} :\n', f'\tx = {x}')
    print("Iteration= ", iteration)
    return x

