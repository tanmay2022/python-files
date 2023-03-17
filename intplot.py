# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:48:47 2020

@author: Tanmay
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.axis([0, 1e-5, 0, 1e-5])
# plt.figure(figsize=(5,5))
# plt.axis([0, 5e-5, 0, 5e-5])


# plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
# params = {'text.usetex' : True,
#           'font.size' : 14,
#           'font.family' : 'lmodern',
#           'text.latex.unicode' : True,
#           }
# plt.rcParams.update(params)

dT = 13
dx = 1e-8
# dT = 4
# dx = 5e-8

file_name = ["GP_MPI_f2_dt"+str(dT)+"_70.csv",
      "GP_MPI_f3_dt"+str(dT)+"_70.csv",
      "GP_MPI_f4_dt"+str(dT)+"_70.csv",
      "OFAlZn"+str(dT)+"K_00126.csv",
      "amrex_"+str(dT)+"K_plt_14.csv",
      "KKS_"+str(dT)+"K_F2_700000.csv",
      "KKS_"+str(dT)+"K_F3_700000.csv",
      "KKS_"+str(dT)+"K_F4_700000.csv",
      "CUDA_AlZn_und_"+str(dT)+"K_F02_700000.csv",
      "CUDA_AlZn_und_"+str(dT)+"K_F03_700000.csv",
      "CUDA_AlZn_und_"+str(dT)+"K_F04_700000.csv"]

legn = ["GP:CPU Function_F = 2", "GP:CPU Function_F = 3", "GP:CPU Function_F = 4", 
        "GP:OpenFOAM Function_F = 4", "GP:AMReX Function_F = 4",
        "KKS:OpenCL Function_F = 2", "KKS:OpenCL Function_F = 3", "KKS:OpenCL Function_F = 4",
        "KKS:CUDA Function_F = 2", "KKS:CUDA Function_F = 3", "KKS:CUDA Function_F = 4"] #
fmt = ["sb", "sr", "sk", "*k", "xk", "ob", "or", "ok", "^b", "^r", "^k"]


for kk in range(0,3):
    data = pd.read_csv(file_name[kk])

    X = np.array(data.loc[:,'Points:1']).squeeze()*dx
    Y = np.array(data.loc[:,'Points:2']).squeeze()*dx
    plt.plot(X[0:-1:9], Y[0:-1:9], fmt[kk], markerfacecolor='none', label = legn[kk], linewidth = 1.5, markersize = 4)


for kk in range(3,len(file_name)):
    data = pd.read_csv(file_name[kk])
    
    X = np.array(data.loc[:,'Points:0']).squeeze()
    Y = np.array(data.loc[:,'Points:1']).squeeze()
    plt.plot(X[0:-1:9], Y[0:-1:9], fmt[kk], markerfacecolor='none', label = legn[kk], linewidth = 1.5, markersize = 4)

plt.xlabel('X (m)')
plt.ylabel('Y (m)')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.savefig('dt'+str(dT)+'_Contour.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show()