import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

homefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/yunsamples/'
sample_fnstartl_vshl=[\
    (1326, ['sample1cv'], [0.]), \
    ]



savep=os.path.join(homefolder, 'yunCV_dlist.pck')

dlist=[]
for sample, fnstartl, vshl in sample_fnstartl_vshl:
    d={}
    d['Sample']=sample
    fold=homefolder
    fns=os.listdir(fold)
    pl=[[os.path.join(fold, fn) for fn in fns if fn.startswith(fnstart)][0] for fnstart in fnstartl]
    for p, fnstart, vsh in zip(pl, fnstartl, vshl):
        d[fnstart]={}
        
        f=open(p, mode='r')

        dr=csv.DictReader(f, delimiter='\t')

        for l in dr:
            for kr in l.keys():
                k=kr.strip()
                if not k in d[fnstart].keys():
                    d[fnstart][k]=[]
                d[fnstart][k]+=[myeval(l[kr].strip())]
        for k in d[fnstart].keys():
            d[fnstart][k]=numpy.array(d[fnstart][k])
        f.close()
        y=d[fnstart]['I(mAcm2)']
        x=d[fnstart]['Ewe(VOER)']+vsh
        inds=numpy.where((x[1:]>x[:-1]) & ((x[1:]-x[:-1])<.01))
        x=x[inds]
        y=y[inds]
        inds=numpy.argsort(x)
        x=x[inds]
        y=y[inds]
        i=numpy.argmax(x)
        x=x[:i]
        y=y[:i]
        
        inds=numpy.where(x>-.1)
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
        pylab.title(fnstart)
        
    dlist+=[d]

pylab.show()

#pylab.show()
if 1:
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()
    
