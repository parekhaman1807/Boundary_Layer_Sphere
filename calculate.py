import numpy as np 
import pandas as pd 
from matplotlib import pyplot as plt 
import math
from scipy.integrate import simps
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset

re = float(input("Enter Reynold's Number: "))
surface = input("Enter Surface: ")
# radius = float(input("Enter the Radius of the Sphere: "))
radius = 0.249276
max_limit = radius * 2
viscosity = (2 * radius)/re
density = 1

# Setting up the DataFrame

cols = ['X', 'Y', 'U', 'V', 'dudy']
tcdata = pd.read_csv(r'E:\Aman\tcdata.csv', sep=',', names=cols)
tcdata['dudy'] = tcdata['V']
tcdata['V'] = tcdata['U']
tcdata['U'] = tcdata['Y']
tcdata['Y'] = tcdata['X']
tcdata['X'] = tcdata.index 
tcdata = tcdata.reset_index()
tcdata = tcdata.drop(columns=['index'])

frequency = float(input("Enter the Angle Frequency: "))
degs = np.arange(-40, 51, frequency)
degs_for_ticks_upper = degs + 90
degs_for_ticks_lower = degs - 90
num_of_degs = len(degs) 

check = np.array_split(tcdata, num_of_degs)
pos = 0

# Calculating Displacement Thickness

def Displacement_Thickness(val, dy):
    dis_thick = simps(val, dy)
    return dis_thick

def Momentum_Thickness(val1, val2, dy):
    y = np.multiply(val1, val2)
    momen_thick = simps(y, dy)
    return momen_thick

# Calculating Boundary Layer Thickness

bl_thick = np.empty(0)
bl_thick_x = np.empty(0)
bl_thick_y = np.empty(0)

displacement_thickness = np.empty(0)
momentum_thickness = np.empty(0)

uy = np.empty(0)
uy_self = np.empty(0)

for df in check:
    df['deg'] = degs[pos]
    df['radial'] = np.linspace(0, max_limit - radius, 10000)

    df['Vel_Per'] = (df['U'] * math.cos(math.radians(degs[pos]))) - (df['V'] * math.sin(math.radians(degs[pos])))

    index_of_max_vel = df.idxmax(axis=0)['Vel_Per'] - pos*10000
    # print(index_of_max_vel)
    # print(df['radial'].iloc[index_of_max_vel])
    if(index_of_max_vel != 999):
        bl_thick = np.append(bl_thick, df['radial'].iloc[index_of_max_vel])
        bl_thick_x = np.append(bl_thick_x, df['X'].iloc[index_of_max_vel])
        bl_thick_y = np.append(bl_thick_y, df['Y'].iloc[index_of_max_vel])
    
    u = df[['Vel_Per']].to_numpy()
    u = np.asarray(u).squeeze()
    U = df['Vel_Per'].iloc[index_of_max_vel]
    U = U * np.ones(len(u))
    val = np.ones(len(u)) - (np.divide(u, U))

    dy = df[['radial']].to_numpy()
    dy = np.asarray(dy).squeeze()

    # print(val)
    # print(dy[:index_of_max_vel])
    dis_thick = Displacement_Thickness(val[:index_of_max_vel], dy[:index_of_max_vel])
    displacement_thickness = np.append(displacement_thickness, dis_thick)

    momen_thick = Momentum_Thickness(np.divide(u[:index_of_max_vel], U[:index_of_max_vel]), val[:index_of_max_vel], dy[:index_of_max_vel])
    momentum_thickness = np.append(momentum_thickness, momen_thick)

    # Trying to Calculate du/dy at the Surface
    dudy_self = (df['Vel_Per'].iloc[1] - df['Vel_Per'].iloc[0])/(df['radial'].iloc[1] - df['radial'].iloc[0])
    uy_self = np.append(uy_self, dudy_self)
    dudy = df['dudy'].iloc[3]
    uy = np.append(uy, dudy)
    # print(df['dudy'])
    
    # if(dudy>0):
    fricvel = math.sqrt((viscosity * abs(dudy_self))/density)
    df['Non_Dim_Vel_Per'] = df['Vel_Per']/fricvel
    df['Non_Dim_radial'] = (df['radial'] * fricvel)/viscosity
        # df['Non_Dim_Vel_Per'].iloc[0] = df['Non_Dim_Vel_Per'].iloc[1]
        # df['Non_Dim_radial'].iloc[0] = df['Non_Dim_radial'].iloc[1]

    # else:
        # df['check_for_sep'] = np.zeros(10000)
    # print(degs[pos])
    # print(degs_for_ticks_upper[pos], dudy_self, dudy)
    pos = pos + 1

