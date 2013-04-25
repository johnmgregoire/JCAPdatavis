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

sdcp='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121101NiFeCoTi_P_plate3_dlist.dat'#20121031NiFeCoTi_P_plate2_dlist.dat'
os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate3/LinSubPlots')
savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate3'
uvp='C:/Users/Gregoire/Documents/CaltechWork/UVvisdata/201210NiFeCoTi_P/plate3_wl_en_dlist.pck'

#sdcp='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate2_dlist.dat'#
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate2/UVvisPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate2'
#uvp='C:/Users/Gregoire/Documents/CaltechWork/UVvisdata/201210NiFeCoTi_P/plate2_wl_en_dlist.pck'

#sdcp='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate1_dlist.dat'#
#os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1/UVvisPlots')
#savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/plate1'
#uvp='C:/Users/Gregoire/Documents/CaltechWork/UVvisdata/201210NiFeCoTi_P/plate1_wl_en_dlist.pck'


p_am15='C:/Users/Gregoire/Documents/CaltechWork/UVvisdata/201210NiFeCoTi_P/AM15_W_m2_nm.pck'
f=open(p_am15, mode='r')
W_m2_nm=pickle.load(f)
f.close()



f=open(sdcp, mode='r')
dlist=pickle.load(f)
f.close()

f=open(uvp, mode='r')
wl, en, uvdlist=pickle.load(f)
f.close()
    
sdcsmpall=numpy.array([d['Sample'] for d in dlist])
uvsmpall=numpy.array([d['sample_no'] for d in uvdlist])

for count, (d, s) in enumerate(zip(dlist, sdcsmpall)):
    i=numpy.where(uvsmpall==s)[0]
    if len(i)!=1:
        print 'problem with ', count, s, i
        continue
    i=i[0]
    d['UVvis_T']=uvdlist[i]['T']

print 'sdc:', len(dlist)
print 'uvvis:', len(uvdlist)
dlist=[d for d in dlist if 'UVvis_T' in d.keys()]
print 'together:', len(dlist)

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
#    pylab.plot(en, d['UVvis_T'], '-', color=cols[plotcount])
#    pylab.ylim(-.5, 2)
#    smpl+=[d['Sample']]
#    plotcount+=1


##save csv of FOM
##calcmeanT
en0, en1=(1.4, 3.)
inds=numpy.where((en>en0)&(en<en1))
k='UVvis_T_%.1f_%.1f' %(en0, en1)

den=en[1:]-en[:-1]
den=numpy.concatenate([den, [den[-1]]])
den=numpy.abs(den)

den_inds=den[inds]
intfcn=lambda arr:(arr[inds]*den_inds).sum()/den_inds.sum()

denam15_inds=W_m2_nm[inds]*den[inds]

intfcn_am15=lambda arr:(arr[inds]*denam15_inds).sum()/denam15_inds.sum()


k_am15='UVvis_Ten_%.1f_%.1f_am1.5' %(en0, en1)

k3='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__I677mV'

k4='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__I627mV'
k4b='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__0.3cutI627mV'
k4c='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__0.23cutI627mV'

k5='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__I577mV'

k5b='UVvis_Ten_%.1f_%.1f_am15' %(en0, en1)+'__0.1cutI577mV'

for d in dlist:
    d[k]=intfcn(d['UVvis_T'])
    d[k_am15]=intfcn_am15(d['UVvis_T'])
    d[k3]=d[k_am15]*d['I677mVLinSub']
    d[k4]=d[k_am15]*d['I627mVLinSub']
    d[k4b]=d[k_am15]*min(d['I627mVLinSub'], 3.e-4)/3.e-4
    d[k4c]=d[k_am15]*min(d['I627mVLinSub'], 2.3e-4)/2.3e-4
    d[k5]=d[k_am15]*d['I577mVLinSub']
    d[k5b]=d[k_am15]*min(d['I577mVLinSub'], 1.e-4)/1.e-4
    
savekeys=[k, k_am15, k3, k4, k4b, k4c, k5, k5b]


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

if 0:
    f=open(sdcp, mode='w')
    pickle.dump(dlist, f)
    f.close()
