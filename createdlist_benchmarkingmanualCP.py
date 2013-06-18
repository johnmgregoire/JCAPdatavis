import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

homefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking'

sample_fnstartl_vl=[\
    (170, ['complete02', 'complete03', 'complete04'], [0.364, 0.372, 0.385]), \
    (725, ['complete02', 'complete03', 'complete04'], [0.381, 0.361, 0.396]), \
    (1326, ['complete02', 'complete03', 'complete04'], [0.361, 0.403, 0.373]), \
    ]



savep=os.path.join(homefolder, 'benchmarking2hrCP_dlist.pck')

dlist=[]
for sample, fnstartl, vl in sample_fnstartl_vl:
    d={}
    d['Sample']=sample

    for fnstart, v in zip(fnstartl, vl):
        d[fnstart]={}
        d[fnstart]['I(mAcm2)']=10.
        d[fnstart]['Ewe(VOER)']=v
        
    dlist+=[d]

#pylab.show()
if 1:
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()
    
