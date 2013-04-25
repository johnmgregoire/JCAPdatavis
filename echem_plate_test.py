import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate1_test21Aug2012'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastCV_plate1'
p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9FeCoNiTi_500C_CPCV_Plate3-rerun'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9FeCoNiTi_500C_fast_CPCV_plate2'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastCPCV_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastrep2_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastrep3_plate1'

mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=p)

echemvis=form.echem

echemvis.expmntLineEdit.setText('CV5')

echemvis.get_techniquedictlist(nfiles=99999)

dlist=echemvis.techniquedictlist


#from Biologic_testprocess import dl2
#dlist=dl2



#SGpts=20
#critfracposcurve=.95
#curvetol=3.e-5
def calccurvregions_dlist(dlist, SGpts=10, critfracposcurve=.95, curvetol=3.e-5):
    for d in dlist:
        d['I(A)_dtdtSG']=numpy.empty(d['I(A)'].shape, dtype='float32')
        d['I(A)_dtSG']=numpy.empty(d['I(A)'].shape, dtype='float32')
        for segd in d['segprops_dlist']:
            #d['I(A)_dtdtSG'][inds]=numpy.float32(savgolsmooth(d['I(A)'][inds], nptsoneside=SGpts, order = 3, dx=d['dt'], deriv=2, binprior=0))
            inds=segd['inds']
            d['I(A)_dtSG'][inds]=numpy.float32(savgolsmooth(d['I(A)'][inds], nptsoneside=SGpts, order = 2, dx=d['dt'], deriv=1, binprior=0))
            d['I(A)_dtdtSG'][inds]=numpy.float32(savgolsmooth(d['I(A)_dtSG'][inds], nptsoneside=SGpts, order = 2, dx=d['dt'], deriv=1, binprior=0))
            
            startatend=segd['rising']
            
            
            if startatend:
                arr=d['I(A)_dtdtSG'][inds][::-1]
            else:
                arr=d['I(A)_dtdtSG'][inds]
            arr+=curvetol
            zinds=arrayzeroind1d(arr, postoneg=True, negtopos=False)
            zinds.sort()
            zinds=numpy.array(zinds, dtype='int32')
            posarr=arr>=0
            starti=numpy.where(posarr)[0][0]
            if len(zinds)==0 and numpy.all(posarr):
                cutoffind=len(arr)
            else:
                if len(zinds)==0:
                    zinds=numpy.array([len(arr)])
                cutoffinds=[zi for zi in zinds if (posarr[starti:zi].sum(dtype='float32'))/(zi-starti)>critfracposcurve]
                if len(cutoffinds)==0:
                    print 'no suitable positive curvature reagion found'
                    cutoffind=starti
                else:
                    cutoffind=max(cutoffinds)
            
            if startatend:
                segd['anreginds']=inds[::-1][starti:cutoffind][::-1]
                #poscurveinds=set(inds[posarr[::-1]])
            else:
                segd['anreginds']=inds[starti:cutoffind]
    #            poscurveinds=set(inds[posarr])
    #        
    #        poscurveinds=numpy.array(poscurveinds.intersection(set(segd['anreginds'])))
    #        segd['poscurveinds']=numpy.sorted(poscurveinds)
            
            #segd['poscurveinds']=inds[d['I(A)_dtdtSG'][inds]>0]
            segd['poscurveinds']=segd['anreginds'][d['I(A)_dtdtSG'][segd['anreginds']]>0]
            if cutoffind==starti:
                pylab.figure()
                pylab.plot(arr)
                pylab.plot(zinds[zinds<len(arr)], arr[zinds<len(arr)],'ro')
                pylab.figure()
                ax=pylab.subplot(111)
                ax2=ax.twinx()
                pylab.figure()
                ax3=pylab.subplot(111)
                ax4=ax3.twinx()
            #for segd in d['segprops_dlist']:
                inds=segd['inds']
                aninds=segd['anreginds']
                pcinds=segd['poscurveinds']
                ax.plot(d['t(s)'][inds], d['I(A)'][inds], ':', linewidth=5)
                ax.plot(d['t(s)'][aninds], d['I(A)'][aninds], '--', linewidth=3)
                ax.plot(d['t(s)'][pcinds], d['I(A)'][pcinds], '.', ms=3)
                ax2.plot(d['t(s)'][inds], d['I(A)_dtSG'][inds])
                ax3.plot(d['t(s)'][inds], d['I(A)_dtdtSG'][inds])
                #ax4.plot(d['t(s)'][inds], d['I(A)_dt_dtSG'][inds], ':')
    #            break
    #    if cutoffind==starti:
    #        break




