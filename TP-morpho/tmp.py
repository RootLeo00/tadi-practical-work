from numpy import *
import math
import matplotlib.pyplot as plt

t = linspace(0, 2*math.pi, 400)
a = -log(t)
b = (1 - t)**2

yhat=0.1
plt.plot(t, a, 'r') # plotting t, a separately 
plt.plot(t, b, 'b') # plotting t, b separately 
# plt.plot(yhat, -log(yhat), marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")
# plt.plot(yhat, (1 - yhat)**2, marker="o", markersize=5, markeredgecolor="red", markerfacecolor="green")

plt.show()