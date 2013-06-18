import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *



SYSTEM=9
if SYSTEM==0:
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012'
    filterstr='2012-9_FeCoNiTi500'
if SYSTEM==1:
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201210'
    filterstr=''
if SYSTEM==2:
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F'
    filterstr=''
if SYSTEM==3:
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoAl_P'
    filterstr=''
if SYSTEM==4:    
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe'
    filterstr='201212_BiVNiFe'
if SYSTEM==5:
    homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/NiFeCoCe plates 1M NaOH'
    filterstr='201304'
if SYSTEM==6:
    homepath='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/'
    filterstr='20130605NiFeCoCe_plate1_CP_6220'
if SYSTEM==7:
    homepath='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/'
    filterstr='2013060607NiFeCoCe_plate1_CP3_6220'
if SYSTEM==8:
    homepath='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/'
    filterstr='2013040'
if SYSTEM==9:
    homepath='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321'
    filterstr='20130610NiFeCoCe_plate1_CP_6321'
    
mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=homepath)

echemvis=form.echem

def processplate(datafolder, savefolder, expmntindex=3, expmntstring='CV2', calcoptionindex=0, nfiles=99999, echemvis=echemvis, CalcParams=[], savedlist=False):
    echemvis.folderpath=datafolder

    echemvis.expmntComboBox.setCurrentIndex(expmntindex)
    echemvis.expmntLineEdit.setText(expmntstring)
    echemvis.fillcalcoptions(batchmode=True)
    echemvis.calcoptionComboBox.setCurrentIndex(calcoptionindex)
    if len(CalcParams)>0:
        echemvis.CalcParams=CalcParams
    echemvis.get_techniquedictlist(nfiles=nfiles)
    echemvis.CalcAllFOM()

    if not savefolder is None:
        echemvis.writefile(p=savefolder, savedlist=savedlist)



for fn in os.listdir(homepath):
    p=os.path.join(homepath, fn)
    if os.path.isdir(p) and filterstr in fn:
        print fn
        echemvis.folderpath=p
        #sf=os.path.join(homepath+'_results', fn.partition('late')[0][:-1])
        sf=os.path.join(homepath,'results')
        if not os.path.isdir(sf):
            os.mkdir(sf)
#        #CV2 and CV5
#        echemvis.expmntComboBox.setCurrentIndex(3)
#        for s in ['CV2', 'CV5']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=10)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=3, expmntstring=s, calcoptionindex=0)

#        #CP1 and CP4
#        echemvis.expmntComboBox.setCurrentIndex(1)
#        for s in ['CP1']:#, 'CP4']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=10)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=1, expmntstring=s, calcoptionindex=2, CalcParams=[1., 10.])

#        #CP1 and CP4 Efin
#        echemvis.expmntComboBox.setCurrentIndex(1)
#        for s in ['CP1']:#, 'CP4']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=10)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=1, expmntstring=s, calcoptionindex=0)
                
#        #CP1 and CP4 Ethresh
#        for s in ['CV2', 'CV5']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=10)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=3, expmntstring=s, calcoptionindex=2, CalcParams=[2.e-5, 10, 1, numpy.nan])

#        #photo
#        nfiles=10
#        echemvis.expmntComboBox.setCurrentIndex(0)
#        for s in ['OCV0']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=nfiles)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=0, expmntstring=s, calcoptionindex=3, CalcParams=[.7, .95, .7, .95])
#        echemvis.expmntComboBox.setCurrentIndex(3)
#        for s in ['CV3']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=nfiles)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=3, expmntstring=s, calcoptionindex=5, CalcParams=[.4, .95, .4, .95])
#        echemvis.expmntComboBox.setCurrentIndex(2)

#        for s in ['CA5']:
#            echemvis.expmntLineEdit.setText(s)
#            echemvis.get_techniquedictlist(nfiles=nfiles)
#            if len(echemvis.techniquedictlist)>8:
#                print s
#                processplate(p, sf, expmntindex=2, expmntstring=s, calcoptionindex=3, CalcParams=[.4, .95, .4, .95])
#        break

        #CPs Eave 20pts
        echemvis.expmntComboBox.setCurrentIndex(1)
        for s in ['CP4', 'CP5', 'CP6']:#
            echemvis.expmntLineEdit.setText(s)
            echemvis.get_techniquedictlist(nfiles=9999)
            print len(echemvis.techniquedictlist)
            if len(echemvis.techniquedictlist)>8:
                print s
                processplate(p, sf, expmntindex=1, expmntstring=s, calcoptionindex=1, CalcParams=[1, 2, 20, 1], savedlist=True)
