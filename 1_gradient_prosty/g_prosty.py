import matplotlib.pyplot as plt
import numpy as np


def y1(x):
    return 3.04 * x ** 2 + 3.76 * x - 18


def y2(x):
    return 0.0034 * x  ** 4  - 20 * x ** 2 - 170 * x


def gradient(y, x1, x2):
    if (x2 - x1) != 0:
        return (y(x2) - y(x1)) / (x2 - x1)
    else:
        return 1


def gradient_descent(x, y, h, x0, func: str):
    plt.figure()
    x2_array = []
    y2_array = []
    plt.plot(x, y(x))
    plt.plot(x0, y(x0), 'r.')
    xi1 = x0
    xi2 = xi1 + h
    epsilon = 0.5
    while abs(gradient(y, xi1, xi2)) >= epsilon:
        x2_array.append(xi2)
        y2_array.append(y(xi2))

        xi1, xi2 = xi2, xi2 - h * gradient(y, xi1, xi2)
        #print("xi1", xi1)
        #print("xi2", xi2)
        print("gradient(y, xi1, xi2)", gradient(y, xi1, xi2))
    plt.plot(x2_array, y2_array, 'g.--')
    for i in range(len(x2_array)):
        plt.annotate(str(i), xy=(x2_array[i], y2_array[i]+y(x[0])/20), fontsize=6)
    plt.annotate(f"h = {h}", xy=(x[0], 0))
    ann2 = "$x_{min}$ =" + "{my_min:.2f}".format(my_min=xi2)
    plt.annotate(ann2, xy=(x[0], y(x[0]) / 10))
    plt.annotate(f"$\epsilon = {epsilon}$", xy=(x[0], y(x[0])* 2 / 10))
    plt.title(func)
    plt.show()


if __name__ == "__main__":
    h = 2*1e-2  # dlugość kroku
    x = np.arange(-100, 100)
    #gradient_descent(x, y1, h, 70, "$3.04 \cdot x^2 + 3.76 \cdot x - 18$")
    gradient_descent(x, y2, h, -100, "$0.0034 \cdot x  ** 4  - 20 \cdot x ** 2 - 170 \cdot x$")
    """plt.plot(x, y2(x))
    plt.show()"""