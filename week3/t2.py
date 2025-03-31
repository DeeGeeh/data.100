import numpy as np

testLim = 20
testArray = np.array(
[[9, 4, 5, 9, 4, 6, 2, 3],
 [6, 3, 7, 5, 5, 4, 5, 5],
 [4, 4, 2, 8, 3, 9, 6, 3],
 [1, 2, 4, 4, 7, 1, 3, 6]])


def largeCols(arr, lim):
    columnSums = np.sum(arr, axis=0)
    mask = columnSums >= lim
    result = arr[:, mask]

    return result


if __name__ == "__main__":
    res = largeCols(testArray, testLim)
    print(res)