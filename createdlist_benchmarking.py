import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

homefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking'

subfold_sample_fnstartl_vshl=[\
    ('NiFeCoCe50301703', 170, ['complete02', 'complete03', 'complete04'], [-0.1813, -0.1818, -0.1838]), \
    ('NiFeCoCe40202020', 725, ['complete02', 'complete03', 'complete04'], [-0.17705, -0.17905, -0.18255]), \
    ('NiFeCoCe30072043', 1326, ['complete02', 'complete03', 'complete04'], [-0.17605, -0.1788, -0.18005]), \
    ]

savep=os.path.join(homefolder, 'benchmarkingCVs_dlist.pck')

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
        y=d[fnstart]['<I>/mA']/.196
        x=d[fnstart]['Ewe/V']+vsh
        d[fnstart]['I(mAcm2)']=y
        d[fnstart]['Ewe(VOER)']=x
        i=numpy.argmax(x)
        x=x[:i]
        y=y[:i]
#        inds=numpy.where((x>.1)&(x<.15))
#        xi=x[inds]
#        yi=y[inds]
#        fitdy, fitint=numpy.polyfit(xi, yi, 1)
#        fitvals=numpy.polyval((fitdy, fitint), x)
#        ys=y-fitvals
        inds=numpy.where((x>.1))
        xi=x[inds]
        yi=y[inds]
        inds=numpy.argsort(yi)[:20]
        minval=yi[inds].mean()
        ys=y-minval
        pylab.figure()
        pylab.plot(x, y, 'g')
        #pylab.plot(x, fitvals, 'b')
        pylab.plot(x, ys, 'r')
        pylab.twinx()
        inds=numpy.where(ys>.1)
        yl=numpy.log10(ys[inds])
        xl=x[inds]
        pylab.plot(xl, yl)
        d[fnstart]['I(mAcm2)_LinSub']=ys
        d[fnstart]['Ewe(VOER)_LinSub']=x
        pylab.title(subfold+fnstart)
        
    dlist+=[d]

pylab.show()
if 0:
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()
    
