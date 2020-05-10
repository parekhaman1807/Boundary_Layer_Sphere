import numpy as np 
from matplotlib import pyplot as plt 
from scipy.integrate import simps
import math

x = np.arange(0, 1.01, 0.01)
y = x**2

integ = simps(y, x)
print(integ)
integ = integ * np.ones(len(x))

fig, (ax1, ax2) = plt.subplots(1, 2, sharex=True, sharey=True)

ax1.plot(x, y)
ax1.fill_between(x,
                0, y,
                alpha=0.25)
ax1.title.set_text('Parabolic Boundary Layer Profile')
ax2.plot(x, integ)
ax2.fill_between(x,
                0, integ,
                alpha=0.25)
ax2.title.set_text('Displacement Thickness')
plt.show()