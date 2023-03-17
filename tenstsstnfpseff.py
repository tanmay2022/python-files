# -*- coding: utf-8 -*-
"""
Created on Thu May  7 10:17:38 2020

@author: Tanmay
"""

import os.path
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
plt.figure(figsize=(5,4))
plt.axis([0, 0.12, 0, 2.1])

plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
params = {'text.usetex' : True,
          'font.size' : 14,
          'font.family' : 'lmodern',
          'text.latex.unicode' : True,
          }
plt.rcParams.update(params)

L0 = 2.0 #lenth
c0 = 1.e3 #initial cohesion
srt = 1.e-2 #srain rate
num = 3 # repeats
st = ["D:\\docs\\feap\\Source ss rt BMGC\\BMGC ss rt patch\\pls ten N 0.3 V 0\\",
      "D:\\docs\\feap\\Source ss rt BMGC\\BMGC ss rt patch\\pls ten N 0.3 V 30\\",
      "D:\\docs\\feap\\Source ss rt BMGC\\BMGC ss rt patch\\pls ten N 0.3 V 45\\",
      "D:\\docs\\feap\\Source ss rt BMGC\\BMGC ss rt patch\\pls ten N 0.3 V 100\\"]
legn = ["$V_f$ = 0\% (BMG)", "$V_f$ = 30\% (BMGC)", "$V_f$ = 45\% (BMGC)", 
        "$V_f$ = 100\% (Dendrite)"] #
fmt = ["-b", "-.r", "--k", ":m"]
failpt = np.zeros([len(st),2])
mod = np.zeros(len(st))

for kk in range(0,len(st)):
    path = os.path.join(st[kk], "fpseff.dat")
    f1 = np.genfromtxt(path, delimiter = None)#, unpack = True)
    p = len(f1[:,1])
    q = len(f1[1,:])
    dim = int(p+1) # dimension of E2 & S2 arrays
    E2 = np.zeros(dim)
    S2 = np.zeros(dim)
    for ii in range(0,dim-1):
        E2[ii+1] = f1[ii,1]/L0
        S2[ii+1] = f1[ii,3]/f1[ii,5]
    
    S2 = S2/c0
    S2 = savgol_filter(S2, 11, 3)
    failpt[kk,0] = E2[-1]
    failpt[kk,1] = S2[-1]
    E2l = np.log(1+E2)
    mod[kk] = S2[5]/E2[5]
    plt.plot(E2l, S2, fmt[kk], label = legn[kk], linewidth = 1.5, markersize = 4)

#plt.plot(failpt[0,0], failpt[0,1], 'xb', linewidth = 1.5, markersize = 6)
plt.xlabel('ln$(1+\Delta/L_0)$')
plt.ylabel('$\overline{\sigma}_{22}/c_0$')
#plt.title('A tale of 2 subplots')
#plt.ticklabel_format(axis = {'both'}, style = {'plain'})
plt.legend()
plt.savefig('sstenstrue.png', format='png', dpi=1000, bbox_inches = "tight")
plt.show()