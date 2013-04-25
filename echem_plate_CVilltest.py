import time, copy
import os, os.path
import sys, operator
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *


p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/201212_BiVNiFe_plate1_4026'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/201212_BiVNiFe_plate2_4015'
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/201212_BiVNiFe_plate3_4004'
os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results/')
mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=p)

echemvis=form.echem

echemvis.expmntLineEdit.setText('CV3')

echemvis.get_techniquedictlist(nfiles=220)

dlist=echemvis.techniquedictlist

if 1:
    smpls=[d['Sample'] for d in dlist]
    d=dlist[smpls.index(121)]
else:
    d=dlist[-1]

#ikey=[.5, 9999, .5, 1]
#illfracrange=(.4, 1.)#(.7, .95)
#darkfracrange=(.4, 1.)#(.7, .95)
#ykeys=['I(A)']
#xkeys=['t(s)', 'Ewe(V)']
 
def calcdiff_choppedill(d, ikey='Illum', ykeys=['I(A)'], xkeys=['t(s)', 'Ewe(V)'], illfracrange=(.4, .95), darkfracrange=(.4, .95)):
    if isinstance(ikey, list) or isinstance(ikey, numpy.ndarray):
        lv_dark, lv_ill, lv_duty, lv_period=ikey
        illum=numpy.zeros(len(d['t(s)']), dtype='bool')
        indsill=numpy.where((d['t(s)']>lv_dark)&(d['t(s)']<=lv_ill))[0]
        till=d['t(s)'][indsill]
        till-=till[0]
        cycfrac=(till%lv_period)/lv_period
        illum[indsill[cycfrac<=lv_duty]]=1
        d['Illumcalc']=illum
    else:
        illum=d[ikey]!=0
    istart_len_calc=lambda startind, endind, fracrange: (startind+numpy.floor(fracrange[0]*(endind-startind)), numpy.ceil((fracrange[1]-fracrange[0])*(endind-startind)))
    riseinds=numpy.where(illum[1:]&numpy.logical_not(illum[:-1]))[0]+1
    fallinds=numpy.where(numpy.logical_not(illum[1:])&illum[:-1])[0]+1
    if len(fallinds)<2 or len(riseinds)==0:
        print 'insufficint light cycles'
    riseinds=riseinds[riseinds<fallinds[-1]]#only consider illum if there is a dark before and after
    fallinds=fallinds[fallinds>riseinds[0]]
    if len(fallinds)<2 or len(riseinds)==0:
        print 'insufficint light cycles'

    ill_istart, ill_len=istart_len_calc(riseinds, fallinds, illfracrange)
    darkstart, darkend=numpy.where(numpy.logical_not(illum))[0][[0, -1]]
    dark_istart, dark_len=istart_len_calc(numpy.concatenate([[darkstart], fallinds]), numpy.concatenate([riseinds, [darkend]]), darkfracrange)


    #inds_ill=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(ill_istart, ill_len)]
    #inds_dark=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(dark_istart, dark_len)]

    indstemp=[(range(int(i0ill), int(i0ill+ilenill)), range(int(i0dark), int(i0dark+ilendark))) for i0ill, ilenill, i0dark, ilendark in zip(ill_istart, ill_len, dark_istart, dark_len) if ilenill>0 and ilendark>0]
    inds_ill=map(operator.itemgetter(0), indstemp)
    inds_dark=map(operator.itemgetter(1), indstemp)
    if dark_len[-1]>0:
        inds_dark+=[range(int(dark_istart[-1]), int(dark_istart[-1]+dark_len[-1]))]
    else:
        inds_ill=inds_ill[:-1]

    d['inds_ill']=inds_ill
    d['inds_dark']=inds_dark

    getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_ill])
    getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_dark])

    for k in xkeys+ykeys:
        d[k+'_ill']=getillvals(d[k])
        d[k+'_dark']=getdarkvals(d[k])
    for k in ykeys:
        d[k+'_illdiff']=d[k+'_ill']-0.5*(d[k+'_dark'][:-1]+d[k+'_dark'][1:])
        d[k+'_illdiffmean']=numpy.mean(d[k+'_illdiff'])
        d[k+'_illdiffstd']=numpy.std(d[k+'_illdiff'])

calcdiff_choppedill(d, ikey=[.5, 9999, .5, 1], illfracrange=(0.2, .9), darkfracrange=(0.2, .9))
k='I(A)'
darkbaseline=d[k+'_dark'].mean()
illwrtdark=d[k+'_illdiff']+darkbaseline
iseg=numpy.argmax(d['Ewe(V)'])
pylab.plot(d['Ewe(V)'][:iseg+1], d['I(A)'][:iseg+1], 'g-')
pylab.plot(d['Ewe(V)'][iseg:], d['I(A)'][iseg:], 'g--')

#pylab.plot(d['t(s)_ill'], d[k+'_ill'], 'c_')
#pylab.plot(d['t(s)_dark'], d[k+'_dark'], 'b_')
#for inds in d['inds_ill']:
#    pylab.plot(d['t(s)'][inds], d['I(A)'][inds], 'm.')
#for inds in d['inds_dark']:
#    pylab.plot(d['t(s)'][inds], d['I(A)'][inds], 'k.')
    
#pylab.plot([min(d['t(s)']), max(d['t(s)'])], [darkbaseline, darkbaseline], '-', color=(.5, .5, .5))
iseg2=numpy.argmax(d['Ewe(V)_ill'])
pylab.plot(d['Ewe(V)_ill'], d[k+'_illdiff'], 'ro')
pylab.plot(d['Ewe(V)_ill'][:iseg2+1], d[k+'_illdiff'][:iseg2+1], 'r-')
pylab.plot(d['Ewe(V)_ill'][iseg2:], d[k+'_illdiff'][iseg2:], 'r--')
pylab.twinx()
#pylab.plot(d['t(s)'], d['Illum'], 'y-')
#pylab.plot(d['t(s)'], d['Illumcalc'], 'y-')
#pylab.plot(d['t(s)'], d['Illumcalc'], 'y.')
#pylab.show()


pylab.figure()

pylab.plot(d['t(s)'], d['I(A)'], 'k-')
pylab.plot(d['t(s)'], d['I(A)'], 'k.')
pylab.twinx()
pylab.plot(d['t(s)'], d['Illumcalc'], 'y-')
pylab.plot(d['t(s)'], d['Illumcalc'], 'y.')

#pylab.figure()
##d={}
##d['t(s)']=numpy.arange(100)/10.
#ikey=[1, 9999, .5, 2]
#lv_dark, lv_ill, lv_duty, lv_period=ikey
#illum=numpy.zeros(len(d['t(s)']), dtype='bool')
#indsill=numpy.where((d['t(s)']>lv_dark)&(d['t(s)']<=lv_ill))[0]
#till=d['t(s)'][indsill]
#till-=till[0]
#cycfrac=(till%lv_period)/lv_period
#illum[indsill[cycfrac<=lv_duty]]=1
#
#pylab.plot(d['t(s)'], illum, 'k-')
#pylab.ylim([-.1, 1.1])
pylab.show()
