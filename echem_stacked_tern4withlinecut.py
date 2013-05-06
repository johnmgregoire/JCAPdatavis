import matplotlib.cm as cm
import numpy, pickle
import pylab
import h5py, operator, copy, os, csv, sys
from echem_plate_fcns import *
from echem_plate_math import *

PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_stackedtern30 import *
from quaternary_FOM_bintern import *
#os.chdir(cwd)

pylab.rc('font', family='serif', serif='Times New Roman')

elkeys=['A', 'B', 'C', 'D']
SYSTEM=70
#29,34,39
pointsize=20
opacity=.6
view_azim=-159
view_elev=30
labelquat=True
#permuteelements=[1, 2, 0, 3]
permuteelements=[0, 1, 2, 3]
allposn=True
linedpath=None
if SYSTEM==0:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop')
    rootstr='20120728NiFeCoTiplate'
    #expstr='CV2V_Ithresh'
    #fomlabel='Potential for 0.1mA (V vs H$_2$0/O$_2$)'
    #fomshift=-.2
    #vmin=.3
    #vmax=.6
    fommult=1.
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTi_allplateresults'
    binarylegloc=1
elif SYSTEM==1:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop')
    rootstr='20120728NiFeCoTiplate'
    expstr='CP1Ess'
    fomlabel='Potential for 0.02mA (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.21
    vmax=.44
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.5'
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTi_allplateresults'
    binarylegloc=9
elif SYSTEM==2:
    ellabels=['Ni', 'La', 'Co', 'Ce']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012_results')
    rootstr='2012-9_NiLaCoCe'
    expstr='CV2Imax'
    fomlabel='max I in CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.03
    vmax=.54
    cmap=cm.jet
    aboverangecolstr='.5'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=1
elif SYSTEM==222:
    ellabels=['Ni', 'La', 'Co', 'Ce']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012_results')
    rootstr='2012-9_NiLaCoCe'
    expstr='CP4Ess'
    fomlabel='Potential for 0.1mA (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.34
    vmax=.44
    cmap=cm.jet_r
    aboverangecolstr='.5'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=1
elif SYSTEM==3:
    ellabels=['Fe', 'Ni', 'Zr', 'Ga']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012_results')
    rootstr='2012-08_FeNiZrGa'
    expstr='CP1Ess'
    fomlabel='Potential for 0.02mA (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.2
    vmax=.6
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.5'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=9
elif SYSTEM==4:
    ellabels=['Fe', 'Ni', 'Mg', 'Zr']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012_results')
    rootstr='2012-8_FeNiMgZr'
    expstr='CP1Ess'
    fomlabel='Potential for 0.02mA (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.2
    vmax=.6
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.5'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=9
elif SYSTEM==5:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012_results')
    rootstr='2012-9_FeCoNiTi500'
    expstr='CV2Imax'
    fomlabel='max I in CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.01
    vmax=.17
    cmap=cm.jet
    aboverangecolstr='.5'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==6:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi500'
    expstr='CV2V_Ithresh'
    fomlabel='V to reach 2E-5 A in CV (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.35
    vmax=.45
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), rootstr)
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==7:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi500C_fastCV'
    expstr='CV2V_Ithresh'
    fomlabel='V to reach 2E-5 A in CV (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.35
    vmax=.65
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==8:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fastinit_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    expstr='I500mVoverpotLinSub'
    fomlabel='I at 500mV in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.03
    vmax=.3
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.getcwd()#os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==9:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    expstr='V_IthreshCVLinSub'
    fomlabel='V to reach 1E-4 A in CV (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.42
    vmax=.6
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==10:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fastCP_plate1'
    expstr='CP1Ess'
    fomlabel='V from CP at 1E-4 A (V vs H$_2$0/O$_2$)'
    fomshift=-.24
    fommult=1.
    vmin=.42
    vmax=.6
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==11:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    rootstr='2012-9_FeCoNiTi_500C_fast_'
    os.chdir(os.path.join('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/'))
    expstr='I500mVoverpotLinSub'
    fomlabel='I at 500mV in LinSub CV ($\mu$A)'
    fomshift=0.
    fommult=1.e6
    vmin=30.
    vmax=252.
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_graphs1'
    binarylegloc=1
    elkeys=ellabels
    allposn=False
    view_azim=-40
    view_elev=2

