import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt 
import math

surface = input("Enter Surface: ")
radius = float(input("Enter the Radius of the Sphere: "))

if(surface == 'lower'):
    radius = radius * (-1)
max_limit = radius * 2

frequency = float(input("Enter the Frequency of Angles: "))
degs = np.arange(-40, 51, frequency)

data = pd.DataFrame(columns=['X','Y'])

def LineGenerator(deg):
    x_start = radius * math.sin(math.radians(deg))
    x_end = max_limit * math.sin(math.radians(deg))
    y_start = radius * math.cos(math.radians(deg))
    y_end = max_limit * math.cos(math.radians(deg))
    
    x_points = np.linspace(x_start, x_end, 10000)
    y_points = np.linspace(y_start, y_end, 10000)
    radial = np.linspace(radius, max_limit, 10000)

    return x_points, y_points, radial

for deg in degs:
    x, y, radial = LineGenerator(deg)
    temp = pd.DataFrame({'X': x, 'Y': y})
    data = pd.concat([data, temp], sort=False)

# fig, ax = plt.subplots(1)

# ax.plot(data['X'], data['Y'])
# ax.axes.set_aspect(aspect = 'equal')
# plt.show()

data.to_csv(r'E:\Aman\data.csv', index=False)
