import numpy, scipy
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from echem_plate_math import *
import time, pickle
from echem_plate_fcns import *


p='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835/Sample4825_x60_y65_A33B23C3D40_FCVS7.txt'
p2='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835/Sample4825_x60_y65_A33B23C3D40_FCVS8.txt'
#p2=''
#vrange=(-.19, -.14)

def calccapacitivecurrent(pathlist, vscanrangefrac=(.15, .85), vendrangefrac=(.02, .98), vendtol=0.01, plotfignum=None, plotsavepath=None, returndict=False):
#use pathlist to send data files from multipls FCVS techniques
#vendrangefrac is used to test where the endpoints of the scan are located - should not need to be changed
# vendtol is the V difference between the test points and the usbale part of the scan

    if not plotfignum is None:
        pylab.figure(num=plotfignum)
        plotbool=True
    else:
        plotbool=False
    d=readechemtxt(pathlist[0])

    for p2 in pathlist[1:]:
        d2=readechemtxt(p2)
        for k, v in d2.iteritems():
            if isinstance(v, numpy.ndarray) and not k.startswith('comp'):
                d[k]=numpy.append(d[k], v)
        
    vraw=d['Ewe(V)']
    iraw=d['I(A)']

    if plotbool:
        ax1=pylab.subplot(221)
        pylab.plot(d['Ewe(V)'], d['I(A)'])
        #pylab.show()

    indsendarr=numpy.int32(len(vraw)*numpy.array(vendrangefrac))
    vendrange=vraw[numpy.argsort(vraw)[indsendarr]]
    vscanning=vraw[(vraw>=vendrange[0]+vendtol)&(vraw<=vendrange[1]-vendtol)]

    indsscanarr=numpy.int32(len(vscanning)*numpy.array(vscanrangefrac))
    vrange=vscanning[numpy.argsort(vscanning)[indsscanarr]]

    #pylab.plot(vrange, [iraw.min(), iraw.min()])
    #pylab.show()
    vrbool=(vraw>=vrange[0])&(vraw<=vrange[1])

    testlen=4
    vrboolmean=numpy.array([vrbool[i:i+testlen].mean(dtype='float32')>.5 for i in range(len(vrbool)-testlen//2)])

    vrboolapproxinds=numpy.where(numpy.logical_not(vrboolmean[:-1])&(vrboolmean[1:]))[0]+testlen//2
    vrboolnoisyinds=numpy.where(numpy.logical_not(vrbool[:-1])&(vrbool[1:]))[0]
    vstartinds_seg=vrboolnoisyinds[numpy.array([numpy.argmin((vrboolnoisyinds-i)**2) for i in vrboolapproxinds])]

    vlen_seg=[]
    for i, j in zip(vstartinds_seg, numpy.concatenate([vstartinds_seg[1:], [-1]])):
        #print len(vrboolmean), i, j, j-testlen
        vlen_seg+=[numpy.where(vrboolmean[i:j-testlen])[0][-1]+testlen//2]
    if plotbool:
        pylab.subplot(223)
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
        if plotbool:
            pylab.plot(segd['Ewe(V)'], segd['I(A)'])
            pylab.plot(segd['Ewe(V)'], segd['I_Efit'])
            
    d['vstartinds_seg']=vstartinds_seg
    d['vlen_seg']=vlen_seg
    
    if len(segdl)%2==1:
        print 'odd number of segments'
        raise
    dEdt=numpy.array([sd['E_tfitfitpars'][0] for sd in segdl])
    dIdE=numpy.array([sd['I_Efitfitpars'][0] for sd in segdl])
    C=numpy.array([numpy.trapz(sd['I_Efitfitpars'], x=sd['t(s)']) for sd in segdl])

    d['dEdt_seg']=dEdt
    d['dIdE_seg']=dIdE
    
    inds=numpy.arange(0, len(segdl), 2)

    dEdtmean=(numpy.abs(dEdt[inds])+numpy.abs(dEdt[inds+1]))/2.
    dC=C[inds]-C[inds+1]

    vtest=numpy.array(vrange).mean()

    itestarr=numpy.array([scipy.polyval(sd['I_Efitfitpars'], vtest) for sd in segdl])
    delI=itestarr[inds]-itestarr[inds+1]

    CC_dEdtfitpars=scipy.polyfit(dEdtmean, delI, 1)
    lims=numpy.array([0, dEdtmean.max()])
    fitlimvals=scipy.polyval(CC_dEdtfitpars, lims)
    fitvals=scipy.polyval(CC_dEdtfitpars, dEdtmean)
    fitr2=1.-((fitvals-delI)**2).sum()/((delI-delI.mean())**2).sum()
    
    dIdt=dIdE*dEdt
    avesloperatio=numpy.abs((dIdt[inds]/dIdt[inds+1])).mean()
    
    d['dEdtmean_cycs']=dEdtmean
    d['delI_cycs']=delI
    d['CC_dEdtfitpars']=CC_dEdtfitpars
    d['CC_dEdtfitR2']=fitr2
    d['Capac']=CC_dEdtfitpars[0]
    d['CurrIntercept']=CC_dEdtfitpars[1]
    d['dIdt_fwdrevratio']=avesloperatio
    
    if plotbool:
        pylab.subplot(222)
        pylab.plot(dIdt[inds]*1.e6, 'bo', label='fwd')
        pylab.plot(numpy.abs(dIdt[inds+1]*1.e6), 'go', label='rev')
        pylab.ylabel('dI/dt ($\mu$A/s)')
        pylab.xlabel('CV number')
        pylab.legend(loc=2)
        pylab.title('fwd:rev dI/dt = %.2f' %avesloperatio)

        pylab.subplot(224)
        pylab.plot(dEdtmean, delI*1.e6, 'o')
        pylab.ylabel('capacitive current ($\mu$A)')
        pylab.xlabel('ave scan rate (V/s)')



        pylab.plot(lims, fitlimvals*1.e6, 'r-')
        pylab.title('%.2e $\mu$F +%.2e $\mu$A, R$^2$=%.2f' %(CC_dEdtfitpars[0]*1.e6, CC_dEdtfitpars[1]*1.e6, fitr2), horizontalalignment='right')

        cs=''.join(['%s$_{%.2f}$' %tup for tup in zip(d['elements'], d['compositions'])])

        s='Sample %d, %s' %(d['Sample'], cs)
        ax1.set_title(s)
        pylab.subplots_adjust(left=.14, wspace=.26, right=.94, top=.93, hspace=.37)
        if not plotsavepath is None:
            pylab.savefig(plotsavepath)
    if returndict:
        return tuple(list(CC_dEdtfitpars)+[fitr2, d])
    else:
        return tuple(list(CC_dEdtfitpars)+[fitr2])

#CapCharge, CurrIntercept=calccapacitivecurrent([p, p2],plotfignum=1)
#pylab.show()
