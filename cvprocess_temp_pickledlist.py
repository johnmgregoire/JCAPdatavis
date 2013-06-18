
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

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121101NiFeCoTi_P_plate3_dlist.dat'#20121031NiFeCoTi_P_plate2_dlist.dat'
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate3/LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate3'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate2_dlist.dat'#
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate2/LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate2'

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate1_dlist.dat'#
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1/LinSubPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1'

#pl=1
#os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results/plate%d/LinSubPlots'%pl)
#savefolder='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results/20130425 NiFeCoLa_plate1_5959_dlist.dat';vshift=-(.187-.030)
#elif pl==2:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results/20130426NiFeCoLa_plate2_5904_dlist.dat';vshift=-(.187-.028)
#elif pl==3:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results/20130427 NiFeCoLa_plate3_5791_dlist.dat';vshift=-(.187-.005)

#pl=3
#os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results/plate%d/LinSubPlots'%pl)
#savefolder='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results/20130423 NiFeCeLa_plate1_5836_dlist.dat';vshift=-(.187-.005)
#elif pl==2:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results/20130424 NiFeCeLa_plate2 5825 B_dlist.dat';vshift=-(.187-0.)
#elif pl==3:
#    p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results/20130425 NiFeCeLa_plate3_5847_dlist.dat';vshift=-(.187-.034)


#pl=3
#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/plate%d/LinSubPlots'%pl)
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130402NiFeCoCe_Plate1_5500_dlist.dat';vshift=-(.187-.045)
#elif pl==2:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate2_5498_dlist.dat';vshift=-(.187-.045)
#elif pl==3:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate3_4835_dlist.dat';vshift=-(.187-.045)
    

#os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/LinSubPlots0.02')
#savefolder='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.02_plate123'
#p='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.02_plate123_dlist.dat';vshift=-(.187-.0)
    
#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/LinSubPlots')
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'
#p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130604NiFeCoCe_plate1_CV_6220_dlist.dat';vshift=-(.187-.043)



#pl=3
#os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/plate%d/LinSubPlots'%pl)
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/plate%d' %pl
#if pl==1:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130529NiFeCoCe_plate1_5577_dlist.dat';vshift=-(.187-.045)
#elif pl==2:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130603NiFeCoCe_plate2_5498_dlist.dat';vshift=-(.187-.045)
#elif pl==3:
#    p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130528NiFeCoCe_plate3_4835_dlist.dat';vshift=-(.187-0.045)


os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results/LinSubPlots')
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results'
p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130612NiFeCoCe_plate1_CVpostCP_6321_dlist.dat';vshift=-(.187-0.045)



#vshift=0#.-.177#-.24

f=open(p, mode='r')
dlist=pickle.load(f)
f.close()

##filter dlist
dlist=[d for d in dlist if 'I(A)_LinSub' in d.keys()]


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
        x=d['Ewe(V)'][segd['inds']]
        y1=d['I(A)'][segd['inds']]
        y2=d['I(A)_LinSub'][segd['inds']]
        pylab.plot(x, y1, '--', color=cols[plotcount])
        pylab.plot(x, y1-y2, ':', color=cols[plotcount])
        pylab.plot(x, y2, '-', color=cols[plotcount])
        break
    smpl+=[d['Sample']]
    plotcount+=1


