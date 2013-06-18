
import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *
import pickle
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate1_test21Aug2012'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate1_dlist.dat'
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate1_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1'
#vshift=-.2

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9FeCoNiTi_500C_fast_CPCV_plate3_dlist.dat'
##os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate3_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate3'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9FeCoNiTi_500C_fast_CPCV_plate2_dlist.dat'
##os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate3_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate2'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCPCV_plate1_dlist.dat'
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate1_LinSubPlots2')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1'
#
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastrep2_plate1_dlist.dat'
##os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate3_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastrep2_plate1'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastrep3_plate1_dlist.dat'
##os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate3_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastrep3_plate1'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9FeCoNiTi_500C_CPCV_Plate3-rerun_dlist.dat'
##os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastCV_plate3_LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate3'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results/NiFeCoAl_F_plate3_dlist.dat'
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results/plate3/LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results/'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate1_dlist.dat'#20121101NiFeCoTi_P_plate3_dlist.dat'
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1/LogLinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1'



#pl=3
#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/plate%d/LogLinSubPlots'%pl)
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130402NiFeCoCe_Plate1_5500_dlist.dat';vshift=-(.187-.045)
#elif pl==2:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate2_5498_dlist.dat';vshift=-(.187-.045)
#elif pl==3:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate3_4835_dlist.dat';vshift=-(.187-.045)

#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/LogLinSubPlots')
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'
#p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130604NiFeCoCe_plate1_CV_6220_dlist.dat';vshift=-(.187-.043)


#pl=3
#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/plate%d/LogLinSubPlots'%pl)
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130529NiFeCoCe_plate1_5577_dlist.dat';vshift=-(.187-.045)
#elif pl==2:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130603NiFeCoCe_plate2_5498_dlist.dat';vshift=-(.187-.045)
#elif pl==3:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130528NiFeCoCe_plate3_4835_dlist.dat';vshift=-(.187-0.045)
    

os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results/LogLinSubPlots')
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results'
p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130612NiFeCoCe_plate1_CVpostCP_6321_dlist.dat';vshift=-(.187-0.045)


if not os.path.exists(savefolder):
    os.mkdir(savefolder)
startpath_fom=os.path.join(savefolder, os.path.split(os.path.split(savefolder)[0])[1])

critsegVrange=.04
critsegIend=3.e-5
critsegVend=0.36

f=open(p, mode='r')
dlist=pickle.load(f)
f.close()

##filter dlist
dlist=[d for d in dlist if 'I(A)_LinSub' in d.keys()]


    

SGpts=10
booldev_frac=.5#this is for a binary array so anything between 0 and 1 is legit
booldev_nout=3
booldn_segstart=3*booldev_nout

dx=d['dE']
dydev_frac=.2
dydev_nout=5
dn_segstart=3*dydev_nout
dydev_abs=0.

plotbool=0

SegSG_dlist(dlist, SGpts=SGpts, order=1, k='I(A)_LinSub')

#for selecting a particular sample
#smpall=numpy.array([d['Sample'] for d in dlist])
#i=numpy.where(smpall==18)[0]
#dlist=[dlist[i]]


#delete previous tael calculations
for d in dlist:
    segd=d['segprops_dlist'][0]
    for k in segd.keys():
        if k.startswith('Tafel'):
            del segd[k]
    for k in d.keys():
        if k.startswith('Tafel'):
            del d[k]    