elif SYSTEM==12:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    rootstr='2012-9_FeCoNiTi_500C_fastrep2_plate1'
    os.chdir(os.path.join('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/', rootstr))
    expstr='I500mVoverpotLinSub'
    fomlabel='I at 500mV in LinSub CV (mA)'
    fomshift=0.
    fommult=1.e6
    vmin=30.
    vmax=252.
    cmap=cm.jet
    aboverangecolstr=''
    belowrangecolstr='.3'
    savefolder=os.getcwd()#os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==13:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    rootstr='2012-9_FeCoNiTi_500C_fastrep3_plate1'
    os.chdir(os.path.join('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/', rootstr))
    expstr='I500mVoverpotLinSub'
    fomlabel='I at 500mV in LinSub CV (mA)'
    fomshift=0.
    fommult=1.e6
    vmin=30.
    vmax=252.
    cmap=cm.jet
    aboverangecolstr=''
    belowrangecolstr='.3'
    savefolder=os.getcwd()#os.path.join(os.getcwd(), '2012-9_FeCoNiTi500')
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==14:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    os.chdir(os.path.join('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/', rootstr))
    expstr='I500mVoverpotLinSub'
    fomlabel='I at 500mV in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.03
    vmax=.3
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_graphs2'
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==15:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    expstr='E_dIdEcrit'
    fomlabel='V to reach 5E-4 mA/V in CV (V vs H$_2$0/O$_2$)'
    fomshift=-.24
    fommult=1.
    vmin=.36
    vmax=.505
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.getcwd()
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==16:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    expstr='dIdE_aveabovecrit'
    fomlabel='ave dI/dE above crit (mA/V)'
    fomshift=0.
    fommult=1000.
    vmin=.51
    vmax=2.15
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.getcwd()
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==17:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results/2012-9_FeCoNiTi_500C_fast_plate1')
    rootstr='2012-9_FeCoNiTi_500C_fast_plate1'
    expstr='dIdEmax'
    fomlabel='max dI/dE mA/V'
    fomshift=0.
    fommult=1000.
    vmin=.4
    vmax=15.52
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.getcwd()
    binarylegloc=1
    elkeys=ellabels
elif SYSTEM==20:
    ellabels=['Ni', 'Fe', 'Co', 'Al']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201210_results/20121002NiFeCoAl_CPCVill_Plate1')
    rootstr='20121002NiFeCoAl'
    expstr='CV5Imax'
    fomlabel='max I in CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.055
    vmax=2.2
    cmap=cm.jet
    aboverangecolstr='.5'
    belowrangecolstr='k'
    savefolder=os.path.join(os.path.split(os.getcwd())[0], rootstr)
    binarylegloc=1
    elkeys=['Fe', 'Ni', 'Ti', 'Co']
elif SYSTEM==21:
    ellabels=['Ni', 'Fe', 'Co', 'Al']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201210_results/20121002NiFeCoAl_CPCVill_Plate1')
    rootstr='20121002NiFeCoAl'
    expstr='CP1Ess'
    fomlabel='V from CP at 1E-4 A (V vs H$_2$0/O$_2$)'
    fomshift=-.24
    fommult=1.
    vmin=.22
    vmax=.502
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.path.split(os.getcwd())[0], rootstr)
    binarylegloc=1
    elkeys=['Fe', 'Ni', 'Ti', 'Co']
