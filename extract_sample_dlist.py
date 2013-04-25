
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

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121101NiFeCoTi_P_plate3_dlist.dat'#20121031NiFeCoTi_P_plate2_dlist.dat'
#savep='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate3_dlist_5742.pck'
#sample=5742

p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121101NiFeCoTi_P_plate3_dlist.dat'#20121031NiFeCoTi_P_plate2_dlist.dat'
savep='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate3_dlist_5838.pck'
sample=5838

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/20121031NiFeCoTi_P_plate1_dlist.dat'#
#savep='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate1_dlist_52.pck'
#sample=52


f=open(p, mode='r')
dlist=pickle.load(f)
f.close()

##filter dlist
smpl=[d['Sample'] for d in dlist]
i=smpl.index(sample)

d=dlist[i]

if 1:
    f=open(savep, mode='w')
    pickle.dump(d, f)
    f.close()
