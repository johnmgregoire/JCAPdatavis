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

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate1_test21Aug2012'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastCV_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9FeCoNiTi_500C_CPCV_Plate3-rerun'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9FeCoNiTi_500C_fast_CPCV_plate2'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastCPCV_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastrep2_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9_FeCoNiTi_500C_fastrep3_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/20121102NiFeCoAl_F_plate2 set2'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoAl_P/20121031NiFeCoTi_P_plate1'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoAl_P/20121031NiFeCoTi_P_plate2'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/20121101NiFeCoTi_P_plate3'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/20121031NiFeCoTi_P_plate2'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/20121031NiFeCoTi_P_plate1'

#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/20130425 NiFeCoLa_plate1_5959'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/20130426NiFeCoLa_plate2_5904'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/20130427 NiFeCoLa_plate3_5791'

#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/20130425 NiFeCeLa_plate3_5847'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/20130424 NiFeCeLa_plate2 5825 B'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/20130423 NiFeCeLa_plate1_5836'

#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/20130402NiFeCoCe_Plate1_5500'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/20130403NiFeCoCe_Plate2_5498'
p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/20130403NiFeCoCe_Plate3_4835'

fld, fn=os.path.split(p)
savep=os.path.join(os.path.join(fld, 'results'), fn+'_dlist.dat')

mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=p)

echemvis=form.echem

echemvis.expmntLineEdit.setText('CV3')

if 1:
    echemvis.get_techniquedictlist(nfiles=99999)

    dlist=echemvis.techniquedictlist

    print len(dlist)
    dlist=[d for d in dlist if len(d['Ewe(V)'])>100]
    print '%%', len(dlist)
    
    calcmeandEdt_dlist(dlist)
    if 1:
        calcsegind_dlist(dlist, SGpts=10)
    else:
        manualsegind_dlist(dlist, istart=[0, 562])
    SegSG_dlist(dlist, SGpts=10, order=1)
    SegSG_dlist(dlist, SGpts=10, order=1, k='Ewe(V)')
else:
    f=open(savep, mode='r')
    dlist=pickle.load(f)
    f.close()

#dlist=dlist[335:336]
#print len(dlist)

#from Biologic_testprocess import dl2
#dlist=dl2

#nsegs=numpy.array([len(d['segprops_dlist']) for d in dlist])
#dlist=[dlist[i] for i in numpy.where(nsegs==1)[0]]


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


#calccurvregions_dlist(dlist, SGpts=20, critfracposcurve=.95, curvetol=3.e-5)



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
###LinSub
for count, d in enumerate(dlist):
    dx=d['dt']
#    dx=d['scanrate']/1000.
#    minslope*=d['dt']/dx
#    dydev_abs*=d['dt']/dx
    for segd in d['segprops_dlist'][:1]:#[2:3]:
        try:
            y=d['I(A)'][segd['inds']]
            istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(y, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=plotbool, dx=dx, critdy_fracmaxdy=None)
            #print '***', istart_segs
            if len(istart_segs)==0:
                print 'NO SEGS FOUND',  count, 'sample',  d['Sample']
                pylab.plot(y)
                pylab.figure()
                pylab.plot(dy)
                istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(y, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=1, dx=dx, critdy_fracmaxdy=None)
                continue
            v0v1=numpy.array([d['Ewe(V)'][segd['inds']][i0:i0+l][[0, -1]] for i0, l in zip(istart_segs, len_segs)])
            dE_segs=v0v1[:, 1]-v0v1[:, 0]
            segi=numpy.where(((dE_segs)>Vsegrange1)&(fitdy_segs>minslope))[0]
            if len(segi)>0:
                seli=segi[numpy.argmin(fitdy_segs[segi])]
            else:
                segi=numpy.where(fitdy_segs>minslope)[0]
                seli=segi[numpy.argmin(fitdy_segs[segi])]
                print 'dE', dE_segs[seli],  'sample',  d['Sample']
            dysel=fitdy_segs[seli]
            intsel=fitinterc_segs[seli]
            #print dysel, intsel
            #for i0, l, dy, interc in zip(istart_segs, len_segs, fitdy_segs, fitinterc_segs):
            ylin=intsel+dysel*numpy.arange(len(y))*dx
    #        pylab.figure()
    #        pylab.plot(y)
    #        pylab.plot(ylin)
    #        pylab.plot(y-ylin)
            d['SegIndStart_LinSub']=istart_segs[seli]
            d['LinLen_LinSub']=len_segs[seli]
            d['Intercept_LinSub']=intsel
            d['dIdt_LinSub']=dysel
            d['I(A)_LinSub']=numpy.zeros(d['I(A)'].shape, dtype='float32')
            d['I(A)_LinSub'][segd['inds']]=numpy.float32(y-ylin)
        except:
            print 'problem,  skipping Sample ', d['Sample']

dIdEcrit=.0005
SegdtSG_dlist(dlist, SGpts=10, order=1, k='I(A)_LinSub', dxk='dE')
for d in dlist:
    if not 'I(A)_LinSub_dtSG' in d.keys():
        continue
    for segd in d['segprops_dlist'][:1]:
        y=d['I(A)_LinSub_dtSG'][segd['inds']]
        x=d['Ewe(V)_SG'][segd['inds']]
        starti=numpy.where(y<dIdEcrit)[0][-1]+1
        if starti<len(y):
            d['dIdE_aveabovecrit']=y[starti:].mean()
            d['E_dIdEcrit']=x[starti]
        else:
            d['dIdE_aveabovecrit']=numpy.nan
            d['E_dIdEcrit']=numpy.nan

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
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()

    #f=open(savep, mode='r')
    #dlistr=pickle.load(f)
    #f.close()

