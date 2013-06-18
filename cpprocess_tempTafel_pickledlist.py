
import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *
import pickle, csv

os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/LogCPPlots')
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'
folder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'

kl=['CP4Eave', 'CP5Eave', 'CP6Eave']
il=[1.e-4, 1.e-5, 1.9e-4]
vshiftl=[-(.187-.043), -(.187-.043), -(.187-.048)]

fns=os.listdir(folder)
d=None
for k, vs in zip(kl, vshiftl):
    for fn in fns:
        if k in fn and fn.endswith('txt'):
            p=os.path.join(folder, fn)
            f=open(p, mode='r')
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
            if d is None:
                d=dropd
            else:
                d[k]=dropd[k]
            d[k]-=vs
            break

#f=open(p, mode='r')
#dlist=pickle.load(f)
#f.close()
#
###filter dlist
#dlist=[d for d in dlist if 'I(A)_LinSub' in d.keys()]
#dlist=[d for d in dlist if d['Sample']<1970] #for the pseudoternary plate to avoid the 14x repeated compositions
#
#SGpts=10
#booldev_frac=.5#this is for a binary array so anything between 0 and 1 is legit
#booldev_nout=3
#booldn_segstart=3*booldev_nout
#
#dx=d['dE']
#dydev_frac=.2
#dydev_nout=5
#dn_segstart=3*dydev_nout
#dydev_abs=0.
#
#plotbool=0
#
#SegSG_dlist(dlist, SGpts=SGpts, order=1, k='I(A)_LinSub')
#
###save csv of FOM
###calculate V for critical I, etc
#for count, d in enumerate(dlist):
#    inds=d['segprops_dlist'][0]['inds']
#    #d['CV6fwdImax']=numpy.max(d['I(A)'][inds])
#    i=d['I(A)_LinSub_SG'][inds]
#    v=d['Ewe(V)'][inds]+vshift
#    posinds=numpy.where(i>5e-8)
#    invboolarr=numpy.float32(i<=5.e-8)
#    istart_segs, len_segs, fitdy_segs, fitinterc_segs=findzerosegs(invboolarr, booldev_frac,  booldev_nout, booldn_segstart,  SGnpts=10, plotbool=False, dx=1., maxfracoutliers=.5)
#    if len(istart_segs)==0:
#        print 'no positive segments found for ', count, ',  sample ',  d['Sample']
#        continue
#    ind=numpy.argmax(len_segs)
#    i0=istart_segs[ind]
#    i1=i0+len_segs[ind]
#    taffitinds=numpy.arange(i0, i1)
#    d['segprops_dlist'][0]['TafelFitInds']=inds[taffitinds]
#    i=i[i0:i1]
#    i[i<5e-8]=5e-8 #needed due to outliers
#    v=v[i0:i1]
#    il=numpy.log10(i)
#    istart_segs, len_segs, fitdy_segs, fitinterc_segs, dy=findlinearsegs(il, dydev_frac,  dydev_nout, dn_segstart, dydev_abs=dydev_abs,  plotbool=plotbool, dx=dx, critdy_fracmaxdy=None)
#    if len(istart_segs)==0:
#        print 'no Tafel segments found for ', count, ',  sample ',  d['Sample']
#        continue
#    ind=numpy.argmax(len_segs)
#    i0=istart_segs[ind]
#    i1=i0+len_segs[ind]
#    tafinds=numpy.arange(i0, i1)
#    it=il[tafinds]
#    vt=v[tafinds]
#    fitdy, fitint=numpy.polyfit(vt, it, 1)
##    fitx=numpy.array([v.min(), v.max()])
##    fity=fitint+fitdy*fitx
#    
#    d['segprops_dlist'][0]['TafelInds']=inds[taffitinds][tafinds]
#    d['TafelSlopeVperdec']=1./fitdy
#    d['TafelEstart_TafelValue']=v[0]
#    d['TafelFitVrange']=vt.max()-vt.min()
#    d['TafelLogExCurrent']=fitint
#    
##    for segd in d['segprops_dlist']:#[2:3]:
##        for st, k in zip([':', '--', '-'], ['inds', 'TafelFitInds', 'TafelInds']):
##            if not k in segd.keys():
##                continue
##            x=d['Ewe(V)'][segd[k]]+vshift
##            y=d['I(A)_LinSub'][segd[k]]
##            posinds=numpy.where(y>5e-8)
##            x=x[posinds]
##            y=numpy.log10(y[posinds])
##            pylab.plot(x, y, st)
##        break
##    pylab.plot(fitx, fity, 'y-')
##    print 1./fitdy, fitdy, fitint
##    
##    break
##pylab.show()
##    
##    
#
###making 10-sample plots of linear subtraction
#cols=['k','b', 'g', 'r', 'c', 'm', 'y', 'brown', 'purple', 'grey']
#smpall=numpy.array([d['Sample'] for d in dlist])
#dinds=numpy.argsort(smpall)
#plotcount=0
#smpl=[]
#pylab.figure()
#for di in dinds:
#    d=dlist[di]
#    if plotcount==10:
#        s='_'.join([`smp` for smp in smpl])
#        pylab.title(s)
#        pylab.savefig(s)
#        plotcount=0
#        smpl=[]
#        pylab.figure()
#    
#    for segd in d['segprops_dlist']:#[2:3]:
#        for st, k in zip([':', '--', '-'], ['inds', 'TafelFitInds', 'TafelInds']):
#            if not k in segd.keys():
#                continue
#            x=d['Ewe(V)'][segd[k]]
#            y=d['I(A)_LinSub'][segd[k]]
#            posinds=numpy.where(y>5e-8)
#            x=x[posinds]
#            y=numpy.log10(y[posinds])
#            pylab.plot(x, y, st, color=cols[plotcount])
#        break
#    smpl+=[d['Sample']]
#    plotcount+=1
#
#
#savekeys=['TafelSlopeVperdec','TafelEstart_TafelValue','TafelFitVrange','TafelLogExCurrent']
#
#
#mainapp=QApplication(sys.argv)
#form=MainMenu(None, execute=False, folderpath=savefolder)
#echemvis=form.echem
#echemvis.techniquedictlist=dlist
#
#
#def savefom(dlist, savefolder, key):
#    for d in dlist:
#        if key in d.keys():
#            d['FOM']=d[key]
#        else:
#            d['FOM']=numpy.nan
#            d[key]=numpy.nan
#
#    echemvis.writefile(p=savefolder, explab=key)
#
#for skey in savekeys:
#    savefom(echemvis.techniquedictlist, savefolder, skey)
#    
#if 1:
#    f=open(p, mode='w')
#    pickle.dump(dlist, f)
#    f.close()
