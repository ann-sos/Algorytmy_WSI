import matplotlib.pyplot as plt
import numpy as np
import random


def y(x):
    return 17.8 * (x - 20) ** 2 + 0.3 * x + 43.6


def gradient(x1, x2):
    if (x2 - x1) != 0:
        return (y(x2) - y(x1)) / (x2 - x1)
    else:
        return 1


plot_range = [0, 100]
x = np.arange(-100, 100)
plt.plot(x, y(x))


h = 0.5 # dlugość kroku
x0 = random.randrange(plot_range[0], plot_range[1])     # punkt startowy

plt.plot(x0, y(x0), 'r.')
xi1 = x0
xi2 = xi1 + h
epsilon = 0.5
while np.abs(gradient(xi1, xi2)) >= epsilon:
    print(xi2)
    if y(xi2) > y(xi1):
        h = h / 2
        xi2 = xi1 - h * gradient(xi1, xi2)
    if y(xi2) < y(xi1):
        xi1 = xi1 - h * gradient(xi1, xi2)
        xi2 = xi2 - h * gradient(xi1, xi2)
print(xi2)
plt.plot(xi2, y(xi2), 'go')
plt.show()