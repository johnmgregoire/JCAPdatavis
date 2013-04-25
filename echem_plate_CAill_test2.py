import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *


p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/201212_BiVNiFe_plate1_4026'
os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results/')
mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=p)

echemvis=form.echem

echemvis.expmntLineEdit.setText('CA5')

echemvis.get_techniquedictlist(nfiles=2)

dlist=echemvis.techniquedictlist

d=dlist[0]

ikey='Illum'
ykeys=['I(A)']
xkeys=['t(s)', 'Ewe(V)']
illfracrange=(.4, .95)
darkfracrange=(.4, .95)


istart_len_calc=lambda startind, endind, fracrange: (startind+numpy.floor(fracrange[0]*(endind-startind)), numpy.ceil((fracrange[1]-fracrange[0])*(endind-startind)))
illum=d[ikey]!=0
riseinds=numpy.where(illum[1:]&numpy.logical_not(illum[:-1]))[0]+1
fallinds=numpy.where(numpy.logical_not(illum[1:])&illum[:-1])[0]
if len(fallinds)<2 or len(riseinds)==0:
    print 'insufficint light cycles'
riseinds=riseinds[riseinds<fallinds[-1]]#only consider illum if there is a dark before and after
fallinds=fallinds[fallinds>riseinds[0]]
if len(fallinds)<2 or len(riseinds)==0:
    print 'insufficint light cycles'
print '***'
ill_istart, ill_len=istart_len_calc(riseinds, fallinds, illfracrange)
darkstart, darkend=numpy.where(numpy.logical_not(illum))[0][[0, -1]]
dark_istart, dark_len=istart_len_calc(numpy.concatenate([[darkstart], fallinds]), numpy.concatenate([riseinds, [darkend]]), darkfracrange)


inds_ill=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(ill_istart, ill_len)]
inds_dark=[range(int(i0), int(i0+ilen)) for i0, ilen in zip(dark_istart, dark_len)]

getillvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_ill])
getdarkvals=lambda arr:numpy.array([arr[inds].mean() for inds in inds_dark])

for k in xkeys+ykeys:
    d[k+'_ill']=getillvals(d[k])
    d[k+'_dark']=getdarkvals(d[k])
for k in ykeys:
    d[k+'_illdiff']=d[k+'_ill']-0.5*(d[k+'_dark'][:-1]+d[k+'_dark'][1:])
    d[k+'_illdiffmean']=numpy.mean(d[k+'_illdiff'])
    d[k+'_illdiffstd']=numpy.std(d[k+'_illdiff'])
