import matplotlib.pyplot as plt

y = range(20)
x1 = range(20)
x2 = range(0, 200, 10)

fig, axes = plt.subplots(ncols=2, sharey=True)
axes[0].barh(y, x1, align='center', color='red')
axes[1].barh(y, x2, align='center', color='blue')
axes[0].invert_xaxis()
plt.savefig('foo.png')
plt.close(fig)
