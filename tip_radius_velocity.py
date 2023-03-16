#!/usr/bin/env python
# coding: utf-8

# In[3]:


import csv
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[4]:

file_start_time = 1;
file_end_time = 100;

dt = 14e-8;
dx = 1e-8;
writeInterval = 1000*dt;

m   = 770;
DELTA_C = 0.921-0.817;
D   = 1e-9;

f_name_write = 'AlZn_Tm870_dT_13_OpenFoam.dat'

file_time = file_start_time;
t=0;

d_0 = 6.6e-8;


# In[17]:


f_name = "OF_contour0." + str(file_time) + ".csv"

#file = open(f_name);
data = pd.read_csv(f_name);
#csvreader = csv.reader(file);

X = np.array(data.loc[:,'Points:0']).squeeze()
Y = np.array(data.loc[:,'Points:1']).squeeze()

#print(Y);

X0 = X[0];
Y0 = Y[0];

XL = X[-1];
YL = Y[-1];

R  = np.add(np.multiply(X-X0,X-X0), np.multiply(Y-Y0, Y - Y0));
R_ = np.add(np.multiply(X-XL,X-XL), np.multiply(Y-YL, Y - YL));

data['CL'] = R - R_;

data = data.sort_values(by='CL');

X = np.array(data.loc[:,'Points:0']).squeeze()
Y = np.array(data.loc[:,'Points:1']).squeeze()

distance = np.add(np.multiply(X,X),np.multiply(Y,Y));

d_old = math.sqrt(np.amax(distance));
#Y_old = Y[0];

time = range(file_start_time, file_end_time);
f = open(f_name_write, "w");
tip_radius = np.empty(np.size(time)+file_start_time ,  dtype = float)
tip_velocity = np.empty(np.size(time)+file_start_time ,  dtype = float)

sigma_star = 0.0

for n in time:
    file_time = n;
    f_name = "OF_contour0." + str(file_time) + ".csv"
    file = open(f_name);
    data = pd.read_csv(f_name);
    #csvreader = csv.reader(file);
    #rint(n)
    
    X = np.array(data.loc[:,'Points:0']).squeeze()
    Y = np.array(data.loc[:,'Points:1']).squeeze()
    
    X0 = X[0];
    Y0 = Y[0];

    XL = X[-1];
    YL = Y[-1];

    #R = np.add(np.multiply(X-X0,X-X0), np.multiply(Y-Y0, Y - Y0));
    #R_ = np.add(np.multiply(X-XL,X-XL), np.multiply(Y-YL, Y - YL));
    R = np.add(np.multiply(X,X), np.multiply(Y, Y));
    #data['CL'] = R - R_;
    data['CL'] = R;

    data = data.sort_values(by='CL');

    X = np.array(data.loc[:,'Points:0']).squeeze()
    Y = np.array(data.loc[:,'Points:1']).squeeze()

    distance = np.add(np.multiply(X,X),np.multiply(Y,Y));
    
    #d = math.sqrt(np.amax(X));
    d = math.sqrt(np.amax(distance));
    index = np.argmax(distance);

    X_ = X[index-20:index+20];
    Y_ = Y[index-20:index+20];

    p_tip = np.polyfit(X_,Y_,2);

   

    d2ydx2 = np.polyder(p_tip,2);
    dydx   = np.polyder(p_tip,1);

    p      =  np.poly1d(d2ydx2);
    
    r_tip = p(X[index]);
   
    r_tip = -1.0/r_tip;
    print(r_tip)
    tip_radius[n] = r_tip
    t = t + writeInterval;
    
    V = (d - d_old)/(writeInterval);
    tip_velocity[n] = V

    if (V !=0):
        sigma_star = (2*d_0*D/(r_tip*r_tip*V));
 
    
    s = str(t) + str(' ') + str(r_tip) + str(' ') + str(sigma_star) + str(' ') + str(V) 
    f.write(s + "\n") 
    
    d_old = d;



#tip_radius

plt.scatter(time[1:] , tip_radius[(file_start_time+1):])
plt.show()
#plt.scatter(np.arange(1, len(tip_velocity)) , tip_velocity[1:])
plt.scatter(time[1:], tip_velocity[(file_start_time+1):])
plt.show()
#plt.scatter(np.arange(2, 170) , tip_radius[2:170])