elif SYSTEM==22:
    ellabels=['Ni', 'Fe', 'Co', 'Al']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results')
    rootstr='plate'
    expstr='CP1Efin'
    fomlabel='V from CP at 1E-4 A (V vs H$_2$0/O$_2$)'
    fomshift=-.177
    fommult=1.
    vmin=.19
    vmax=.5
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Al']
elif SYSTEM==23:
    ellabels=['Ni', 'Fe', 'Co', 'Al']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results')
    rootstr='plate'
    expstr='V_IthreshCVLinSub'
    fomlabel='V to reach 1E-4A in LinSub CV (V vs H$_2$0/O$_2$)'
    fomshift=-.177
    fommult=1.
    vmin=.19
    vmax=.5
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Al']
elif SYSTEM==24:
    ellabels=['Ni', 'Fe', 'Co', 'Al']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results')
    rootstr='plate'
    expstr='ImaxCVLinSub'
    fomlabel='max I in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.3
    vmax=3.2
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Al']
elif SYSTEM==25:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='I650mVLinSub'
    fomlabel='I in LinSub CV at 650mV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.3
    vmax=2.9
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==26:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='ImaxCVLinSub'
    fomlabel='Imax in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.3
    vmax=2.9
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==27:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='CV6fwdImax'
    fomlabel='Imax in CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.3
    vmax=2.9
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']

elif SYSTEM==28:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='I677mVLinSub'
    fomlabel='I at 500mV (O2/H2O) in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.1
    vmax=2.15
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    
elif SYSTEM==29:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='I627mVLinSub'
    fomlabel='$J_\mathrm{C}$ at $V_{OER}$ = 450mV (mA cm$^{-2}$)'
    fomshift=0.
    fommult=1.e5
    vmin=2
    vmax=101.3
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    view_azim=214
    view_elev=24

elif SYSTEM==30:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='I577mVLinSub'
    fomlabel='I at 400mV (O2/H2O) in LinSub CV (mA)'
    fomshift=0.
    fommult=1000.
    vmin=.02
    vmax=.3
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    
elif SYSTEM==31:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='V_IthreshCVLinSub_100'
    fomlabel='V to reach 1E-4A in LinSub CV (V vs H$_2$0/O$_2$)'
    fomshift=-.177
    fommult=1.
    vmin=.37
    vmax=.511
    cmap=cm.jet_r
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']

elif SYSTEM==32:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='V_IthreshCVLinSub_200'
    fomlabel='V to reach 2E-4A in LinSub CV (V vs H$_2$0/O$_2$)'
    fomshift=-.177
    fommult=1.
    vmin=.385
    vmax=.511
    cmap=cm.jet_r
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==33:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_T_400_925'
    fomlabel='frac Trans from 400-925nm'
    fomshift=0.
    fommult=1.
    vmin=.2#.16
    vmax=1.006#1.005
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==34:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am1.5'
    #fomlabel='frac AM1.5 en trans from 400-925nm'
    fomlabel='$\eta_{\mathrm{C},T}$ , transmission efficiency'
    fomshift=0.
    fommult=1.
    vmin=.19
    vmax=1.01
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    view_azim=214
    view_elev=24
    
elif SYSTEM==35:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__I677mV'
    fomlabel='frac TransEn AM1.5 400-925nm * curr at 500mV overpot.'
    fomshift=0.
    fommult=1000.
    vmin=.1
    vmax=1.78
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==36:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__I627mV'
    fomlabel='frac TransEn AM1.5 400-925nm * curr at 450mV overpot.'
    fomshift=0.
    fommult=1000.
    vmin=.01
    vmax=.9
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==37:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__I577mV'
    fomlabel='frac TransEn AM1.5 400-925nm * curr at 400mV overpot.'
    fomshift=0.
    fommult=1000.
    vmin=.01
    vmax=0.28
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==38:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__0.3cutI627mV'
    fomlabel='frac TransEn AM1.5 400-925nm * frac of 0.3mA at 450mV overpot.'
    fomshift=0.
    fommult=1.
    vmin=.1
    vmax=1.01
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
elif SYSTEM==39:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__0.23cutI627mV'
    #fomlabel='frac TransEn AM1.5 400-925nm * frac of 0.23mA at 450mV overpot.'
    fomlabel='$\eta_{\mathrm{C}}$ , catalytic and optical efficiency'
    fomshift=0.
    fommult=1.
    vmin=.1
    vmax=1.01
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    view_azim=214
    view_elev=24
