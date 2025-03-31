import matplotlib.pyplot as plt
import numpy as np

a=3
b=4
c=-3
d=-10
minX=-10
maxX=10


def thirdDegreePlot(a, b, c, d, minX, maxX):
    xArr = np.linspace(minX, maxX, int(1+10*(maxX - minX)))

    resArr = a*xArr**3 + b*xArr**2 + c*xArr + d

    return plt.plot(xArr, resArr)


if __name__ == "__main__":
    thirdDegreePlot(a, b, c, d, minX, maxX)
    plt.show()