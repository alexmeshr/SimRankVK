import numpy as np


def colMinSum(mat, limit=2):
    idx = -1
    N = mat.shape[0]
    minSum = N+1+limit
    for i in range(N):
        sum = np.sum(mat[i])
        if (sum < minSum):
            minSum = sum
            idx = i
            if minSum < limit:
                break
    return idx, minSum


def clear_data(matr, users):
    #print([np.sum(matr[i]) for i in range(matr.shape[0])])
    idx, minSum = 0, 0
    while minSum < 2:
        idx, minSum = colMinSum(matr)
        matr = np.delete(np.delete(matr, idx, 0), idx, 1)
        users = np.delete(users, idx, 0)
    print("after data processing {} people remained, minimal friends count = {}".format(users.shape[0], minSum))
    return matr, users
