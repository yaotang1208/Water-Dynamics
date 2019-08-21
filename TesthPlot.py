# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 14:46:31 2019

@author: yaotang
"""

import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import gridspec


delta = 0.025
x = np.arange(-3.0, 3.0, delta)
y = np.arange(-2.0, 2.0, delta)
X, Y = np.meshgrid(x, y)
Z = np.outer(np.cos(y), np.cos(3*x))

# Gridspec is now 2x2 with sharp width ratios
gs = gridspec.GridSpec(2,2,height_ratios=[4,1],width_ratios=[20,1])
fig = plt.figure()

cax = fig.add_subplot(gs[0])

CS = cax.contourf(X, Y, Z)
cax.plot([-3,3],[0,0],ls="--",c='k')

lax = fig.add_subplot(gs[2],sharex=cax)

lax.plot(x, np.cos(3*x))
lax.set_xlim([-3,3])

# Make a subplot for the colour bar
bax = fig.add_subplot(gs[1])

# Use general colour bar with specific axis given.
cbar = plt.colorbar(CS,bax)

plt.show()