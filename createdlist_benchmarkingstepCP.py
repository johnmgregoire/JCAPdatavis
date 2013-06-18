import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

homefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking'

subfold_sample_fnstartl_vshl=[\
    ('NiFeCoCe50301703/stepCP', 170, ['complete02', 'complete03', 'complete04'], [-0.1813, -0.1818, -0.1838]), \
    ('NiFeCoCe40202020/stepCP', 725, ['complete02', 'complete03', 'complete04'], [-0.17705, -0.17905, -0.18255]), \
    ('NiFeCoCe30072043/stepCP', 1326, ['complete02', 'complete03', 'complete04'], [-0.17605, -0.1788, -0.18005]), \
    ]

savep=os.path.join(homefolder, 'benchmarkingstepCPs_dlist.pck')

dlist=[]
for subfold, sample, fnstartl, vshl in subfold_sample_fnstartl_vshl:
    d={}
    d['Sample']=sample
    fold=os.path.join(homefolder, subfold)
    fns=os.listdir(fold)
    pl=[[os.path.join(fold, fn) for fn in fns if fn.startswith(fnstart)][0] for fnstart in fnstartl]
    for p, fnstart, vsh in zip(pl, fnstartl, vshl):
        d[fnstart]={}
        
        f=open(p, mode='r')
        f.readline()
        f.readline()
        dr=csv.DictReader(f, delimiter='\t')

        for l in dr:
            for kr in l.keys():
                k=kr.strip()
                if k in ['Unknown']:
                    continue
                if not k in d[fnstart].keys():
                    d[fnstart][k]=[]
                d[fnstart][k]+=[myeval(l[kr].strip())]
        for k in d[fnstart].keys():
            d[fnstart][k]=numpy.array(d[fnstart][k])
        f.close()
        try:
            x=d[fnstart]['I/mA']/.196
        except:
            x=d[fnstart]['<I>/mA']/.196
        try:
            y=d[fnstart]['Ewe/V']+vsh
        except:
            y=d[fnstart]['<Ewe>/V']+vsh
        indsl=[i*300-numpy.arange(50)-5 for i in range(4, 9)]
        xv=numpy.array([x[inds].mean() for inds in indsl])
        yv=numpy.array([y[inds].mean() for inds in indsl])
        iv=numpy.array([inds.mean() for inds in indsl])
        pylab.figure()
        pylab.plot(x, 'b-')
        pylab.plot(iv, xv, 'bo')
        pylab.twinx()
        pylab.plot(y, 'g-')
        pylab.plot(iv, yv, 'go')
        pylab.title(subfold+fnstart)
        d[fnstart]['I(mAcm2)']=xv
        d[fnstart]['Ewe(VOER)']=yv
        
    dlist+=[d]

#pylab.show()
if 1:
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()
    
