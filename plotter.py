import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import math

bl_thick = pd.read_csv(r'E:\Aman\bl.csv')
dis_thick = pd.read_csv(r'E:\Aman\dis.csv')
momen_thick = pd.read_csv(r'E:\Aman\momen.csv')

radius = float(input("Enter the Radius of the Sphere: "))

degs = np.arange(-90, 91, 0.1)

x_points = np.empty(0)
y_points = np.empty(0)

for deg in degs:
    x = radius * math.sin(math.radians(deg))
    y = radius * math.cos(math.radians(deg))

    x_points = np.append(x_points, x)
    y_points = np.append(y_points, y)

fig, ax = plt.subplots(1)

# ax.plot(x_points, y_points, linewidth=0.5)
plt.gca().fill_between(x_points,
                        0, y_points,
                        alpha=0.25)
ax.plot(bl_thick['X'], bl_thick['Y'], label='Boundary Layer Thickness')
ax.plot(dis_thick['X'], dis_thick['Y'], label='Displacement Thickness')
ax.plot(momen_thick['X'], momen_thick['Y'], label='Momentum Thickness')
plt.xlim([(-radius*2), (radius*2)])
plt.ylim([0, (radius*3)])
ax.axes.set_aspect(aspect='equal')
plt.legend(loc='center')
plt.show()