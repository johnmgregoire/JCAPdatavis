import pylab 
import numpy
import h5py
import os, os.path, time, copy
import struct
from scipy.optimize import leastsq

folder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120925_NiFe_CXbiologictest/npy'

dl1=[]
dl2=[]
dl3=[]
fkey1='120925-FeNi 5050 plate1capacitive '
fkey2='120925-FeNi 5050 plate1 CV scan '
fkey3='120925-Fe100%-'

for fn in os.listdir(folder):
    
    d={}
    arr=numpy.load(os.path.join(folder, fn))
    print fn, arr.shape
    for ind, k in zip((0, 1, 2), ['t(s)', 'Ewe(V)', 'I(A)']):
        d[k]=arr[ind]
    d['I(A)']/=1000.
    if fkey1 in fn:
        a, b, c=fn.partition(fkey1)
        s=c.partition('mV')[0].strip()
        n=eval(s)
        d['scanrate']=n
        dl1+=[d]
    if fkey2 in fn:
        a, b, c=fn.partition(fkey2)
        s=c.partition('mV')[0].strip()
        n=eval(s)
        d['scanrate']=n
        dl2+=[d]
    if fkey3 in fn:
        a, b, c=fn.partition(fkey3)
        s=c.partition('mV')[0].strip()
        n=eval(s)
        d['scanrate']=n
        dl3+=[d]
pylab.figure()
for d in dl1:
    pylab.plot(d['Ewe(V)'], d['I(A)'])
pylab.figure()
for d in dl2:
    pylab.plot(d['Ewe(V)'], d['I(A)'])
pylab.figure()
for d in dl3:
    pylab.plot(d['Ewe(V)'], d['I(A)'])
pylab.show()
print 'done'