##save csv of FOM
##calculate V for critical I, etc
for count, d in enumerate(dlist):
    inds=d['segprops_dlist'][0]['inds']
    #d['CV6fwdImax']=numpy.max(d['I(A)'][inds])
    i=d['I(A)_LinSub_SG'][inds]
    v=d['Ewe(V)'][inds]+vshift
    posinds=numpy.where(i>5e-8)
    invboolarr=numpy.float32(i<=5.e-8)
    istart_segs, len_segs, fitdy_segs, fitinterc_segs=findzerosegs(invboolarr, booldev_frac,  booldev_nout, booldn_segstart,  SGnpts=10, plotbool=False, dx=1., maxfracoutliers=.5)
    if len(istart_segs)==0:
        print 'no positive segments found for ', count, ',  sample ',  d['Sample']
        continue
    ind=numpy.argmax(len_segs)
    i0=istart_segs[ind]
    i1=i0+len_segs[ind]
    taffitinds=numpy.arange(i0, i1)
    d['segprops_dlist'][0]['TafelFitInds']=inds[taffitinds]
    i=i[i0:i1]
    i[i<5e-8]=5e-8 #needed due to outliers
    v=v[i0:i1]
    il=numpy.log10(i)
    try:
        istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(il, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=plotbool, dx=dx, critdy_fracmaxdy=None)
    except:
        print 'error finding Tafel segments found for ', count, ',  sample ',  d['Sample']
        continue
    if len(istart_segs)==0:
        print 'no Tafel segments found for ', count, ',  sample ',  d['Sample']
        continue
    
    #only take those segments covering a certain V range and with a min current for the top 10th of the V range in the segment and  positive slope for there on out and then take the steepest one.
    ind=None
    maxdy=0
    npts=critsegVrange/dx
    npts2=max(2, npts//10+1)
    for count2, (it0, slen, dyv) in enumerate(zip(istart_segs, len_segs, fitdy_segs)):
        #print '**', count2
        #print slen
        if slen<npts:
            continue
        it1=it0+slen
        #print numpy.mean(i[it1-npts2:it1])
        if numpy.mean(i[it1-npts2:it1])<critsegIend:
            continue
        #print numpy.mean(v[it1-npts2:it1])
        if numpy.mean(v[it1-npts2:it1])<critsegVend:
            continue
        #print numpy.any(dy[it1:]<0.)
        if numpy.any(dy[it1:]<0.):
            continue
        #print dyv, maxdy
        if dyv>maxdy:
            maxdy=dyv
            ind=count2
    if ind is None:
        print 'no Tafel segments found for ', count, ',  sample ',  d['Sample']
        continue
    #just take the longest
    #ind=numpy.argmax(len_segs)
    
    i0=istart_segs[ind]
    i1=i0+len_segs[ind]
    tafinds=numpy.arange(i0, i1)
    it=il[tafinds]
    vt=v[tafinds]
    fitdy, fitint=numpy.polyfit(vt, it, 1)

    
    d['segprops_dlist'][0]['TafelInds']=inds[taffitinds][tafinds]
    d['TafelSlopeVperdec']=1./fitdy
    d['TafelEstart_TafelValue']=v[0]
    d['TafelFitVrange']=vt.max()-vt.min()
    d['TafelLogExCurrent']=fitint


##making 10-sample plots of linear subtraction
cols=['k','b', 'g', 'r', 'c', 'm', 'y', 'brown', 'purple', 'grey']
smpall=numpy.array([d['Sample'] for d in dlist])
dinds=numpy.argsort(smpall)
plotcount=0
smpl=[]
pylab.figure()
for di in dinds:
    d=dlist[di]
    if plotcount==10:
        s='_'.join([`smp` for smp in smpl])
        pylab.title(s)
        pylab.savefig(s)
        plotcount=0
        smpl=[]
        pylab.figure()
    
    for segd in d['segprops_dlist']:#[2:3]:
        for st, k in zip([':', '--', '-'], ['inds', 'TafelFitInds', 'TafelInds']):
            if not k in segd.keys():
                continue
            x=d['Ewe(V)'][segd[k]]+vshift
            y=d['I(A)_LinSub'][segd[k]]
            posinds=numpy.where(y>5e-8)
            x=x[posinds]
            y=numpy.log10(y[posinds])
            pylab.plot(x, y, st, color=cols[plotcount])
        break
    smpl+=[d['Sample']]
    plotcount+=1
    
#pylab.show()


savekeys=['TafelSlopeVperdec','TafelEstart_TafelValue','TafelFitVrange','TafelLogExCurrent']


def writefile(p, dlist, savedlist=True, fomkey='FOM'):
    
    if len(dlist)==0:
        print 'no data to save'
        return

    labels=['Sample', 'x(mm)', 'y(mm)']
    labels+=dlist[0]['elements']
    labels+=[fomkey]
    kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), (fomkey, '%.6e')]
    arr=[]
    for d in dlist:
        arr2=[]
        for k, fmt in kv_fmt:
            if not k in d.keys():
                v=numpy.nan
            else:
                v=d[k]
            if isinstance(v, numpy.ndarray) or isinstance(v, list):
                for subv in v:
                    arr2+=[fmt %subv]
            else:
                arr2+=[fmt %v]
        arr+=['\t'.join(arr2)]
    s='\t'.join(labels)+'\n'
    s+='\n'.join(arr)
    
    f=open(p, mode='w')
    f.write(s)
    f.close()
    
    if savedlist:
        f=open(p[:-4]+'_dlist.pck', mode='w')
        pickle.dump(dlist, f)
        f.close()

for fomkey in savekeys:
    pf=startpath_fom+'_'+fomkey+'.txt'
    #p=p[::-1].replace('plate'[::-1], 'plate1'[::-1], 1)[::-1]#temporary fix for file naming for stacked_tern4
    writefile(pf, dlist, savedlist=False, fomkey=fomkey)
    
if 1:
    f=open(p, mode='w')
    pickle.dump(dlist, f)
    f.close()
