import numpy as np

testArray = np.array([[1,2],
                      [3,4]])

def mirror(arr):
    vertical_mirror = np.flipud(arr)
    vertical_stack = np.vstack((arr, vertical_mirror))

    horizontal_mirror = np.fliplr(vertical_stack)
    horizontal_stack = np.hstack((vertical_stack, horizontal_mirror))

    return horizontal_stack

if __name__ == "__main__":
    res = mirror(testArray)
    print(res)