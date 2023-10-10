# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:48:47 2020

@author: Tanmay
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plt
#plt.figure(figsize=(5,5))
#plt.axis([0, 1e-5, 0, 1e-5])
#plt.figure(figsize=(5,5))
#plt.axis([0, 5e-5, 0, 5e-5])


# plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
# params = {'text.usetex' : True,
#           'font.size' : 14,
#           'font.family' : 'lmodern',
#           'text.latex.unicode' : True,
#           }
# plt.rcParams.update(params)

cuda_scaling_data_2D = pd.read_csv("MicroSim_KKS_FD_CUDA_MPI_Scaling.csv", index_col=0)
cuda_scaling_data_3D = pd.read_csv("MicroSim_KKS_FD_CUDA_MPI_Scaling_3D.csv", index_col=0)

ax = cuda_scaling_data_2D["Wall Time (s)"].plot(kind="bar")

ax.bar_label(ax.containers[0], label_type='edge')

axes = plt.gca()

axes.set_axisbelow(True)

axes.yaxis.grid()

plt.xticks(rotation='horizontal')

plt.xlabel('Number of GPUs')
plt.ylabel('Execution time (s)')

plt.savefig('CUDA_scaling_2D.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show()

######################################

ax = cuda_scaling_data_3D["Wall Time (s)"].plot(kind="bar")

ax.bar_label(ax.containers[0], label_type='edge')

axes = plt.gca()

axes.set_axisbelow(True)

axes.yaxis.grid()

plt.xticks(rotation='horizontal')

plt.xlabel('Number of GPUs')
plt.ylabel('Execution time (s)')

plt.savefig('CUDA_scaling_3D.pdf', format='pdf', dpi=1000, bbox_inches = "tight")
plt.show()