elif SYSTEM==40:
    ellabels=['Ni', 'Fe', 'Co', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results')
    rootstr='plate'
    expstr='UVvis_Ten_400_925_am15__0.1cutI577mV'
    fomlabel='frac TransEn AM1.5 400-925nm * frac of 0.1mA at 400mV overpot.)'
    fomshift=0.
    fommult=1.
    vmin=.1
    vmax=1.01
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ti']
    
elif SYSTEM==41:
    ellabels=['Bi', 'V', 'Ni', 'Fe']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results')
    rootstr='.txt'
    expstr='CA5Iphoto'
    fomlabel='photocurrent Fe2/3 shorted to Pt (mA)'
    fomshift=0.
    fommult=1000.
    vmin=-.008
    vmax=.1
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Bi', 'V', 'Ni', 'Fe']
    
elif SYSTEM==42:
    ellabels=['Bi', 'V', 'Ni', 'Fe']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results')
    rootstr='.txt'
    expstr='OCV0Ephoto'
    fomlabel='illuminated OCV shift, in Fe2/3 wrt Pt (mV)'
    fomshift=0.
    fommult=1000.
    vmin=-70
    vmax=10
    cmap=cm.jet_r
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Bi', 'V', 'Ni', 'Fe']

elif SYSTEM==43:
    ellabels=['Bi', 'V', 'Ni', 'Fe']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results')
    rootstr='.txt'
    expstr='OCV0Ess'
    fomlabel='illuminated OCV in Fe2/3 wrt Pt (mV)'
    fomshift=0.
    fommult=1000.
    vmin=-20
    vmax=5
    cmap=cm.jet_r
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Bi', 'V', 'Ni', 'Fe']

elif SYSTEM==44:
    ellabels=['Bi', 'V', 'Ni', 'Fe']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/201212_BiVNiFe/results')
    rootstr='.txt'
    expstr='OCV0Efin'
    fomlabel='illuminated OCV in Fe2/3 wrt Pt (mV)'
    fomshift=0.
    fommult=1000.
    vmin=-80
    vmax=5
    cmap=cm.jet_r
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)
    binarylegloc=1
    elkeys=['Bi', 'V', 'Ni', 'Fe']
elif SYSTEM==45:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/NiFeCoCe plates 1M NaOH/results')
    rootstr='201304'
    expstr='CP1Efin'
    fomlabel='V for 10 mA/cm$^2$ (V vs H$_2$0/O$_2$)'
    fomshift=-.187
    fommult=1.
    vmin=.33
    vmax=.43
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='.3'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']    
elif SYSTEM==46:
    ellabels=['Ni', 'Fe', 'Co', 'La']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results')
    rootstr=''
    expstr='ImaxCVLinSub'
    fomlabel='max I (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=2
    vmax=165
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'La']
elif SYSTEM==47:
    ellabels=['Ni', 'Fe', 'Co', 'La']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results')
    rootstr='_I350mVLinSub.txt'
    expstr='I350mVLinSub'
    fomlabel='I at 350mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=30
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'La']
elif SYSTEM==48:
    ellabels=['Ni', 'Fe', 'Co', 'La']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoLa/results')
    rootstr='_I400mVLinSub.txt'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=100
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'La']    
    


