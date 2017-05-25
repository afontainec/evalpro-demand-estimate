import matplotlib.pyplot as plt
import numpy as np
n = 50
x = np.random.randn(n)
# y = x * np.random.randn(n)
y = 1 + 2 * x

# fig, ax = plt.subplots()
# fit = np.polyfit(x, y, deg=1)
# ax.plot(x, fit[0] * x + fit[1], color='red')
# ax.scatter(x, y)

# fig.show()


plt.plot(x, y, 'bo')
fit = np.polyfit(x, y, deg=1)

plt.plot(x, fit[0] * x + fit[1], color='red')
fit2 = np.polyfit(x, y, deg=2)
plt.plot(x,fit2[2] + fit2[1] * x + fit2[0] * x * x, color='green')




plt.show()
