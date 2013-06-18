import numpy, scipy
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from echem_plate_math import *
import time, pickle
from echem_plate_fcns import *


p='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835/Sample4825_x60_y65_A33B23C3D40_FCVS7.txt'
p2='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835/Sample4825_x60_y65_A33B23C3D40_FCVS8.txt'
#p2=''
vrange=(-.19, -.14)


d=readechemtxt(p)

if p2!='':
    d2=readechemtxt(p2)
    for k, v in d2.iteritems():
        d[k]=numpy.append(d[k], v)
    
vraw=d['Ewe(V)']
iraw=d['I(A)']

pylab.plot(d['Ewe(V)'], d['I(A)'])
#pylab.show()


vrbool=(vraw>=vrange[0])&(vraw<=vrange[1])

testlen=4
vrboolmean=numpy.array([vrbool[i:i+testlen].mean(dtype='float32')>.5 for i in range(len(vrbool)-testlen//2)])

vrboolapproxinds=numpy.where(numpy.logical_not(vrboolmean[:-1])&(vrboolmean[1:]))[0]+testlen//2
vrboolnoisyinds=numpy.where(numpy.logical_not(vrbool[:-1])&(vrbool[1:]))[0]
vstartinds_seg=vrboolnoisyinds[numpy.array([numpy.argmin((vrboolnoisyinds-i)**2) for i in vrboolapproxinds])]

vlen_seg=[]
for i, j in zip(vstartinds_seg, numpy.concatenate([vstartinds_seg[1:], [-1]])):
    print len(vrboolmean), i, j, j-testlen
    vlen_seg+=[numpy.where(vrboolmean[i:j-testlen])[0][-1]+testlen//2]

pylab.figure()
segdl=[]
for vsi, vlen in zip(vstartinds_seg, vlen_seg):
    segd={}
    for k in ['Ewe(V)','I(A)', 't(s)']:
        segd[k]=d[k][vsi:vsi+vlen]
    v=segd['Ewe(V)']
    i=segd['I(A)']
    t=segd['t(s)']
    ans=scipy.polyfit(v, i, 1)
    segd['I_Efit']=scipy.polyval(ans, v)
    segd['I_Efitfitpars']=ans

    ans=scipy.polyfit(t, v, 1)
    segd['E_tfit']=scipy.polyval(ans, t)
    segd['E_tfitfitpars']=ans
    
    segdl+=[segd]
    pylab.plot(segd['Ewe(V)'], segd['I(A)'])
    pylab.plot(segd['Ewe(V)'], segd['I_Efit'])

dEdt=numpy.array([sd['E_tfitfitpars'][0] for sd in segdl])
dIdE=numpy.array([sd['I_Efitfitpars'][0] for sd in segdl])
C=numpy.array([numpy.trapz(sd['I_Efitfitpars'], x=sd['t(s)']) for sd in segdl])

inds=numpy.arange(0, len(segdl), 2)

dEdtmean=(numpy.abs(dEdt[inds])+numpy.abs(dEdt[inds+1]))/2.
dC=C[inds]-C[inds+1]

vtest=numpy.array(vrange).mean()

itestarr=numpy.array([scipy.polyval(sd['I_Efitfitpars'], vtest) for sd in segdl])
delI=itestarr[inds]-itestarr[inds+1]

#pylab.figure()
#pylab.plot(dEdtmean, dC*1.e6, 'o')
#pylab.ylabel('differentialcharge (microC)')
#pylab.xlabel('ave scan rate (V/s)')

pylab.figure()
dIdtplot=dIdE*dEdt*1.e6
pylab.plot(dIdtplot[inds], 'bo', label='fwd')
pylab.plot(numpy.abs(dIdtplot[inds+1]), 'go', label='rev')
pylab.ylabel('dI/dt (microA/s)')
pylab.xlabel('CV number')
pylab.legend(loc=2)

pylab.figure()
pylab.plot(dEdtmean, delI*1.e6, 'o')
pylab.ylabel('capacitive current ($\mu$A)')
pylab.xlabel('ave scan rate (V/s)')

CC_dEdtfitpars=scipy.polyfit(dEdtmean, delI, 1)
lims=numpy.array([0, dEdtmean.max()])
fitvals=scipy.polyval(CC_dEdtfitpars, lims)
    
pylab.plot(lims, fitvals*1.e6, 'r-')
pylab.title('%.2e $\mu$C/V +%.2e $\mu$A' %(CC_dEdtfitpars[0]*1.e6, CC_dEdtfitpars[1]*1.e6))

pylab.show()
