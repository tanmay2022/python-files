# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:48:47 2020

@author: Tanmay
"""

import numpy as np
import matplotlib.pyplot as plt
plt.figure(figsize=(5,4))
plt.axis([0, 2800.0, 0, 9.0])

plt.rcParams['text.latex.preamble']=[r"\usepackage{lmodern}"]
params = {'text.usetex' : True,
          'font.size' : 14,
          'font.family' : 'lmodern',
          'text.latex.unicode' : True,
          }
plt.rcParams.update(params)

nu = 0.4
v = 0.45
E = 60*v+100*(1-v)
t = np.linspace(0.0, 2800.0, num = 15)
K1 = t*64/6000
J = (1-nu**2)*K1**2/E
Jint = np.array([0, 5.4e-2, 0.18, 0.45, 0.78, 1.15, 1.72, 2.25, 2.87, 3.67,
                 4.45, 5.3, 6.4, 7.13, 8.37])

plt.plot(t, J, '-b', label = 'Elastic', linewidth = 1.5, markersize = 4)
plt.plot(t, Jint, 'or', label = 'Contour', linewidth = 1.5, markersize = 4)
plt.xlabel('time')
plt.ylabel('$J/(c_ob_o)$')
plt.legend()
plt.show()