#import csv
#import math
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
#from scipy.interpolate import CubicSpline

arr = pd.read_csv('tempvstime.csv');

time1 = np.array(arr.loc[:,'time']).squeeze()
time1 = np.insert(time1, 0, 0.)
temp1 = np.array(arr.loc[:,'temp']).squeeze()
temp1 = np.insert(temp1, 0, temp1[0])

dt = 1.0e-8
write = 1.0e-5
count = int(write/dt)

time = time1[0:-1:count]
temp = temp1[0:-1:count]

tempvstime = CubicSpline(time,temp)

dtemp = tempvstime.derivative(nu=1)

n = len(time)

temprate = []
timeave = []


for i in range(0,n-1):
    timeave_i = 0.5*float(time[i]+time[i+1])
    timeave.append(timeave_i)
    
    temprate_i = float(temp[i+1]-temp[i])/(time[i+1]-time[i])
    temprate.append(temprate_i)	
    


# In[]:
    
df_OF = pd.DataFrame({'timeave': time, 'temprate': dtemp(time)})
df_OF.to_csv('temprate.csv', index=False)

plt.plot(time,dtemp(time),'*-b', label = 'AlZn alloy', linewidth = 1.5, markersize = 4);
#plt.plot(timeave,temprate,'*-b', label = 'AlZn alloy', linewidth = 1.5, markersize = 4);
#plt.plot(time,temp,'*-b', label = 'AlZn alloy', linewidth = 1.5, markersize = 4);


#plt.xlim()
#plt.ylim([0, 100])

plt.xlabel('t', fontsize=15);
plt.ylabel('dT/dt', fontsize=15);
#plt.ylabel('T', fontsize=15);

#plt.legend(['OpenFOAM', 'Scheil']);
plt.legend();
#plt.title('Comparision of average liquidus composition vs \n average liquidus volume fraction obtained from \n OpenFOAM simulation and Scheil equation')
#plt.savefig('Temperature_AlZn.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.savefig('Temperature_rate_AlZn.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show();
