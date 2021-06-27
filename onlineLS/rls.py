import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#
(X, y, coef) = make_regression(n_samples=100,
                                 n_features=2,
                                 n_informative=2,
                                 n_targets=1,
                                 bias=10,
                                 noise=0,
                                 coef=True,
                                 random_state=42)

# X = np.random.normal(loc=0, scale=1, size=(100,2))
# theta_true = np.array([1,2]).reshape(2, -1)
# y =  0.5 * np.ones(shape=(100, 1)) + np.matmul(X, theta_true) + np.random.normal(loc=0, scale=0.01, size=(100,1))

# start RLS
q = 3
fit_intercept = True

theta = np.zeros(shape=(q, 1))
s = np.zeros(shape=(q, q, 1))
k = np.zeros(shape=(q, 1))

for i in range(len(X)):
    print(i)

    # get last sample
    xN, yN = X[i, :].T, y[i],

    thetaNprev, sNprev = theta[:, i],  s[:, :, i]

    if fit_intercept:
        xN = np.append(xN, [1])

    xN, yN = xN.reshape(q, -1), yN.reshape(1, -1)

    thetaNprev, sNprev = thetaNprev.reshape(q, -1), sNprev.reshape(q, q)


    eN = yN - np.matmul(xN.T, thetaNprev)

    sN = sNprev - np.matmul(xN, xN.T)

    kN = np.matmul(np.linalg.inv(sN), xN)

    thetaN = thetaNprev - np.matmul(kN, eN)

    theta = np.append(theta, thetaN, axis=1)
    s = np.append(s, sN.reshape(q, q, -1), axis=2)
    k = np.append(k, kN, axis=1)

theta[:,-1]