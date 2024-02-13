#import csv
#import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline


file_start = 0
file_end = [140, 70, 70]

hotzone_temp = [1653, 1700, 1750]

fmt=["ob", "or", "ok"]
legn=['1653K', '1700K', '1750K']

#iterating over different cases
for m in range(0,len(hotzone_temp)):

    save_steps = range(file_start, file_end[m]);

    time_array = np.zeros(file_end[m]);
    tempgrad_array = np.zeros(file_end[m]);


#reading from csv
    for n in save_steps:
        arr = pd.read_csv(str(hotzone_temp[m])+'K/csv/'+str(hotzone_temp[m])+'K_'+str(n)+'.csv');

#arr = pd.read_csv(str(hotzone_temp)+'K/csv/'+str(hotzone_temp)+'K_10.csv');

        time1 = np.array(arr.loc[:,'Time']).squeeze()
#time1 = np.insert(time1, 0, 0.)
        temp1 = np.array(arr.loc[:,'Tpsi']).squeeze()
#temp1 = np.insert(temp1, 0, temp1[0])
        x1 = np.array(arr.loc[:,'arc_length']).squeeze()

        time_array[n] = time1[0]
# considering only the region with psi=1
        temp = temp1[70:-70:5]
        x = x1[70:-70:5]

        tempvsx = CubicSpline(x,temp)

        tempgrad = tempvsx.derivative(nu=1)

        tempgrad_array[n] = np.max(tempgrad(x))

    #print('tempgrad = '+str(cold_tempgrad))

    
    df_OF = pd.DataFrame({'time': time_array, 'tempgrad': tempgrad_array})
    df_OF.to_csv('tempgrad_'+str(hotzone_temp[m])+'K.csv', index=False)

#plt.plot(x,tempgrad(x),'*-b', label = 'tempgrad', linewidth = 1.5, markersize = 4);
#plt.plot(x,temp,'*-b', label = 'temp', linewidth = 1.5, markersize = 4);
    #plt.plot(time_array,tempgrad_array,'*-b', label = 'tempgrad', linewidth = 1.5, markersize = 4);
    plt.plot(time_array, tempgrad_array, fmt[m], markerfacecolor='none', label = legn[m], linewidth = 1.5, markersize = 4)


#plt.xlabel('x', fontsize=15);
#plt.ylabel('dT/dx', fontsize=15);
#plt.ylabel('T', fontsize=15);

plt.xlabel('Time (s)', fontsize=15);
plt.ylabel('Thermal gradient (K/m)', fontsize=15);

plt.legend(legn);
#plt.legend();
plt.title('Thermal gradient at the cold-zone \n for different hot-zone temperatures')
#plt.savefig('Temperature.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.savefig('Temperature_gradient.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show();