till = len(bl_thick) 

bl = pd.DataFrame({'X': bl_thick_x, 'Y': bl_thick_y})
bl.to_csv(r'E:\Aman\bl.csv', index=False)

# Calculating Points for Displacement Thickness

dis_thick_x = np.empty(0)
dis_thick_y = np.empty(0)
momen_thick_x = np.empty(0)
momen_thick_y = np.empty(0)
pos = 0

for deg in degs:
    displacement_distance = displacement_thickness[pos] + radius
    x_val_dis = displacement_distance * math.sin(math.radians(deg))
    y_val_dis = displacement_distance * math.cos(math.radians(deg))
    dis_thick_x = np.append(dis_thick_x, x_val_dis)
    dis_thick_y = np.append(dis_thick_y, y_val_dis)

    momentum_distance = momentum_thickness[pos] + radius
    x_val_momen = momentum_distance * math.sin(math.radians(deg))
    y_val_momen = momentum_distance * math.cos(math.radians(deg))
    momen_thick_x = np.append(momen_thick_x, x_val_momen)
    momen_thick_y = np.append(momen_thick_y, y_val_momen)

    pos = pos + 1

dis_thick_x = dis_thick_x[:till]
dis_thick_y = dis_thick_y[:till]
dis = pd.DataFrame({'X': dis_thick_x, 'Y': dis_thick_y})
dis.to_csv(r'E:\Aman\dis.csv', index=False)

momen_thick_x = momen_thick_x[:till]
momen_thick_y = momen_thick_y[:till]
momen = pd.DataFrame({'X': momen_thick_x, 'Y': momen_thick_y})
momen.to_csv(r'E:\Aman\momen.csv', index=False)

# Plotting

if(surface == 'upper'):

    fig4, ax4 = plt.subplots(1)
    
    for df in check:
        df['Non_Dim_radial'].iloc[0] = 0
        df['Non_Dim_Vel_Per'].iloc[0] = 0
        ax4.plot(df['Non_Dim_radial'], df['Non_Dim_Vel_Per'], label=str(int(df['deg'].iloc[0] + 90)) + r'$^\circ$', linewidth=3.0)

    yplus = np.linspace(0,1000, 10000)
    uplus = yplus
    uplusplus = (np.log(yplus)/0.41) + 5.0
    ax4.plot(yplus, uplus, 'b--', label='u+ = y+')
    ax4.plot(yplus, uplusplus, 'b--', label='Log Law')
    ax4.set_xlim(0.1, 1000)
    ax4.set_ylim(0, 40)
    plt.xscale('log')
    plt.xlabel('y+')
    plt.ylabel('u+')
    plt.title('Velocity Profiles in Inner Variables')
    plt.legend()

    fig, ax = plt.subplots(1)

    for df in check:
        ax.plot(df['Vel_Per'], df['radial']/radius, label=str(int(df['deg'].iloc[0] + 90)) + r'$^\circ$')

    ax.set_ylim(0, 0.15)    
    plt.xlabel('u')
    plt.ylabel('y/D')
    plt.title('Velocity Profile')
    plt.legend()

    test = bl_thick/3
    test2 = bl_thick/6
    fig2, ax2 = plt.subplots(1)

    # The following plot does not seem like  what was thought as it is flow past sphere and not a flat plate.
    ax2.plot(degs_for_ticks_upper[:till], bl_thick, label='Boundary Layer Thickness')
    # ax2.plot(degs_for_ticks[:till], test, label='Boundary Layer Thickness/3', alpha=0.10)
    # ax2.plot(degs_for_ticks[:till], test2, label='Boundary Layer Thickness/6', alpha=0.10)
    plt.gca().fill_between(degs_for_ticks_upper[:till],
                            test, test2,
                            alpha=0.25,
                            label='Blasius Laminar Profile Displacement Thickness Domain(1/3 to 1/6)')
    ax2.plot(degs_for_ticks_upper[:till], displacement_thickness[:till], label='Displacement Thickness')
    ax2.plot(degs_for_ticks_upper[:till], momentum_thickness[:till], label='Momentum Thickness')
    plt.xlabel('Angle')
    plt.ylabel('Thickness')
    plt.legend(loc='center')

    fig3, ax3 = plt.subplots(1)
    shape_factor = np.divide(displacement_thickness[:till], momentum_thickness[:till])
    ax3.plot(degs_for_ticks_upper[:till], shape_factor)
    plt.xlabel('Angle')
    plt.ylabel('Shape Factor')
    ax3.set_ylim(0,4)
    # axins = zoomed_inset_axes(ax3, 1.5, loc=2)
    # axins.plot(degs_for_ticks[:till], shape_factor)
    # axins.set_ylim(0, 3)
    # axins.set_xlim(50, 110)
    # mark_inset(ax3, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    fig5, ax5 = plt.subplots()
    ax5.plot(degs_for_ticks_upper, uy, label='Calculated externally')
    ax5.plot(degs_for_ticks_upper, uy_self, label='Calculated in Tecplot')
    plt.legend()
    plt.show()

    shape_fac = pd.DataFrame({'deg': degs_for_ticks_upper[:till], 'Y': shape_factor})
    shape_fac.to_csv(r'E:\Aman\upper_100k.csv', index=False)
