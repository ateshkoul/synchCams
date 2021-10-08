# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 17:31:36 2021

@author: Atesh
"""

import sys
sys.path.insert(0,"E:\\Libraries\\")
from synchCams.synchCams import synchCams
exp = synchCams([0,1])
exp.start_experiment()
exp.releaseCams()