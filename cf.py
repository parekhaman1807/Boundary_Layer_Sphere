import numpy as np
import pandas as pd 
from matplotlib import pyplot as plt
import math

Re = float(input("Enter Reynold's Number: "))
radius = 0.25

degs = np.linspace(0, 360, 1000)

cols = ['X', 'Y', 'U', 'V', 'dudy', 'shear']
cfdata = pd.read_csv(r'E:\Aman\cfdata.csv', sep=',', names=cols)
cfdata['shear'] = cfdata['dudy']
cfdata['dudy'] = cfdata['V']
cfdata['V'] = cfdata['U']
cfdata['U'] = cfdata['Y']
cfdata['Y'] = cfdata['X']
cfdata['X'] = cfdata.index 
cfdata = cfdata.reset_index()
cfdata = cfdata.drop(columns=['index'])
print(cfdata)

utheta = np.empty(0)

deg = degs[0]
step_size = degs[1] - degs[0]
for i in range(len(cfdata.index)):
    deg = deg + step_size
#     # print(deg)
#     # if(deg>90 or deg<270):
#         # u = (-1)*(cfdata['U'].iloc[i]*math.sin(math.radians(deg)) + cfdata['V'].iloc[i]*math.cos(math.radians(deg)))
#     # else:
    u = cfdata['U'].iloc[i]*math.sin(math.radians(deg)) + cfdata['V'].iloc[i]*math.cos(math.radians(deg))
    utheta = np.append(utheta, u)

cf_self = []
for i in utheta:
    uy = i/0.000722
    b = uy/Re
    cf_self.append(b)

dudy = cfdata['shear'].tolist()
cf = []
for i in dudy:
    a = 2 * i
    cf.append(a)
    # print(a)

zero = np.empty(0)
zero_self = np.empty(0)
angle = np.empty(0)
angle_self = np.empty(0)
a = 150
for i in cf[150:750]:
    print(i)
    if(i<0.00002 and i>-0.00002):
        zero = np.append(zero, 0)
        angle = np.append(angle, a*step_size)
    a = a + 1

a = 150
for i in cf_self[150:750]:
    if(i<0.0002 and i>-0.0002):
        zero_self = np.append(zero_self, 0)
        angle_self = np.append(angle_self, a*step_size)
    a = a + 1

# print(angle[0], angle[-1])

fig, ax = plt.subplots(1)

# print(degs, cf)
ax.plot(degs, cf, label='Calculated in TecPlot', linewidth=3)
cf_store = pd.DataFrame({'deg': degs, 'cf': cf})
cf_store.to_csv(r'E:\Aman\50kcf.csv', index=False)
ax.plot(angle[0], zero[0], 'b', marker='o', markersize=10)
ax.plot(angle[-1], zero[-1], 'b', marker='o', markersize=10)
# ax.plot(degs, cf_self, label='Calculated Externally', linewidth=3)
# ax.plot(angle_self[0], zero_self[0], 'o', marker='o', markersize=10)
# ax.plot(angle_self[-1], zero_self[-1], 'o', marker='o', markersize=10)
ax.set_xlim(0, 360)
ax.set_ylim(-0.01, 0.01)
plt.xlabel('theta')
plt.ylabel('C_f')
plt.title('C_f vs Theta')
# plt.legend()
plt.show()