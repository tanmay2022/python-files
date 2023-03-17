# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 09:47:45 2020

@author: Tanmay
"""

import numpy as np
import matplotlib.pyplot as plt

node = np.loadtxt('node.dat', delimiter = None, unpack = True)

ElemConn = np.loadtxt('ElemConn.dat', dtype = np.int_, delimiter = None, unpack = True)

node = np.transpose(node)
ElemConn = np.transpose(ElemConn)

#tol = 1e-04
nen = len(node[:,1]) # number of total nodes
ndm = len(node[1,:])-1 # number of dimension

nelem = len(ElemConn[:,1]) # number of elements
nel = len(ElemConn[1,:])-1 # number of nodes within each element

mtx = np.zeros((nen,nen)) # initializing bandwidth matrix

for i in range(0,nen): # each node
    for j in range(0,nelem): # from element list
        for k in range(1,nel+1): # connected to other nodes
            if ElemConn[j,k] == i+1: # node i found in element j
                mtx[i,ElemConn[j,k]-1] = 1
                if (k > 1) and (k < nel):
                    mtx[i,ElemConn[j,k-1]-1] = 1
                    mtx[i,ElemConn[j,k+1]-1] = 1
                elif (k == 1): # 1st node of an element
                    mtx[i,ElemConn[j,nel]-1] = 1
                    mtx[i,ElemConn[j,k+1]-1] = 1
                elif (k == nel): # last node of an element
                    mtx[i,ElemConn[j,k-1]-1] = 1
                    mtx[i,ElemConn[j,1]-1] = 1

plt.matshow(mtx)
plt.show()

mat = np.ones(nelem)*2 # initializing material index

cntd = 0 # number of dendrite elements
cntc = 0 # number of outside elements

# writing reformatted connectivities with material index
with open('ElemConn_New.dat', 'w') as f1:
    for i in range(0,nelem):
        if  (ElemConn[i,0] > 0) and (ElemConn[i,0] < 3037): #Dendrite
            mat[i] = 1
            cntd = cntd+1
        elif  (ElemConn[i,0] > 6897) and (ElemConn[i,0] < 7603): #outside
            mat[i] = 3
            cntc = cntc+1
        f1.write(f"{ElemConn[i,0]:5d}")
        f1.write(f"{int(mat[i]):5d}")
        for j in range(1,nel+1):
            f1.write(f"{ElemConn[i,j]:5d}")
        f1.write("\n")
    
cntb = nelem-cntd-cntc # number of BMG elements

# writing reformatted node coordinates
with open('node_data.dat', 'w') as f2:
    for i in range(0,nen):
        f2.write(f"{int(node[i,0]):5d}")
        f2.write(f"{0:5d}")
        for j in range(1,ndm+1):
            f2.write(f"{node[i,j]:10.4f}")
        f2.write("\n")
    
# writing to tecplot file for visulalization
with open('vis.tec', 'w') as f3:
    f3.write("TITLE = \" coord \"\n")
    f3.write(" VARIABLES = X Y\n")
    if (cntd != 0):
        f3.write(f" ZONE T = \"ZONE ONE\", I = {nen:d}, J = {cntd:d}, F = FEPOINT, C = RED\n")
        for i in range(0,nen):
            for j in range(1,ndm+1):
                f3.write(f"{node[i,j]:13.5E}")
            f3.write("\n")
        for i in range(0,nelem):
            if (mat[i] == 1):
                for j in range(1,nel+1):
                    f3.write(f"{ElemConn[i,j]:5d}")
                f3.write("\n") # dendrites

    if (cntb != 0):
        f3.write(f" ZONE T = \"ZONE TWO\", I = {nen:d}, J = {cntb:d}, F = FEPOINT, C = BLACK\n")
        for i in range(0,nen):
            for j in range(1,ndm+1):
                f3.write(f"{node[i,j]:13.5E}")
            f3.write("\n")
        for i in range(0,nelem):
            if (mat[i] == 2):
                for j in range(1,nel+1):
                    f3.write(f"{ElemConn[i,j]:5d}")
                f3.write("\n") # BMG

    if (cntc != 0):
        f3.write(f" ZONE T = \"ZONE THREE\", I = {nen:d}, J = {cntc:d}, F = FEPOINT, C = BLUE\n")
        for i in range(0,nen):
            for j in range(1,ndm+1):
                f3.write(f"{node[i,j]:13.5E}")
            f3.write("\n")
        for i in range(0,nelem):
            if (mat[i] == 3):
                for j in range(1,nel+1):
                    f3.write(f"{ElemConn[i,j]:5d}")
                f3.write("\n") # outside
