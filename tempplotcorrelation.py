import matplotlib.cm as cm
import numpy
import pylab
import h5py, operator, copy, os, csv
from echem_plate_math import *

#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results')
#dpl=['2012-9_FeCoNiTi_500C_fastCV_plate1_dlist.dat_V_IthreshCVLinSub.txt', '2012-9_FeCoNiTi_500C_fastCP_plate1_CP1Ess.txt']
#fomlabell=['V to reach 1E-4 A in CV (V vs H$_2$0/O$_2$)','V from CP at 1E-4 A (V vs H$_2$0/O$_2$)']
#fomshiftl=[-.2, -.24]
#fommult=1.
#expstrl=['V_IthreshCVLinSub','CP1Ess']

os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results')
dpl=['plate1_V_IthreshCVLinSub.txt', 'plate1_CP1Efin.txt']
fomlabell=['V to reach 1E-4 A in CV (V vs H$_2$0/O$_2$)','V from CP at 1E-4 A (V vs H$_2$0/O$_2$)']
fomshiftl=[-.177, -.177]
fommult=1.
expstrl=['V_IthreshCVLinSub','CP1Efin']

dropdl=[]
for dp in dpl:
    if dp=='':
        dropdl+=[None]
        continue
    f=open(dp, mode='r')
    dr=csv.DictReader(f, delimiter='\t')
    dropd={}
    for l in dr:
        for kr in l.keys():
            k=kr.strip()
            if not k in dropd.keys():
                dropd[k]=[]
            dropd[k]+=[myeval(l[kr].strip())]
    for k in dropd.keys():
        dropd[k]=numpy.array(dropd[k])
    f.close()
    dropdl+=[dropd]
foml=[]
smpl=[]
for count, (dropd, fomshift, expstr) in enumerate(zip(dropdl, fomshiftl, expstrl)):
    if dropd is None:
        continue
    print dropd.keys()
    #dropinds=numpy.arange(len(dropd['Sample']))
    dropinds=numpy.argsort(dropd['Sample'])
    dropinds=dropinds[numpy.logical_not(numpy.isnan(dropd[expstr][dropinds]))]
    x=dropd['x(mm)'][dropinds]
    y=dropd['y(mm)'][dropinds]

    fom=(dropd[expstr][dropinds]+fomshift)*fommult
    foml+=[fom]
    smpl+=[dropd['Sample'][dropinds]]


smp=list(set(smpl[0]).intersection(set(smpl[1])))
smp.sort()
fom0=numpy.array([foml[0][smpl[0]==i][0] for i in smp])
fom1=numpy.array([foml[1][smpl[1]==i][0] for i in smp])

fitdy, fitint=numpy.polyfit(fom0, fom1, 1)
fitx=numpy.array([fom0.min(), fom0.max()])
fity=fitint+fitdy*fitx

pylab.plot(fom0, fom1, 'b.')
pylab.plot(fitx, fity, 'r-')
pylab.xlabel(fomlabell[0])
pylab.ylabel(fomlabell[1])
pylab.title('CP=CV*%.3f+%.3f' %(fitdy, fitint))

pylab.show()
