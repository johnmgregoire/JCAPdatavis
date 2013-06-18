
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


os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/LogCVCPPlots')
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'
p='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130604NiFeCoCe_plate1_CV_6220_dlist.dat';vshift=-(.187-.043)

cpfolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results'

if not os.path.exists(savefolder):
    os.mkdir(savefolder)
startpath_fom=os.path.join(savefolder, os.path.split(os.path.split(savefolder)[0])[1])

kl=['CP5Eave', 'CP4Eave', 'CP6Eave']
il=[1.e-5, 1.e-4, 1.9e-4]
cpvshiftl=[-(.187-.043), -(.187-.043), -(.187-.048)]


f=open(p, mode='r')
dlist=pickle.load(f)
f.close()

##filter dlist
dlist=[d for d in dlist if 'TafelSlopeVperdec' in d.keys() and not numpy.isnan(d['TafelSlopeVperdec'])]
dlist=[d for d in dlist if d['Sample']<1970]# this is tfor the pseudoternary plate to filter out the 14x repeat samples at the end




for d in dlist:
    d['I_cp']=numpy.array(il)
    d['V_cp']=[]
smp=[d['Sample'] for d in dlist]

fns=os.listdir(cpfolder)

for cpk, vs in zip(kl, cpvshiftl):
    for fn in fns:
        if cpk in fn and fn.endswith('txt'):
            p2=os.path.join(cpfolder, fn)
            f=open(p2, mode='r')
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
            for s, v in zip(dropd['Sample'], dropd[cpk]):
                if not s in smp:
                    continue
                i=smp.index(s)
                dlist[i]['V_cp']+=[v+vs]
            break

dlist=[d for d in dlist if len(d['V_cp'])==3]
#
#vtemp=numpy.array([d['V_cp'] for d in dlist])
#pylab.plot(vtemp[:, 0])
#pylab.plot(vtemp[:, 1])
#pylab.plot(vtemp[:, 2])
#pylab.show()


    

##save csv of FOM
##calculate V for critical I, etc
for count, d in enumerate(dlist):
    v=d['V_cp']
    il=numpy.log10(d['I_cp'])
    fitdy, fitint=numpy.polyfit(v, il, 1)
    fitvals=scipy.polyval((fitdy, fitint), v)
    fitr2=1.-((fitvals-il)**2).sum()/((il-il.mean())**2).sum()
    

    d['TafelCPSlopeVperdec']=1./fitdy
    d['TafelCPLogExCurrent']=fitint
    d['TafelCPfitR2']=fitr2
    

##making 1-sample plots of linear subtraction
cols=['k','b', 'g', 'r', 'c', 'm', 'y', 'brown', 'purple', 'grey']
smpall=numpy.array([d['Sample'] for d in dlist])
dinds=numpy.argsort(smpall)
plotcount=0
sl=[]
smpl=[]
pylab.figure()
for di in dinds:
    d=dlist[di]
    if plotcount==1:
        s='\n'.join(sl)
        pylab.title(s, fontsize=10)
        s='_'.join([`smp` for smp in smpl])
        pylab.savefig(s+'.png')
        plotcount=0
        sl=[]
        smpl=[]
        pylab.subplots_adjust(top=.82)
        pylab.clf()
    
    for segd in d['segprops_dlist']:#[2:3]:
        for st, k in zip([':', '-'], ['inds', 'TafelInds']):
            if not k in segd.keys():
                continue
            x=d['Ewe(V)'][segd[k]]+vshift
            y=d['I(A)_LinSub'][segd[k]]
            posinds=numpy.where(y>5e-8)
            x=x[posinds]
            y=numpy.log10(y[posinds])
            pylab.plot(x, y, st, color=cols[plotcount])
        break
    pylab.plot(d['V_cp'], numpy.log10(d['I_cp']), 'o', color=cols[plotcount])
    pylab.plot(d['V_cp'], d['V_cp']/d['TafelCPSlopeVperdec']+d['TafelCPLogExCurrent'], '--', color=cols[plotcount])
    sl+=['%d:TSlope CV,CP=%.2e,%.2e CPR2=%.2f' %(d['Sample'], d['TafelSlopeVperdec'], d['TafelCPSlopeVperdec'], d['TafelCPfitR2'])]
    smpl+=[d['Sample']]
    plotcount+=1
    
    

savekeys=['TafelCPSlopeVperdec','TafelCPLogExCurrent', 'TafelCPfitR2']


mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=savefolder)
echemvis=form.echem
echemvis.techniquedictlist=dlist


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

dlist=[d for d in dlist if d['TafelCPfitR2']>.94]

for fomkey in savekeys:
    pf=startpath_fom+'_'+fomkey+'_filterR2.txt'
    #p=p[::-1].replace('plate'[::-1], 'plate1'[::-1], 1)[::-1]#temporary fix for file naming for stacked_tern4
    writefile(pf, dlist, savedlist=False, fomkey=fomkey)


if 1:
    p2=p.replace('.dat', '_Tafelonly.dat')
    f=open(p2, mode='w')
    pickle.dump(dlist, f)
    f.close()