elif SYSTEM==50:
    ellabels=['Ni', 'Fe', 'Ce', 'La']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results')
    rootstr='_I350mVLinSub.txt'
    expstr='I350mVLinSub'
    fomlabel='I at 350mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=30
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
elif SYSTEM==51:
    ellabels=['Ni', 'Fe', 'Ce', 'La']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCeLa/results')
    rootstr='_I400mVLinSub.txt'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=100
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==53:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_I350mVLinSub.txt'
    expstr='I350mVLinSub'
    fomlabel='I at 350mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=10
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
elif SYSTEM==54:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_I400mVLinSub.txt'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=42
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==55:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_V_IthreshCVLinSub_30.txt'
    expstr='V_IthreshCVLinSub_30'
    fomlabel='E for 3mA/cm$^2$ (mV vs E$_{OER}$)'
    fomshift=0.
    fommult=1000.
    vmin=280
    vmax=400
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==56:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_V_IthreshCVLinSub_100.txt'
    expstr='V_IthreshCVLinSub_100'
    fomlabel='E for 10mA/cm$^2$ (mV vs E$_{OER}$)'
    fomshift=0.
    fommult=1000.
    vmin=350
    vmax=440
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
elif SYSTEM==57:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_V_IthreshCVLinSub_300.txt'
    expstr='V_IthreshCVLinSub_300'
    fomlabel='E for 30mA/cm$^2$ (mV vs E$_{OER}$)'
    fomshift=0.
    fommult=1000.
    vmin=380
    vmax=440
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
elif SYSTEM==58:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_TafelSlopeVperdec.txt'
    expstr='TafelSlopeVperdec'
    fomlabel='Tafel mV/decade'
    fomshift=0.
    fommult=1000.
    vmin=25.
    vmax=105.
    cmap=cm.jet_r
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
elif SYSTEM==59:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_TafelLogExCurrent.txt'
    expstr='TafelLogExCurrent'
    fomlabel='Tafel Log$_{10}$ I$_{ex}$/A'
    fomshift=0.
    fommult=1.
    vmin=-18.
    vmax=-8.
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==60:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.04_plate123')
    linedpath='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.04_linedetails.dat'
    linedsmoothfcn=lambda x, y: scipy.interpolate.splev(x, scipy.interpolate.splrep(x=x, y=y, k=5, s=3000))
    rootstr='fom0.04'
    expstr='V_IthreshCVLinSub_100'
    fomlabel='E for 10mA/cm$^2$ (mV vs E$_{OER}$)'
    fomshift=0.
    fommult=1000.
    vmin=350
    vmax=440
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
    
elif SYSTEM==61:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.04_plate123')
    linedpath='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.04_linedetails.dat'
    #linedsmoothfcn=lambda x, y: savgolsmooth(y, nptsoneside=18, order = 2)
    linedsmoothfcn=lambda x, y: scipy.interpolate.splev(x, scipy.interpolate.splrep(x=x, y=y, k=5, s=3000))
    
    rootstr='fom0.04'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=42
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==62:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.06_plate123')
    linedpath='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.06_linedetails.dat'
    #linedsmoothfcn=lambda x, y: savgolsmooth(y, nptsoneside=12, order = 2)
    #linedsmoothfcn=lambda x, y: scipy.interpolate.UnivariateSpline(x=x, y=y, k=5)(x)
    linedsmoothfcn=lambda x, y: scipy.interpolate.splev(x, scipy.interpolate.splrep(x=x, y=y, k=5, s=3000))
    rootstr='fom0.06'
    expstr='I350mVLinSub'
    fomlabel='I at 350mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=10
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
    
elif SYSTEM==63:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.06_plate123')
    linedpath='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.06_linedetails.dat'
    linedsmoothfcn=lambda x, y: scipy.interpolate.splev(x, scipy.interpolate.splrep(x=x, y=y, k=5, s=3000))
    rootstr='fom0.06'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=42
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
    
elif SYSTEM==65:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/fom0.02_plate123')
    linedpath='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline0.02_linedetails.dat'
    linedsmoothfcn=lambda x, y: scipy.interpolate.splev(x, scipy.interpolate.splrep(x=x, y=y, k=5, s=3000))
    rootstr='fom0.02'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=42
    cmap=cm.jet
    aboverangecolstr='k'
    belowrangecolstr='pink'
    savefolder=os.path.join(os.getcwd(), expstr)
    binarylegloc=1
    elkeys=['Ni', 'Fe', 'Co', 'Ce']

elif SYSTEM==70:
    ellabels=['Ce', 'Fe', 'Co', 'Ni']
    os.chdir('C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results')
    rootstr='_I400mVLinSub.txt'
    expstr='I400mVLinSub'
    fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
    fomshift=0.
    fommult=100000.
    vmin=1
    vmax=42
    cmap=cm.jet
    aboverangecolstr='pink'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr+'_Ni')
    binarylegloc=1
    elkeys=['Ce', 'Fe', 'Co', 'Ni']
    
dpl=['', '', '']
for root, dirs, files in os.walk(os.getcwd()):
    testfn=[fn for fn in files if (rootstr in fn) and (expstr in fn)]
    for fn in testfn:
        for count in range(3):
            if ('late%d' %(count+1)) in fn:
                dpl[count]=os.path.join(root, fn)
            
