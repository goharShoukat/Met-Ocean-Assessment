#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 18:40:57 2021

@author: goharshoukat
"""

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.ERA5 import ERA5

directory = 'some_data/'
x = ERA5(directory)
cache = x.load_files('swh')
nearest = x.nearest_point(5, 6)
