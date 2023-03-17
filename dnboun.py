# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 21:00:45 2019

@author: Tanmay
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
params = {'text.usetex' : True,
          'font.size' : 14,
          'font.family' : 'lmodern',
          'text.latex.unicode' : True,
          }
plt.rcParams.update(params)

toll = 0.005
r = 12.0
cntr1 = np.array([-4.0, 48.0])
cntr2 = np.array([52.0, 48.0]) # cntr1x+cntr2x=48
node = np.loadtxt('node_data.dat')
print(node)
num = len(node[:,1])
tmp = len(node[1,:])
xlim1 = 0.0
xlim2 = 48.0
ylim1 = 0.0
ylim2 = 96.0
nB = np.zeros(3) # nodes on bottom
nR = np.zeros(3) # nodes on ride side
nT = np.zeros(3) # nodes on top
nL = np.zeros(3) # nodes on left
# 1st notch
nN1 = np.zeros(2)
#nNT1 = np.zeros(3)
#nNB1 = np.zeros(3)
# 2nd notch
#nNT2 = np.zeros(3)
#nNB2 = np.zeros(3)
nN2 = np.zeros(2)

nd_bdry = np.array([])
bdry2 = np.array([])
bdry3 = np.array([])
bdry4 = np.array([])
bdry5 = np.array([])

for i in range(0,num):
    if (abs(node[i,2]-ylim1) < 0.0001):
        nB = np.vstack((nB,node[i,:]))
    if (abs(node[i,2]-ylim2) < 0.0001):
        nT = np.vstack((nT,node[i,:]))
    if (abs(node[i,1]-xlim1) < 0.0001):
        nL = np.vstack((nL,node[i,:]))
    if (abs(node[i,1]-xlim2) < 0.0001):
        nR = np.vstack((nR,node[i,:]))
#    get distance of current node from the center of first notch 
    xx1 = np.float64(node[i,1] - cntr1[0])
    yy1 = np.float64(node[i,2] - cntr1[1])
    dd = xx1*xx1 + yy1*yy1
    r_c1 = np.sqrt(dd)
#     get distance of current node from the center of 2nd notch
    xx2 = np.float64(node[i,1] - cntr2[0])
    yy2 = np.float64(node[i,2] - cntr2[1])
    dd = xx2*xx2 + yy2*yy2
    r_c2 = np.sqrt(dd)
    if (r_c1 < (r+toll)):
        theta = np.arctan2(yy1,xx1)*180.0/np.pi
        nN1 = np.vstack((nN1,np.array([i+1, theta])))
    elif (r_c2 < (r+toll)):
        theta = np.arctan2(yy2,xx2)*180.0/np.pi
        if (theta < 0):
            theta = 360.0 + theta
        nN2 = np.vstack((nN2,np.array([i+1, theta])))

nB = nB[1:len(nB),:]
id1 = -np.sort(-nB[:,1]) # nodes on bottom
for i in range(0,len(id1)):
    for j in range(0,len(nB[:,0])):
        if (id1[i] == nB[j,1]):
            nd_bdry = np.concatenate((nd_bdry,nB[j,0]), axis = None)

nN1 = nN1[1:len(nN1),:]
id2 = np.sort(nN1[:,1]) # 1st notch
for i in range(0,len(id2)):
    for j in range(0,len(nN1[:,0])):
        if (id2[i] == nN1[j,1]):
            bdry4 = np.concatenate((bdry4,nN1[j,0]), axis = None)

nL = nL[1:len(nL),:]
flag = 0
id3 = np.sort(nL[:,2]) # nodes on left
for i in range(0,len(id3)-1):
    for j in range(0,len(nL[:,0])):
        if (id3[i] == nL[j,2]):
            if (nL[j,0] == bdry4[0]): # nodes around notch
                    bdry5 = np.concatenate((bdry5,bdry4[0:len(bdry4)-1]), axis = None)
                    flag = 1
            elif (flag == 0): # nodes below notch
                bdry5 = np.concatenate((bdry5,nL[j,0]), axis = None)
            else: # nodes above notch
                bdry5 = np.concatenate((bdry5,nL[j,0]), axis = None)

nd_bdry = np.concatenate((nd_bdry,bdry5[1:len(bdry5)]), axis = None)

nT = nT[1:len(nT),:]
id4 = np.sort(nT[:,1]) # nodes on top
for i in range(0,len(id4)):
    for j in range(0,len(nT[:,0])):
        if (id4[i] == nT[j,1]):
            nd_bdry = np.concatenate((nd_bdry,nT[j,0]), axis = None)

nN2 = nN2[1:len(nN2),:]
id5 = np.sort(nN2[:,1]) # 2nd notch
for i in range(0,len(id5)):
    for j in range(0,len(nN2[:,0])):
        if (id5[i] == nN2[j,1]):
            bdry2 = np.concatenate((bdry2,nN2[j,0]), axis = None)

nR = nR[1:len(nR),:]
flag = 0
id6 = -np.sort(-nR[:,2]) # nodes on right
for i in range(0,len(id6)-1):
    for j in range(0,len(nR[:,0])):
        if (id6[i] == nR[j,2]):
            if (nR[j,0] == bdry2[0]): # nodes around notch
                bdry3 = np.concatenate((bdry3,bdry2[0:len(bdry2)-1]), axis = None)
                flag = 1
            elif (flag == 0): # nodes below notch
                bdry3 = np.concatenate((bdry3,nR[j,0]), axis = None)
            else: # nodes above notch
                bdry3 = np.concatenate((bdry3,nR[j,0]), axis = None)

nd_bdry = np.concatenate((nd_bdry,bdry3[1:len(bdry3)]), axis = None)

plt.figure(figsize=(2,4))
plt.axis([xlim1, xlim2, ylim1, ylim2])

with open('BOUNNODES.DAT','w') as f1:
    f1.write(f"{1:d}")
    f1.write(f"{len(nd_bdry):5d}\n")
    cnt = 0
    for i in range(0,len(nd_bdry)):
        f1.write(f"{int(nd_bdry[i]):5d}")
        cnt = cnt + 1
        if (cnt == 16):
            f1.write("\n")
            cnt = 0
        plt.plot(node[int(nd_bdry[i])-1,1], node[int(nd_bdry[i])-1,2], 'r*', markersize = 4)

plt.xlabel('X')
plt.ylabel('Y')
plt.savefig('testboun.svg', format='svg', dpi=600)
plt.show()