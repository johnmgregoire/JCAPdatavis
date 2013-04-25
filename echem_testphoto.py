import time, copy
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy import optimize
from echem_plate_ui import *
from echem_plate_math import *


homepath='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20130301_CuZnSnFe_Plate3_3654'

    
mainapp=QApplication(sys.argv)
form=MainMenu(None, execute=False, folderpath=homepath)

echemvis=form.echem



echemvis.expmntComboBox.setCurrentIndex(2)
echemvis.expmntLineEdit.setText('CA5')
echemvis.fillcalcoptions(batchmode=True)
echemvis.calcoptionComboBox.setCurrentIndex(3)

echemvis.get_techniquedictlist(nfiles=1)

techdict=echemvis.techniquedictlist[0]

echemvis.CalcParams=[0.4, 0.95, 0.4, 0.95, 'Ece(V)', 0.0, 0.8, 1]
echemvis.calckeys=['Illum', 'I(A)', 'Ewe(V)', 't(s)']

ikey=echemvis.CalcParams[4]
tshift=echemvis.CalcParams[5]
if tshift!=0:
    newikey='IllumMod'
    techdict[newikey]=illumtimeshift(techdict, ikey, echemvis.calckeys[3], tshift)
    ikey=newikey
    if echemvis.CalcParams[7]!=0:
        techdict[ikey]*=-1
elif echemvis.CalcParams[7]!=0:
    newikey='IllumMod'
    techdict[newikey]=-1*techdict[ikey]
    ikey=newikey
print ikey
            
            
err=calcdiff_ill_caller(techdict, ikey=ikey, thresh=echemvis.CalcParams[6], ykeys=[echemvis.calckeys[1]], xkeys=list(echemvis.calckeys[2:]), illfracrange=(echemvis.CalcParams[0], echemvis.CalcParams[1]), darkfracrange=(echemvis.CalcParams[2], echemvis.CalcParams[3]))