calcmeandt_dlist(dlist)
calcsegind_dlist(dlist, SGpts=10)

#pylab.figure()
#for d in dlist:
#    pylab.plot(d['Ewe(V)'], d['I(A)'])
#
#pylab.figure()
#for d in dlist:
#    pylab.plot(d['t(s)'], d['Ewe(V)'])
#
#
#pylab.figure()
#for d in dlist:
#    for segd in d['segprops_dlist'][2:3]:
#        pylab.plot(d['Ewe(V)'][segd['inds']], d['I(A)'][segd['inds']])
#        break
#pylab.show()

SegSG_dlist(dlist, SGpts=50, order=1)#10
#calccurvregions_dlist(dlist, SGpts=20, critfracposcurve=.95, curvetol=3.e-5)


###this is for fitting and never really panned out
#def explinfcn(pars, x):
#    return pars[2]*numpy.exp((x-pars[0])/pars[1])
#
#def tafelfcn(pars, x):
#    return pars[1]*numpy.exp(pars[0]*x)
#    
#def currfcn(pars, x):
#    return pars[2]/(1.+numpy.exp((pars[0]-x)*pars[1]/.0591))
#    
#fitfcn_explin=lambda p, x:p[0]+p[1]*x+tafelfcn(p[2:4], x)
#errfcn_explin=lambda p, x, y:fitfcn_explin(p, x)-y
##errfcn_explin=lambda p, x, y:((explin(p, x)-y)**2).sum()
#
#ilimguess_indfrac=.95
#
#for d in dlist:
#    for segd in d['segprops_dlist']:
#        if not segd['rising']:
#            continue
#        iarr=copy.copy(d['I(A)'][segd['anreginds']])
#        varr=copy.copy(d['Ewe(V)'][segd['anreginds']])-.2
#        iind=iarr.argsort()[int(ilimguess_indfrac*len(iarr))]
#        
#        faguess=19.5
#        i0guess=iarr[iind]/tafelfcn([faguess, 1.], varr[iind])
#        print iarr[iind], varr[iind], i0guess
##        iarrsort=iarr[]
##        ilimguess=iarrsort[]
##        ehalfguess=d['Ewe(V)'][segd['poscurveinds']][numpy.argmax(d['I(A)_dtdtSG'][segd['poscurveinds']])]
#        
#        #p0=[0., 0., ehalfguess, 1., ilimguess]
##        p0=[0., 0., faguess, i0guess]
##        p1, covmat, info, msg, success=optimize.leastsq(errfcn_explin, p0, args=(varr, iarr), full_output=1, ftol=1.e-12)
##        #p1_2gauss, covmat_2gauss, info_2gauss, msg_2gauss, success_2gauss=optimize.fmin(errfcn_2gauss, p0_2gauss, args=(q1, ic1), full_output=1, ftol=1.e-12, disp=0)
##        
##        ifit=fitfcn_explin(p1, varr)
##        ifit_exp=tafelfcn(p1[2:4], varr)
##        ifit_lin=ifit-ifit_exp
##        pylab.figure()
##        pylab.plot(varr, iarr, 'k.')
##        pylab.plot(varr, ifit, 'r-')
##        pylab.plot(varr, ifit_lin, 'b-')
##        pylab.plot(varr, ifit_exp, 'g-')
#        
#        pylab.figure()
#        pylab.plot(varr, numpy.log10(iarr))
###********************************