###making 6-sample plots of linear subtraction
#cols=['k','b', 'g', 'r', 'c', 'm', 'y', 'brown', 'purple', 'grey']
#smpall=numpy.array([d['Sample'] for d in dlist])
#dinds=numpy.argsort(smpall)
#plotcount=1
#smpl=[]
#PLOT=1
#SAVE=1
#pylab.figure()
#for di in dinds:
#    d=dlist[di]
#    if PLOT:
#        if not d['Sample'] in [1066,1662]:#[1889,1662]:#[1662, 582,  2073,  2077,  1141,     9,  1603,  1227,  1139,   610]:#[610,1382]:#[76,43,44,53,20,34,42,28,57,55]:#[ 30,67, 641,36,41,46,47,49,58,74]:#[1811, 1382, 1338]:
#            continue
#        if SAVE:
#            fld, fn=os.path.split(p)
#            savep=os.path.join(os.path.join(fld, 'echemplots'), fn[:-4]+'_%d.dat' %d['Sample'])
#            f=open(savep, mode='w')
#            pickle.dump(d, f)
#            f.close()
##    if plotcount==6:
##        s='_'.join([`smp` for smp in smpl])
##        pylab.title(s)
##        pylab.savefig(s)
##        plotcount=0
##        smpl=[]
##        pylab.clf()
#    
#    segd1, segd2=d['segprops_dlist']
#    x=d['Ewe(V)'][segd1['inds']]
#    y1=d['I(A)'][segd1['inds']]
#    y2=d['I(A)_LinSub'][segd1['inds']]
#    if PLOT:
#        pylab.plot(x[5:], y1[5:], '-', color=cols[plotcount])
#        pylab.plot(x[5:], (y1-y2)[5:], ':', color=cols[plotcount])
#    d['ImaxLinSub']=numpy.max(y2)
#    x=d['Ewe(V)'][segd2['inds']]
#    y1=d['I(A)'][segd2['inds']]
#    if PLOT:
#        pylab.plot(x, y1, '--', color=cols[plotcount])
#    d['Imin']=numpy.min(y1)
#    d['IminFromEnd']=numpy.min(y1)-y1[-50:].mean()
#    smpl+=[d['Sample']]
#    plotcount+=1

####finding the riht samples to plot
#if PLOT:
#    pylab.show()
#else:
#    sample=numpy.array([dlist[di]['Sample'] for di in dinds])
#    imin=numpy.array([dlist[di]['Imin'] for di in dinds])
#    isort=numpy.argsort(imin)
#    inds2=dinds[isort]
#    #print [dlist[di]['Sample'] for di in inds2[:10]]
#
#    imax=numpy.array([dlist[di]['ImaxLinSub'] for di in dinds])
#    inds3=numpy.where((imin>-2.2e-5))[0]
#    isort3=numpy.argsort(imax[inds3])
#    #print sample[inds3[isort3[-10:]]]
#    #print imin[inds3[isort3[-10:]]]
#    #print imax[inds3[isort3[-10:]]]
#
#    iminend=numpy.array([dlist[di]['IminFromEnd'] for di in dinds])
#    inds4=numpy.where((iminend>-1.e-6))[0]
#    isort4=numpy.argsort(imax[inds4])
#    #
#    #print sample[inds4[isort4[-10:]]]
#    #print iminend[inds4[isort4[-10:]]]
#    #print imax[inds4[isort4[-10:]]]
#
#    didt=numpy.array([dlist[di]['dIdt_LinSub'] for di in dinds])
#    inds5=numpy.where((didt<6.e-5)&(imax>8.e-5)&(imax<1.e-4))[0]
#    isort5=numpy.argsort(iminend[inds5])
#    print sample[inds5[isort5[:10]]]
#    print iminend[inds5[isort5[:10]]]
#    print imax[inds5[isort5[:10]]]


    

##save csv of FOM
##calculate V for critical I, etc
for d in dlist:
    inds=d['segprops_dlist'][0]['inds']
    #d['CV4fwdImax']=numpy.max(d['I(A)'][inds])
    i=d['I(A)_LinSub'][inds]
    v=d['Ewe(V)'][inds]
    d['ImaxCVLinSub']=numpy.max(i)
    vsh=v+vshift
#    aveinds=numpy.where((vsh>.495)&(vsh<=.505))
#    d['I500mVoverpotLinSub']=numpy.mean(i[aveinds])
    aveinds=numpy.where((v>.645)&(v<=.655))
    d['I650mVLinSub']=numpy.mean(i[aveinds])
    
    vanl=[.3, .35, .4]
    var=vsh
    for van in vanl:
        k='I%dmVLinSub' %(van*1000.,)
        aveinds=numpy.where((var>van-.005)&(var<=van+.005))
        d[k]=numpy.mean(i[aveinds])
    
#    aveinds=numpy.where((v>.695)&(v<=.705))
#    d['I700mVLinSub']=numpy.mean(i[aveinds])
    
#    #vsh=v+vshift
#    aveinds=numpy.where((v>.672)&(v<=.682))
#    d['I677mVLinSub']=numpy.mean(i[aveinds])
#    
#    aveinds=numpy.where((v>.622)&(v<=.632))
#    d['I627mVLinSub']=numpy.mean(i[aveinds])
    
