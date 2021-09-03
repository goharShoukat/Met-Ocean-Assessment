#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 23:36:26 2021

@author: goharshoukat
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import src.scikit.skextremes as ske
direc = 'tests/results/'
df = pd.read_csv(direc + '08_29-02_09_PM.csv', index_col = False)
df['Date'] = pd.to_datetime(df["Date"])



thresh = np.max(df['swh (m)'])
sort = df[df['swh (m)'] > 9]
model = ske.models.classic.GEV(sort['swh (m)'], fit_method = 'mle', ci = 0.05,
                              ci_method = 'delta')
model.plot_summary()
plt.show()


x = model.plot_return_values()
