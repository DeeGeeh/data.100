import numpy as np

testArr = np.array(
[[8, 6, 7, 4, 5],
 [4, 1, 2, 9, 3],
 [5, 6, 8, 2, 8],
 [1, 3, 8, 7, 5],
 [4, 8, 1, 9, 5]])


def addAverages(arr):
    meanPerRow = np.mean(arr, axis=1, keepdims=True)
    step1 = np.hstack((arr, meanPerRow))
    
    meanPerColumn = np.mean(step1, axis=0, keepdims=True)
    result = np.vstack((step1, meanPerColumn))

    return result


if __name__ == "__main__":
    res = addAverages(testArr)
    print(res)