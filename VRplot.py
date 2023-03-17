# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:48:47 2020

@author: Tanmay
"""

import os.path
import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(6,4))
#plt.axis([0, 2.8, 0, 8e-7])
plt.axis([0, 0.03, 0, 1.4e-7])


# plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
# params = {'text.usetex' : True,
#           'font.size' : 14,
#           'font.family' : 'lmodern',
#           'text.latex.unicode' : True,
#           }
# plt.rcParams.update(params)

dT = 13

file_name = ["f_2_velocity_Tm_870_dT_"+str(dT)+"_pravega_mod_guess.dat",
      "f_3_velocity_Tm_870_dT_"+str(dT)+"_solver_pravega_mod_guess.dat",
      "f_4_velocity_Tm_870_dT_"+str(dT)+"_solver_pravega_mod_guess.dat",
      "AlZn_Tm870_dT_"+str(dT)+"_OpenFoam.dat",
      "AlZn_Tm870_dT_"+str(dT)+"_amrex.dat",
      "VR_Input_KKS_github_tdb_und_"+str(dT)+"K_F2.dat",
      "VR_Input_KKS_github_tdb_und_"+str(dT)+"K_F3.dat",
      "VR_Input_KKS_github_tdb_und_"+str(dT)+"K_F4.dat",
      "CUDA_AlZn_und_"+str(dT)+"K_F02_VR.dat",
      "CUDA_AlZn_und_"+str(dT)+"K_F03_VR.dat",
      "CUDA_AlZn_und_"+str(dT)+"K_F04_VR.dat"]

legn = ["GP:CPU Function_F = 2", "GP:CPU Function_F = 3", "GP:CPU Function_F = 4", 
        "GP:OpenFOAM Function_F = 4", "GP:AMReX Function_F = 4",
        "KKS:OpenCL Function_F = 2", "KKS:OpenCL Function_F = 3", "KKS:OpenCL Function_F = 4",
        "KKS:CUDA Function_F = 2", "KKS:CUDA Function_F = 3", "KKS:CUDA Function_F = 4"] #
fmt = ["sb", "sr", "sk", "*k", "xk", "ob", "or", "ok", "^b", "^r", "^k"]


for kk in range(0,3):
    path = os.path.join("/media/tanmay/3e0c1b97-4353-4fae-88a4-e97b9d433879/tanmay/Downloads/2023_microsim_tdb_paper/VR_plot_datfiles/", file_name[kk])
    f1 = np.genfromtxt(path, delimiter = None)#, unpack = True)

    t = f1[:,0]
    v = f1[:,2]
    plt.plot(t, v, fmt[kk], markerfacecolor='none', label = legn[kk], linewidth = 1.5, markersize = 4)


for kk in range(3,len(file_name)):
    path = os.path.join("/media/tanmay/3e0c1b97-4353-4fae-88a4-e97b9d433879/tanmay/Downloads/2023_microsim_tdb_paper/VR_plot_datfiles/", file_name[kk])
    f1 = np.genfromtxt(path, delimiter = None)#, unpack = True)
    
    t = f1[:,0]
    v = f1[:,1]
    plt.plot(t, v, fmt[kk], markerfacecolor='none', label = legn[kk], linewidth = 1.5, markersize = 4)

plt.xlabel('Time (s)')
#plt.ylabel('Dendrite tip velocity (m/s)')
plt.ylabel('Dendrite tip radius (m)')
plt.legend()
plt.savefig('dT'+str(dT)+'_R.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show()