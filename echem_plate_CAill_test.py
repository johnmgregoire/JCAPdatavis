import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *


p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/2012-9FeCoNiTi_500C_CAill_plate1'
os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9FeCoNiTi_500C_CAill_plate1_illgraphs')
mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=p)

echemvis=form.echem

echemvis.expmntLineEdit.setText('CA3')

echemvis.get_techniquedictlist(nfiles=99999)

dlist=echemvis.techniquedictlist


o=numpy.ones(500, dtype='float32')
z=numpy.zeros(500, dtype='float32')
tocat=[z]
for i in range(15):
    tocat+=[o, z]
ill=numpy.concatenate(tocat)


darkinds=numpy.arange(90, 490)
illinds=numpy.arange(590, 990)
darkinds_cyc=[darkinds+i*1000 for i in range(16)]
illinds_cyc=[illinds+i*1000 for i in range(15)]

darkindsplot=numpy.arange(0, 500)
illindsplot=numpy.arange(500, 1000)
darkindsplot_cyc=[darkinds+i*1000 for i in range(16)]
illindsplot_cyc=[illinds+i*1000 for i in range(15)]


getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in darkinds_cyc])
getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in illinds_cyc])

o500=numpy.ones(500, dtype='float32')

t_ill=getillvals(dlist[0]['t(s)'])

pylab.figure()

for d in dlist:
    if d['Sample']!=1164:
        continue
    if len(d['I(A)'])<15500:
        print 'problem with sample ', d['Sample']
        d['Photocurrent(A)']=numpy.nan
        d['Photocurrent_std(A)']=numpy.nan
        d['Photocurrent_cycs(A)']=numpy.nan
        continue
    i_ill=getillvals(d['I(A)'])
    i_dark=getdarkvals(d['I(A)'])
    idiff=i_ill-0.5*(i_dark[:-1]+i_dark[1:])
    d['Photocurrent(A)']=idiff.mean()
    d['Photocurrent_std(A)']=idiff.std()
    d['Photocurrent_cycs(A)']=idiff
    pylab.clf()
    ax=pylab.subplot(111)
    ax2=ax.twinx()
    ax.plot(d['t(s)'], d['I(A)'])
    d['I(A)_SG']=savgolsmooth(d['I(A)'], nptsoneside=100, order = 2)
    ax.plot(d['t(s)'], d['I(A)_SG'], 'k')
    ax2.plot(t_ill, idiff, 'ro')
    iplt=numpy.concatenate([numpy.concatenate([dv*o500, di*o500]) for dv, di in zip(i_dark, i_ill)]+[i_dark[-1]*o500])
    ax.plot(d['t(s)'], iplt, 'g')
    s=`d['Sample']`+', '
    for el, v in zip(d['elements'], d['compositions']):
        s+=el+'%d' %(100*v)
    pylab.title(s)
    pylab.savefig(`d['Sample']`)
if 0:
    import pickle
    fld, fn=os.path.split(p)
    savep=os.path.join(os.path.join(fld, 'results'), fn+'_dlist.dat')
    f=open(savep, mode='w')
    pickle.dump(dlist, f)
    f.close()

    #f=open(savep, mode='r')
    #dlistr=pickle.load(f)
    #f.close()

i_ill=numpy.array([d['Photocurrent(A)'] for d in dlist if not numpy.isnan(d['Photocurrent(A)'])])
stdi_ill=numpy.array([d['Photocurrent_std(A)'] for d in dlist if not numpy.isnan(d['Photocurrent(A)'])])
samples=numpy.array([d['Sample'] for d in dlist if not numpy.isnan(d['Photocurrent(A)'])])
inds=numpy.where((i_ill>0)&(i_ill>2.*stdi_ill))[0]

isort=numpy.argsort(i_ill[inds])
#print len(inds)
#print samples[inds][isort[:10]]


#pylab.show()