#    aveinds=numpy.where((v>.572)&(v<=.582))
#    d['I577mVLinSub']=numpy.mean(i[aveinds])
#    ###requirement to be above critical current for n consecutive points
#    icrit=1.e-4
#    b=numpy.int16(i>=icrit)
#    n=10
#    bconsec=[b[i:i+n].prod() for i in range(len(b)-n)]
#    if True in bconsec:
#        i=bconsec.index(True)
#        d['V_IthreshCVLinSub']=v[i:i+n].mean()
#    else:
#        d['V_IthreshCVLinSub']=numpy.nan
#    

    ###requirement to be above critical current for rest of scan with n outliers
    nout=5
    for icrit in [1.e-5, 3.e-5, 1.e-4, 1.9e-4, 3.e-4]:
        k='V_IthreshCVLinSub_%d' %(icrit*1.e6)
        b=numpy.where(i<icrit)[0]
        if (len(i)-len(b))<(nout+1) or numpy.all(i[-nout:]<icrit):
            d[k]=numpy.nan
        else:
            if len(b)==0:
                ind=0
            else:
                ind=b[-nout]
                ind+=nout-1
            d[k]=var[max(0, ind-4):ind+4].mean()

    


#savekeys=['SegIndStart_LinSub','LinLen_LinSub','Intercept_LinSub','dIdt_LinSub', 'ImaxCVLinSub', 'V_IthreshCVLinSub', 'I500mVoverpotLinSub']
savekeys=['SegIndStart_LinSub','LinLen_LinSub','Intercept_LinSub','dIdt_LinSub', 'ImaxCVLinSub', 'V_IthreshCVLinSub_300',  'V_IthreshCVLinSub_100', 'V_IthreshCVLinSub_30', 'V_IthreshCVLinSub_10', 'V_IthreshCVLinSub_190', 'I300mVLinSub', 'I350mVLinSub', 'I400mVLinSub']#'CV6fwdImax', 'I627mVLinSub', 'I577mVLinSub']


mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=savefolder)
echemvis=form.echem
echemvis.techniquedictlist=dlist


def savefom(dlist, savefolder, key):
    for d in dlist:
        d['FOM']=d[key]
    echemvis.writefile(p=savefolder, explab=key)

for skey in savekeys:
    savefom(echemvis.techniquedictlist, savefolder, skey)


###dEdt analysis
#calcmeandEdt_dlist(dlist)
#SegSG_dlist(dlist, SGpts=10, order=1, k='Ewe(V)')
#dIdEcrit=.0005
#SegdtSG_dlist(dlist, SGpts=10, order=1, k='I(A)_LinSub', dxk='dE')
#for d in dlist:
#    for segd in d['segprops_dlist'][:1]:
#        y=d['I(A)_LinSub_dtSG'][segd['inds']]
#        x=d['Ewe(V)_SG'][segd['inds']]
#        starti=numpy.where(y<dIdEcrit)[0][-1]+1
#        if starti<len(y):
#            d['dIdE_aveabovecrit']=y[starti:].mean()
#            d['E_dIdEcrit']=x[starti]
#        else:
#            d['dIdE_aveabovecrit']=numpy.nan
#            d['E_dIdEcrit']=numpy.nan
#        d['dIdEmax']=y.max()
#for key in ['dIdE_aveabovecrit','E_dIdEcrit', 'dIdEmax']:
#    savefom(echemvis.techniquedictlist, savefolder, key)

###plot select CVs
#smps=[d['Sample'] for d in dlist]
#for sample in [4, 164, 459, 539]:
#    d=dlist[smps.index(sample)]
#    inds=d['segprops_dlist'][0]['inds']
#    x=d['Ewe(V)'][inds][3:]
#    y1=d['I(A)'][inds][3:]
#    y2=d['I(A)_LinSub'][inds][3:]
#    pylab.figure()
#    pylab.plot(d['Ewe(V)'][3:], d['I(A)'][3:], '-', color='k')
#    #pylab.plot(x, y1, '--', color=)
#    pylab.plot(x, y1-y2, ':', color='r')
#    pylab.plot(x, y2, '-', color='b')
#    pylab.title(`sample`)
#pylab.show()
#print 'done'



