import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt 
import math

radius = float(input("Enter the Radius of the Sphere: "))
max_limit = radius * 2

# Setting up the DataFrame

cols = ['X', 'Y', 'U', 'V']
tcdata = pd.read_csv(r'E:\Aman\tcdata.csv', sep=',', names=cols)
tcdata['V'] = tcdata['U']
tcdata['U'] = tcdata['Y']
tcdata['Y'] = tcdata['X']
tcdata['X'] = tcdata.index 
tcdata = tcdata.reset_index()
tcdata = tcdata.drop(columns=['index'])

frequency = float(input("Enter the Angle Frequency: "))
degs = np.arange(-40, 61, frequency)
num_of_degs = len(degs) 

check = np.array_split(tcdata, num_of_degs)
pos = 0

bl_thick = np.empty(0)
bl_thick_x = np.empty(0)
bl_thick_y = np.empty(0)

for df in check:
    df['deg'] = degs[pos]
    df['radial'] = np.linspace(0, max_limit - radius, 1000)
    df['Vel_Per'] = (df['U'] * math.cos(math.radians(degs[pos]))) - (df['V'] * math.sin(math.radians(degs[pos])))
    index_of_max_vel = df.idxmax(axis=0)['Vel_Per'] - pos*1000
    print(index_of_max_vel)
    print(df['radial'].iloc[index_of_max_vel])
    if(index_of_max_vel != 999):
        bl_thick = np.append(bl_thick, df['radial'].iloc[index_of_max_vel])
        bl_thick_x = np.append(bl_thick_x, df['X'].iloc[index_of_max_vel])
        bl_thick_y = np.append(bl_thick_y, df['Y'].iloc[index_of_max_vel])
    pos = pos + 1



fig, ax = plt.subplots(1)

for df in check:
    ax.plot(df['Vel_Per'], df['radial'], label=str(int(df['deg'].iloc[0] + 90)) + r'$^\circ$')
    
plt.xlabel('u')
plt.ylabel('y')
plt.title('Velocity Profile')
plt.legend(ncol=4)

bl = pd.DataFrame({'X': bl_thick_x, 'Y': bl_thick_y})
bl.to_csv(r'E:\Aman\bl.csv', index=False)

fig2, ax2 = plt.subplots(1)
# The following plot does not seem like  what was thought as it flow past sphere and not a flat plate.
till = len(bl_thick) 
ax2.plot(degs[:till], bl_thick)
plt.show()
