import numpy as np
import pandas as pd 
from matplotlib import pyplot as pyplot
import math

seam = input('Is it the Seam(y/n): ')
if(seam == 'n'):
    radius = 0.257
else:
    radius = 0.257

degs = np.linspace(0, 360, 1000)

x_points = np.empty(0)
y_points = np.empty(0)

for deg in degs:
    x_points = np.append(x_points, (-1)*radius*math.cos(math.radians(deg)))
    y_points = np.append(y_points, radius*math.sin(math.radians(deg)))

points = pd.DataFrame({'X': x_points, 'Y': y_points})

points.to_csv(r'E:\Aman\points.csv', index=False)