print 'FOM file paths:'
for dp in dpl:
    print dp
    




dropdl=[]
for dp in dpl:
    if dp=='':
        dropdl+=[None]
        continue
    f=open(dp, mode='r')
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
    dropdl+=[dropd]




fig=pylab.figure(figsize=(9, 4.*len(dropdl)))
figquatall=[]
compsall=[]
fomall=[]
plateindall=[]
codeall=[]
for count, dropd in enumerate(dropdl):
    if dropd is None:
        continue
    print dropd.keys()
    #dropinds=numpy.arange(len(dropd['Sample']))
    try:
        dropd['compositions']=numpy.array([dropd[elkey] for elkey in elkeys]).T
    except:
        dropd['compositions']=numpy.array([dropd[elkey] for elkey in ['A', 'B', 'C', 'D']]).T
    
    unroundcompositions(dropd)
    addcodetoplatemapgen1dlist(dlist=None, dropd=dropd)
    
    dropinds=numpy.argsort(dropd['Sample'])
    dropinds=dropinds[numpy.logical_not(numpy.isnan(dropd[expstr][dropinds]))]
    x=dropd['x(mm)'][dropinds]
    y=dropd['y(mm)'][dropinds]

    fom=(dropd[expstr][dropinds]+fomshift)*fommult
    
    comp=dropd['compositions'][dropinds]
    code=dropd['code'][dropinds]
    
    compsall+=list(comp)
    fomall+=list(fom)
    plateindall+=[count]*len(fom)
    codeall+=list(code)
    
    
    comp=numpy.array([a/a.sum() for a in comp])
    
    if allposn:
        codeinds=numpy.where(code!=1)
    else:
        codeinds=numpy.where(code==0)
    comp=comp[codeinds]
    fom=fom[codeinds]
    x=x[codeinds]
    y=y[codeinds]
    
    clip=True
        
    for fcn, vstr in zip([cmap.set_over, cmap.set_under], [aboverangecolstr, belowrangecolstr]):
        if len(vstr)==0:
            continue
        c=col_string(vstr)
        fcn(c)
        clip=False
    norm=colors.Normalize(vmin=vmin, vmax=vmax, clip=clip)
    print 'fom min, max, mean, std:', fom.min(), fom.max(), fom.mean(), fom.std()
    if numpy.any(fom>vmax):
        if numpy.any(fom<vmin):
            extend='both'
        else:
            extend='max'
    elif numpy.any(fom<vmin): 
        extend='min'
    else:
        extend='neither'


    #ax=pylab.subplot(211)
    #ax2=pylab.subplot(212)
    #pylab.subplots_adjust(left=.03, right=.97, top=.97, bottom=.03, hspace=.01)

    ax2=fig.add_subplot(len(dropdl), 1, count+1)
    ax2.set_aspect(1)
    mapbl=ax2.scatter(x, y, c=fom, s=60, marker='s', edgecolors='none', cmap=cmap, norm=norm)
    ax2.set_xlim(x.min()-2, x.max()+2)
    ax2.set_ylim(y.min()-2, y.max()+2)
    ax2.set_title('plate %d' %(count+1))
    #pylab.title('CP1Ess (V) Map')
    

    figquat=pylab.figure(figsize=(8, 8))
    stp = QuaternaryPlot(111, minlist=[0., 0., 0., 0.], ellabels=ellabels)

    stp.scatter(comp, c=fom, s=pointsize, edgecolors='none', cmap=cmap, norm=norm)

    stp.label(ha='center', va='center', fontsize=20)

    stp.set_projection(azim=view_azim, elev=view_elev)
    caxquat=figquat.add_axes((.83, .3, .04, .4))
    cb=pylab.colorbar(stp.mappable, cax=caxquat, extend=extend)
    cb.set_label(fomlabel, fontsize=16)
    stp.ax.set_title('plate %d' %(count+1))

    figquatall+=[figquat]
compsall=numpy.array(compsall)
fomall=numpy.array(fomall)
plateindall=numpy.array(plateindall)
codeall=numpy.array(codeall)
code0inds=numpy.where(codeall==0)
code02inds=numpy.where(codeall!=1)
code2inds=numpy.where(codeall==2)