###making select ample plots of dI/dt
#cols=['k','b', 'g', 'r', 'c', 'm', 'y', 'brown', 'purple', 'grey']
#smpall=numpy.array([d['Sample'] for d in dlist])
#dinds=numpy.argsort(smpall)
#plotcount=1
#labs=[]
#PLOT=1
#pylab.figure(figsize=(6, 4))
#ax=pylab.subplot(111)
#ax2=ax.twinx()
#for di in dinds:
#    d=dlist[di]
#    if PLOT:
#        if not d['Sample'] in [541,548,546]:#[868,1334,365]:#[1413,1834,1356]:
#            continue
#
#    
#    segd1, segd2=d['segprops_dlist']
#    x=d['Ewe(V)'][segd1['inds']]
#    y1=d['I(A)'][segd1['inds']]
#    y2=d['I(A)_LinSub'][segd1['inds']]
#    dy2=d['I(A)_LinSub_dtSG'][segd1['inds']]
#    xc=d['E_dIdEcrit']
#    if PLOT:
#        ax.plot(x[5:], y1[5:], '--', color=cols[plotcount])
#        ax.plot(x[5:], y2[5:], '-', color=cols[plotcount])
#        ax2.plot(x[5:], dy2[5:], ':', color=cols[plotcount])
#        #i=numpy.argmin((xc-x)**2)
#        ax.plot([xc, xc], list(ax.get_ylim()), '-', color=cols[plotcount], alpha=.7)
#
#    labs+=['%d:%d-%d-%d-%d' %tuple([d['Sample']]+list(d['compositions']*100.))]
#    plotcount+=1
#
####finding the riht samples to plot
#if PLOT:
#    pylab.title(', '.join(labs), fontsize=14)
#    ax.set_xlabel('V (ref)', fontsize=14)
#    ax.set_ylabel('I, raw=dashed, LinSub=solid', fontsize=14)
#    ax2.set_ylabel('dI/dE, dotted', fontsize=14)
#    pylab.subplots_adjust(left=.19, right=.83, bottom=.16)
#    pylab.show()
#    
#    
#else:
#    dinds2=numpy.array([di for di in dinds if not numpy.isnan(dlist[di]['E_dIdEcrit'])])
#    sample=numpy.array([dlist[di]['Sample'] for di in dinds2])
#    
#    EdIdE=numpy.array([dlist[di]['E_dIdEcrit'] for di in dinds2])
#    isortEdIdE=numpy.argsort(EdIdE)
#    indsEdIdE=dinds2[isortEdIdE]
#    
#    avedIdE=numpy.array([dlist[di]['dIdE_aveabovecrit'] for di in dinds2])
#    isortavedIdE=numpy.argsort(avedIdE)
#    indsavedIdE=dinds2[isortavedIdE]
#    
#    maxdIdE=numpy.array([dlist[di]['dIdEmax'] for di in dinds2])
#    isortmaxdIdE=numpy.argsort(maxdIdE)
#    indsmaxdIdE=dinds2[isortmaxdIdE]
#    
##    print '%s, (%s,%s)' %(`[EdIdE[i] for i in isortEdIdE[:3]]`, `EdIdE.min()`, `EdIdE.max()`)
##    print ', '.join(['%s:%s' %(`dlist[di]['Sample']`, `dlist[di]['compositions']`) for di in indsEdIdE[:3]])
#    
##    print '%s, (%s,%s)' %(`[avedIdE[i] for i in isortavedIdE[-3:]]`, `avedIdE.min()`, `avedIdE.max()`)
##    print ', '.join(['%s:%s' %(`dlist[di]['Sample']`, `dlist[di]['compositions']`) for di in indsavedIdE[-3:]])
#    
#    print '%s, (%s,%s)' %(`[maxdIdE[i] for i in isortmaxdIdE[-3:]]`, `maxdIdE.min()`, `maxdIdE.max()`)
#    print ', '.join(['%s:%s' %(`dlist[di]['Sample']`, `dlist[di]['compositions']`) for di in indsmaxdIdE[-3:]])

if 1:
    f=open(p, mode='w')
    pickle.dump(dlist, f)
    f.close()
