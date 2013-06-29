import pickle
import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *


p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/20130628NiFeCoCe_plate1_selectCVs_6220/results/data_dlist.dat'
vsh=-(.187-.055)
f=open(p, mode='r')
dlist=pickle.load(f)
f.close()

s_lab=[(2077, 'c1 50mV/s'), (2076, 'c1 250mV/s'), (2075, 'c1 10mV/s'), (2063, 'c2 50mV/s'), (2062, 'c2 250mV/s'), (2061, 'c2 10mV/s'), (1992, 'FTO 50mV/s')]

allsamples=[d['Sample'] for d in dlist]

il=[allsamples.index(s) for s, l in s_lab]

for count, (i, (s, l)) in enumerate(zip(il, s_lab)):
    d=dlist[i]
    ind=d['segprops_dlist'][2]['inds'][d['segprops_dlist'][2]['npts']//2]
    x=d['Ewe(V)'][ind:]+vsh
    y=d['I(A)'][ind:]*1.e5
    pylab.plot(x, y, label=l)
pylab.legend(loc=2)
pylab.show()
