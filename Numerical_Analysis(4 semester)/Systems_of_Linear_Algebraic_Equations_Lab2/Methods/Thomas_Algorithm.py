import numpy as np


def thomas_tridiagonal(matrix, f):
    size = matrix.shape[0]

    c = -np.diag(matrix)
    a = np.diag(matrix, k=-1)
    b = np.diag(matrix, k=1)
    alpha_i = b[0] / c[0]

    beta_i = -f[0] / c[0]
    alpha = [alpha_i]
    beta = [beta_i]

    x = np.zeros(size)
    for i in range(1, size - 1):
        z_i = c[i] - alpha_i * a[i - 1]

        beta_i = (-f[i] + a[i - 1] * beta_i) / z_i
        beta.append(beta_i)

        alpha_i = b[i] / z_i
        alpha.append(alpha_i)

    z_i = c[-1] - alpha_i * a[-1]

    x[-1] = (-f[-1] + a[-1] * beta_i) / z_i
    for i in range(size - 2, -1, -1):
        x[i] = x[i + 1] * alpha[i] + beta[i]
    return x