if not permuteelements is None:
    ellabels=[ellabels[i] for i in permuteelements]
    compsall=compsall[:, permuteelements]


#fomall[fomall<0.3]=0.

if numpy.any(fomall>vmax):
    if numpy.any(fomall<vmin):
        extend='both'
    else:
        extend='max'
elif numpy.any(fomall<vmin): 
    extend='min'
else:
    extend='neither'
        
fig.subplots_adjust(left=.05, bottom=.03, top=.96, right=.83, hspace=.14)
cax=fig.add_axes((.85, .3, .04, .4))
cb=pylab.colorbar(mapbl, cax=cax, extend=extend)
cb.set_label(fomlabel, fontsize=20)




axl, stpl=make10ternaxes(ellabels=ellabels)
pylab.figure(figsize=(8, 8))
stpquat=QuaternaryPlot(111, ellabels=ellabels)

#stpquat.scatter(compsall[code0inds], c=fomall[code0inds], s=20, edgecolors='none', cmap=cmap, norm=norm)
cols=stpquat.scalarmap(fomall[code0inds], norm, cmap)
stpquat.plotbycolor(compsall[code0inds], cols, marker='o', markersize=5, alpha=.3)#, markeredgecolor=None
scatter_10axes(compsall[code0inds], fomall[code0inds], stpl, s=18, edgecolors='none', cmap=cmap, norm=norm)
if labelquat:
    stpquat.label(fontsize=20)

stpquat.set_projection(azim=view_azim, elev=view_elev)


axl30, stpl30=make30ternaxes(ellabels=ellabels)
scatter_30axes(compsall[code0inds], fomall[code0inds], stpl30, s=18, edgecolors='none', cmap=cmap, norm=norm)


axl_tern, stpl_tern=make4ternaxes(ellabels=ellabels)
scatter_4axes(compsall[code0inds], fomall[code0inds], stpl_tern, s=20, edgecolors='none', cmap=cmap, norm=norm)

axbin, axbininset=plotbinarylines_axandinset(linewidth=2, ellabels=ellabels)
plotbinarylines_quat(axbin, compsall[code0inds], fomall[code0inds], markersize=8, legloc=binarylegloc, ellabels=ellabels)
axbin.set_xlabel('binary composition', fontsize=16)
axbin.set_ylabel(fomlabel, fontsize=16)