else:

    fig4, ax4 = plt.subplots(1)
    
    for df in check:
        ax4.plot(df['Non_Dim_radial'], df['Non_Dim_Vel_Per'], label=str(int(df['deg'].iloc[0] - 90)) + r'$^\circ$', linewidth=3.0)


    yplus = np.linspace(0,1000, 10000)
    uplus = yplus
    uplusplus = (np.log(yplus)/0.41) + 5.0
    ax4.plot(yplus, uplus, 'b--', label='u+ = y+')
    ax4.plot(yplus, uplusplus, 'b--', label='Log Law')
    ax4.set_xlim(0.1, 1000)
    ax4.set_ylim(0, 30)
    plt.xscale('log')
    plt.xlabel('y+')
    plt.ylabel('u+')
    plt.title('Velocity Profiles in Inner Variables')
    plt.legend()

    fig, ax = plt.subplots(1)

    for df in check:
        ax.plot(df['Vel_Per'], df['radial']/radius, label=str(int(df['deg'].iloc[0] - 90)) + r'$^\circ$')

    ax.set_ylim(0, 0.15)    
    plt.xlabel('u')
    plt.ylabel('y/D')
    plt.title('Velocity Profile')
    plt.legend()

    test = bl_thick/3
    test2 = bl_thick/6
    fig2, ax2 = plt.subplots(1)

    # The following plot does not seem like  what was thought as it is flow past sphere and not a flat plate.
    ax2.plot(degs_for_ticks_lower[:till], bl_thick, label='Boundary Layer Thickness')
    # ax2.plot(degs_for_ticks[:till], test, label='Boundary Layer Thickness/3', alpha=0.10)
    # ax2.plot(degs_for_ticks[:till], test2, label='Boundary Layer Thickness/6', alpha=0.10)
    plt.gca().fill_between(degs_for_ticks_lower[:till],
                            test, test2,
                            alpha=0.25,
                            label='Blasius Laminar Profile Displacement Thickness Domain(1/3 to 1/6)')
    ax2.plot(degs_for_ticks_lower[:till], displacement_thickness[:till], label='Displacement Thickness')
    ax2.plot(degs_for_ticks_lower[:till], momentum_thickness[:till], label='Momentum Thickness')
    plt.gca().invert_xaxis()
    plt.xlabel('Angle')
    plt.ylabel('Thickness')
    plt.legend(loc='center')

    fig3, ax3 = plt.subplots(1)
    shape_factor = np.divide(displacement_thickness[:till], momentum_thickness[:till])
    ax3.plot(degs_for_ticks_lower[:till], shape_factor)
    plt.gca().invert_xaxis()
    plt.xlabel('Angle')
    plt.ylabel('Shape Factor')
    ax3.set_ylim(0,4)
    # axins = zoomed_inset_axes(ax3, 1.5, loc=2)
    # axins.plot(degs_for_ticks[:till], shape_factor)
    # axins.set_ylim(0, 3)
    # axins.set_xlim(50, 110)
    # mark_inset(ax3, axins, loc1=2, loc2=4, fc="none", ec="0.5")

    plt.show()

    shape_fac = pd.DataFrame({'degs': degs_for_ticks_lower[:till], 'Y': shape_factor})
    shape_fac.to_csv(r'E:\Aman\lower_100k.csv', index=False)