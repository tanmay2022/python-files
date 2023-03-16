import csv
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

file_start_time = 0;
file_end_time = 278;

dt = 1.0e-8
write = 1.0e-5
count = int(write/dt)

time = range(file_start_time, file_end_time);
# find time from range and dt

phi_Liq_ave = np.zeros(file_end_time);
c_L_ave = np.zeros(file_end_time);

c_scheil = np.zeros(file_end_time);
#B_Sol = (0.8168*18751.246-0.92642*78780.5778);

temparr = pd.read_csv('tempvstime.csv');
time1 = np.array(temparr.loc[:,'time']).squeeze()
time1 = np.insert(time1, 0, 0.)
temp1 = np.array(temparr.loc[:,'temp']).squeeze()
temp1 = np.insert(temp1, 0, temp1[0])
time2 = time1[0:-1:count]
temp2 = temp1[0:-1:count]
T_func = interp1d(time2, temp2, kind='cubic')
# use time to find temp

tdb = pd.read_csv('Composition_FCC_A1.csv');
T_tdb = np.array(tdb.loc[:,'T']).squeeze()
c_S_tdb = np.array(tdb.loc[:,'X_AL_FCC_A1_']).squeeze()
c_L_tdb = np.array(tdb.loc[:,'X_AL_LIQUID_']).squeeze()
cST_func = interp1d(T_tdb, c_S_tdb, kind='cubic')
cLT_func = interp1d(T_tdb, c_L_tdb, kind='cubic')
# use temp to find compo

compo_tdb_func = interp1d(c_L_tdb, c_S_tdb, kind='cubic')

tdb_hliq = pd.read_csv('HSN_LIQUID.csv');
hl_tdb = np.array(tdb_hliq.loc[:,'d2G_LIQUID_AL_0.817']).squeeze()
hlT_func = interp1d(T_tdb, hl_tdb, kind='cubic')
# use temp to find hessian

tdb_hsol = pd.read_csv('HSN_FCC_A1.csv');
hs_tdb = np.array(tdb_hsol.loc[:,'d2G_FCC_A1_AL_0.817']).squeeze()
hsT_func = interp1d(T_tdb, hs_tdb, kind='cubic')
# use temp to find hessian

scheil = pd.read_csv('scheil');

c_L_scheil = np.array(scheil.loc[:,'c_liq']).squeeze()
f_L_scheil = np.array(scheil.loc[:,'f_l']).squeeze()


for n in time:
    file_time = n;
    f_name = "AlZn0." + str(file_time) + ".csv"
    #file = open(f_name);
    data = pd.read_csv(f_name);
    #csvreader = csv.reader(file);
    print(n)
    
    mu = np.array(data.loc[:,'mu']).squeeze()
    phi = np.array(data.loc[:,'phi']).squeeze()
    
    temp_n = T_func(n*write).item();
    cs_n = cST_func(temp_n).item();
    cl_n = cLT_func(temp_n).item();
    hs_n = hsT_func(temp_n).item();
    hl_n = hlT_func(temp_n).item();
    
    B_Sol = (cl_n*hl_n - cs_n*hs_n)
    
    c_Sol = (mu-B_Sol)/hs_n;
    c_Liq = mu/hl_n;
    
    phi_Liq = (1.0-phi);
    c = np.add(np.multiply(c_Sol,phi), np.multiply(c_Liq,phi_Liq));
    
    c_L = np.multiply(c,phi_Liq);
    #c_S = np.multiply(c,phi);
    
    phi_Liq_ave[n] = np.average(phi_Liq);
    c_L_ave[n] = np.average(c_L)/phi_Liq_ave[n];
    #c_S_ave[n] = np.average(c_S)/np.average(phi);
    
    c_S_ave = compo_tdb_func(c_L_ave[n]).item();
    
    if (n == 0):
        c_scheil[n] = c_L_ave[n];
    else:
        c_scheil[n] = c_scheil[n-1] + (c_L_ave[n] - c_S_ave)* \
        (-phi_Liq_ave[n] + phi_Liq_ave[n-1])/phi_Liq_ave[n];
        



# In[]:
    
df_OF = pd.DataFrame({'phi_Liq_ave': phi_Liq_ave, 'c_L_ave': c_L_ave})
df_OF.to_csv('AlZn_avecl_fl.csv', index=False)
    
plt.plot(phi_Liq_ave,c_L_ave,'*-b', label = 'OpenFOAM simulation', linewidth = 1.5, markersize = 4);

#scheil = 0.8168*(phi_Liq_ave)**(0.9264/0.8168-1);

#plt.plot(phi_Liq_ave,c_scheil,'-k');
plt.plot(f_L_scheil[:83],c_L_scheil[:83],'-r', label = 'Scheil equation', linewidth = 1.5, markersize = 4);

plt.xlabel(r'<(1 - $\phi$)>', fontsize=15);
plt.ylabel('<$c_{Liq}$>', fontsize=15);

#plt.legend(['OpenFOAM', 'Scheil']);
plt.legend();
plt.title('Comparison of average liquidus composition vs \n average liquidus volume fraction obtained from \n OpenFOAM simulation and Scheil equation')
plt.savefig('OF_Scheil_comparison.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show();