figtemp=pylab.figure(stpquat.ax.figure.number)
cbax=figtemp.add_axes((.83, .3, .04, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
cb.set_label(fomlabel, fontsize=16)

figtemp=pylab.figure(axl[0].figure.number)
cbax=figtemp.add_axes((.85, .3, .04, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
cb.set_label(fomlabel, fontsize=16)

figtemp=pylab.figure(axl30[0].figure.number)
cbax=figtemp.add_axes((.91, .3, .03, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
cb.set_label(fomlabel, fontsize=18)

figtemp=pylab.figure(axl_tern[0].figure.number)
cbax=figtemp.add_axes((.9, .3, .03, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
cb.set_label(fomlabel, fontsize=16)

purelfig=pylab.figure()
linestyle=['-', '--', '-.', ':']
compsel=compsall[code2inds]
plateindel=plateindall[code2inds]
fomel=fomall[code2inds]
for count, col in enumerate(['c', 'm', 'y', 'k']):
    c_el=compsel[:, count]
    inds=numpy.where(c_el>0.)
    c_el=c_el[inds]
    cvl=list(set(c_el))
    cvl.sort()
    
    fom_el=fomel[inds]
    plate_inds=plateindel[inds]
    platefom_thick=[(plate_inds[c_el==cv], fom_el[c_el==cv]) for cv in cvl]

    for thickcount, ((plate, fom_plate), ls) in enumerate(zip(platefom_thick, linestyle)):
        indsp=numpy.argsort(plate)
        plate=plate[indsp]+1
        fom_plate=fom_plate[indsp]
        if count==3 or thickcount==0:
            pylab.plot(plate, fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13, label='%s,thick. %d' %(ellabels[count], thickcount+1))
#        elif thickcount==0:
#            pylab.plot([1, 2, 3], fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13, label='%s' %(ellabels[count],) )
        else:
            pylab.plot(plate, fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13)
pylab.xlim(.7, 4.3)
pylab.xlabel('plate number', fontsize=16)
pylab.ylabel(fomlabel, fontsize=16)
pylab.title('PURE ELEMENTS. color=element(CMYK). #=thickness', fontsize=18)
pylab.legend(loc=1)

if linedpath is None:
    axlinepar=None
else:
    f=open(linedpath, mode='r')
    lined=pickle.load(f)
    f.close()
    pylab.figure()
    lp=lined['lineparameter'][code0inds]
#    lp[lp<0.]=0.
#    lp[lp>1.]=1.
    fom=fomall[code0inds]
    argsinds=numpy.argsort(lp)
    pylab.plot(lp[argsinds], fom[argsinds], 'b-')
    pylab.plot(lp[argsinds], fom[argsinds], 'bo')
    if not linedsmoothfcn is None:
        fomsmooth=linedsmoothfcn(lp[argsinds], fom[argsinds])
        pylab.plot(lp[argsinds], fomsmooth, 'k-')
    axlinepar=pylab.gca()
    lineparticks=numpy.linspace(0, 1, 4)
    tl=[]
    for i in lineparticks:
        c=lined['compend1']+(lined['compend2']-lined['compend1'])*i
        tl+=[stpquat.singlelabeltext(c)]
    pylab.xlim(0, 1)
    #pylab.ylim(vmin, vmax)
    axlinepar.xaxis.set_ticks(lineparticks)
    axlinepar.xaxis.set_ticklabels(tl)
    pylab.ylabel(fomlabel)


if SYSTEM==1:
    axbin.set_ylim(.23, .7)
if SYSTEM==6:
    axbin.set_ylim(.38, .5)

if not os.path.exists(savefolder):
    os.mkdir(savefolder)
os.chdir(savefolder)
if 1:
    pylab.figure(fig.number)
    pylab.savefig('%s_PlatesAll_Posn.png' %expstr)
    for count, fg in enumerate(figquatall):
        pylab.figure(fg.number)
        pylab.savefig('%s_Plate%d_Quat.png' %(expstr, count+1))
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat.png' %expstr)
    pylab.savefig('%s_PlatesAll_Quat.png' %expstr, dpi=600)
    
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern.png' %expstr)
    
    pylab.figure(axl30[0].figure.number)
    pylab.savefig('%s_stackedtern30.png' %expstr)
    
    pylab.figure(axl_tern[0].figure.number)
    pylab.savefig('%s_ternfaces.png' %expstr)
    
    pylab.figure(axbin.figure.number)
    pylab.savefig('%s_binaries.png' %expstr)
    
    pylab.figure(purelfig.number)
    pylab.savefig('%s_pureelements.png' %expstr)
    if not axlinepar is None:
        pylab.figure(axlinepar.figure.number)
        pylab.savefig('%s_compline.png' %expstr)
    
if 0:
    os.chdir(savefolder)
    pylab.figure(fig.number)
    pylab.savefig('%s_PlatesAll_Posn.eps' %expstr)
    for count, fg in enumerate(figquatall):
        pylab.figure(fg.number)
        pylab.savefig('%s_Plate%d_Quat.eps' %(expstr, count+1))
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat.eps' %expstr)
    pylab.savefig('%s_PlatesAll_Quat.svg' %expstr)
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern.eps' %expstr)
    
    pylab.figure(axl_tern[0].figure.number)
    pylab.savefig('%s_ternfaces.eps' %expstr)
    
    pylab.figure(axbin.figure.number)
    pylab.savefig('%s_binaries.eps' %expstr)
    
    pylab.figure(purelfig.number)
    pylab.savefig('%s_pureelements.eps' %expstr)

    if not axlinepar is None:
        pylab.figure(axlinepar.figure.number)
        pylab.savefig('%s_compline.eps' %expstr)
if 0:
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat_hires.png' %expstr, dpi=600)
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern_hires.png' %expstr, dpi=600)
pylab.show()
