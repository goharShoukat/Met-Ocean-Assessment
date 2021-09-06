#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 18:54:00 2021

@author: goharshoukat
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams.update(mpl.rcParamsDefault)

x = np.random.rand(1,100)
y = x**2/3

plt.figure()
plt.scatter(x, y)

#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()
plt.title('try')
plt.tight_layout()
plt.show()
plt.savefig('test.pdf')
plt.close()