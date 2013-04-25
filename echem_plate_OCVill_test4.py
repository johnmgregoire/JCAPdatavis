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

echemvis.expmntLineEdit.setText('OCV0')

echemvis.get_techniquedictlist(nfiles=1)

dlist=echemvis.techniquedictlist

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
 
def calcdiff_stepill(d, ikey='Illum', ykeys=['Ewe(V)'], xkeys=['t(s)', 'I(A)'], illfracrange=(.4, .95), darkfracrange=(.4, .95)):
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
    
    if len(fallinds)==0 and len(riseinds)==0:
        print 'insufficint light cycles'
        
    if illum[0]:
        illstart=0
        illend=fallinds[0]
        darkstart=fallinds[0]
        if len(riseinds)==0:
            darkend=len(illum)
        else:
            darkend=riseinds[0]
    else:
        darkstart=0
        darkend=riseinds[0]
        illstart=riseinds[0]
        if len(fallinds)==0:
            illend=len(illum)
        else:
            illend=fallinds[0]

    ill_istart, ill_len=istart_len_calc(illstart, illend, illfracrange)
    dark_istart, dark_len=istart_len_calc(darkstart, darkend, darkfracrange)

    inds_ill=[range(int(ill_istart), int(ill_istart+ill_len))]
    inds_dark=[range(int(dark_istart), int(dark_istart+dark_len))]


    d['inds_ill']=inds_ill
    d['inds_dark']=inds_dark

    getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_ill])
    getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_dark])

    for k in xkeys+ykeys:
        d[k+'_ill']=getillvals(d[k])
        d[k+'_dark']=getdarkvals(d[k])
    for k in ykeys:
        d[k+'_illdiffmean']=d[k+'_ill'][0]-d[k+'_dark'][0]
        d[k+'_illdiff']=numpy.array(d[k+'_illdiffmean'])


calcdiff_stepill(d, ikey=[5., 9999, 1, 9999], ykeys=['Ewe(V)'], xkeys=['t(s)', 'I(A)'], illfracrange=(0.7, 1.), darkfracrange=(0.7, 1.))
k='Ewe(V)'
darkbaseline=d[k+'_dark'].mean()
illwrtdark=d[k+'_illdiff']+darkbaseline
pylab.plot(d['t(s)'], d[k], 'g-')
pylab.plot(d['t(s)'], d[k], 'g.')
pylab.plot(d['t(s)_ill'], d[k+'_ill'], 'c_')
pylab.plot(d['t(s)_dark'], d[k+'_dark'], 'b_')
for inds in d['inds_ill']:
    pylab.plot(d['t(s)'][inds], d[k][inds], 'm.')
for inds in d['inds_dark']:
    pylab.plot(d['t(s)'][inds], d[k][inds], 'k.')
    
pylab.plot([min(d['t(s)']), max(d['t(s)'])], [darkbaseline, darkbaseline], '-', color=(.5, .5, .5))
pylab.plot(d['t(s)_ill'], illwrtdark, 'ro')
pylab.twinx()
#pylab.plot(d['t(s)'], d['Illum'], 'y-')
pylab.plot(d['t(s)'], d['Illumcalc'], 'y-')
pylab.plot(d['t(s)'], d['Illumcalc'], 'y.')
#pylab.show()


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