#orig
#dydev_frac=.1
#dydev_nout=20
#dn_segstart=3*dydev_nout
#dydev_abs=2.e-5
#plotbool=1
#Vsegrange=.1
#minslope=-1e-6

#fastCV
dydev_frac=.1
dydev_nout=20
dn_segstart=3*dydev_nout
dydev_abs=2.e-5
plotbool=0
Vsegrange1=.1
Vsegrange2=.1
minslope=-1e-6

#biologic
#dydev_frac=.2
#dydev_nout=20
#dn_segstart=3*dydev_nout
#dydev_abs=4.e-5
#plotbool=0
#Vsegrange=.1
#minslope=-1e-6
#
####LinSub
#for d in dlist:
#    dx=d['dt']
##    dx=d['scanrate']/1000.
##    minslope*=d['dt']/dx
##    dydev_abs*=d['dt']/dx
#    for segd in d['segprops_dlist']:#[2:3]:
#        y=d['I(A)'][segd['inds']]
#        istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(y, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=plotbool, dx=dx, critdy_fracmaxdy=None)
#        if len(istart_segs)==0:
#            print 'NOT SEGS FOUND',  'sample',  d['Sample']
#            pylab.plot(y)
#            pylab.figure()
#            pylab.plot(dy)
#            istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(y, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=1, dx=dx, critdy_fracmaxdy=None)
#            continue
#        v0v1=numpy.array([d['Ewe(V)'][segd['inds']][i0:i0+l][[0, -1]] for i0, l in zip(istart_segs, len_segs)])
#        dE_segs=v0v1[:, 1]-v0v1[:, 0]
#        segi=numpy.where(((dE_segs)>Vsegrange1)&(fitdy_segs>minslope))[0]
#        if len(segi)>0:
#            seli=segi[numpy.argmin(fitdy_segs[segi])]
#        else:
#            segi=numpy.where(fitdy_segs>minslope)[0]
#            seli=segi[numpy.argmin(fitdy_segs[segi])]
#            print 'dE', dE_segs[seli],  'sample',  d['Sample']
#        dysel=fitdy_segs[seli]
#        intsel=fitinterc_segs[seli]
#        #print dysel, intsel
#        #for i0, l, dy, interc in zip(istart_segs, len_segs, fitdy_segs, fitinterc_segs):
#        ylin=intsel+dysel*numpy.arange(len(y))*dx
##        pylab.figure()
##        pylab.plot(y)
##        pylab.plot(ylin)
##        pylab.plot(y-ylin)
#        d['SegIndStart_LinSub']=istart_segs[seli]
#        d['LinLen_LinSub']=len_segs[seli]
#        d['Intercept_LinSub']=intsel
#        d['dIdt_LinSub']=dysel
#        d['I(A)_LinSub']=numpy.empty(d['I(A)'].shape, dtype='float32')
#        d['I(A)_LinSub'][segd['inds']]=numpy.float32(y-ylin)
#        break

#pylab.figure()
#for d in dlist:
#    for segd in d['segprops_dlist']:#[2:3]:
#        pylab.plot(d['Ewe(V)'][segd['inds']], d['I(A)'][segd['inds']])
#        break
#pylab.figure()
#for d in dlist:
#    for segd in d['segprops_dlist']:#[2:3]:
#        pylab.plot(d['Ewe(V)'][segd['inds']], d['I(A)_LinSub'][segd['inds']])
#        break
#
#pylab.show()
#
#pylab.show()
if 1:
    import pickle
    fld, fn=os.path.split(p)
    savep=os.path.join(os.path.join(fld, 'results'), fn+'_dlist.dat')
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()

    #f=open(savep, mode='r')
    #dlistr=pickle.load(f)
    #f.close()


