import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt 
import math
from scipy.integrate import simps

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
degs_for_ticks = degs + 90
num_of_degs = len(degs) 

check = np.array_split(tcdata, num_of_degs)
pos = 0

# Calculating Displacement Thickness

def Displacement_Thickness(val, dy):
    dis_thick = simps(val, dy)
    return dis_thick

# Calculating Boundary Layer Thickness

bl_thick = np.empty(0)
bl_thick_x = np.empty(0)
bl_thick_y = np.empty(0)

displacement_thickness = np.empty(0)

for df in check:
    df['deg'] = degs[pos]
    df['radial'] = np.linspace(0, max_limit - radius, 1000)
    df['Vel_Per'] = (df['U'] * math.cos(math.radians(degs[pos]))) - (df['V'] * math.sin(math.radians(degs[pos])))
    index_of_max_vel = df.idxmax(axis=0)['Vel_Per'] - pos*1000
    # print(index_of_max_vel)
    # print(df['radial'].iloc[index_of_max_vel])
    if(index_of_max_vel != 999):
        bl_thick = np.append(bl_thick, df['radial'].iloc[index_of_max_vel])
        bl_thick_x = np.append(bl_thick_x, df['X'].iloc[index_of_max_vel])
        bl_thick_y = np.append(bl_thick_y, df['Y'].iloc[index_of_max_vel])
    
    u = df[['Vel_Per']].to_numpy()
    u = np.asarray(u).squeeze()
    val = np.ones(len(u)) - u

    dy = df[['radial']].to_numpy()
    dy = np.asarray(dy).squeeze()

    # print(val)
    # print(dy[:index_of_max_vel])
    dis_thick = Displacement_Thickness(val[:index_of_max_vel], dy[:index_of_max_vel])
    displacement_thickness = np.append(displacement_thickness, dis_thick)
    pos = pos + 1

till = len(bl_thick) 
bl = pd.DataFrame({'X': bl_thick_x, 'Y': bl_thick_y})
bl.to_csv(r'E:\Aman\bl.csv', index=False)

# Calculating Points for Displacement Thickness

dis_thick_x = np.empty(0)
dis_thick_y = np.empty(0)
pos = 0

for deg in degs:
    distance = displacement_thickness[pos] + radius
    x_val = distance * math.sin(math.radians(deg))
    y_val = distance * math.cos(math.radians(deg))
    dis_thick_x = np.append(dis_thick_x, x_val)
    dis_thick_y = np.append(dis_thick_y, y_val)
    pos = pos + 1

dis_thick_x = dis_thick_x[:till]
dis_thick_y = dis_thick_y[:till]
dis = pd.DataFrame({'X': dis_thick_x, 'Y': dis_thick_y})
dis.to_csv(r'E:\Aman\dis.csv', index=False)

# Plotting

fig, ax = plt.subplots(1)

for df in check:
    ax.plot(df['Vel_Per'], df['radial'], label=str(int(df['deg'].iloc[0] + 90)) + r'$^\circ$')
    
plt.xlabel('u')
plt.ylabel('y')
plt.title('Velocity Profile')
plt.legend(ncol=4)

test = bl_thick/3
test2 = bl_thick/6
fig2, ax2 = plt.subplots(1)
# The following plot does not seem like  what was thought as it is flow past sphere and not a flat plate.
ax2.plot(degs_for_ticks[:till], bl_thick, label='Boundary Layer Thickness')
ax2.plot(degs_for_ticks[:till], test, label='Boundary Layer Thickness/3')
ax2.plot(degs_for_ticks[:till], test2, label='Boundary Layer Thickness/6')
ax2.plot(degs_for_ticks[:till], displacement_thickness[:till], label='Displacement Thickness')
plt.xlabel('Angle')
plt.ylabel('Thickness')
plt.legend(loc='center')
plt.show()
