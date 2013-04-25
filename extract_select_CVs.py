import time, copy
import os, os.path
import sys
import numpy
from echem_plate_fcns import *
from echem_plate_math import *

p1='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate1_test21Aug2012'
p2='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate3_test22Aug2012'
p3='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012/2012-9_NiLaCoCePlate1'
p4='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/DropEchem_Aug28_Sep14_2012/2012-9_NiLaCoCePlate2'

def pgen(fold, sl):
    fns=os.listdir(fold)
    pl=[]
    for s in sl:
        foundfn=None
        for fn in fns:
            if 'Sample%d_' %s in fn and 'CV2' in fn:
                foundfn=fn
                break
        if foundfn is None:
            print s, 'not found in', fold
            pl+=['']
        else:
            pl+=[os.path.join(fold, foundfn)]
    return pl

#fold_sl_pl=[(p1, [1996, 2067, 915], []), (p2, [6330, 5348, 6273, 6324], []), (p3, [999, 2084, 57, 3], []), (p4, [2942], [])]
fold_sl_pl=[(p3, [100, 605, 1100, 1605], []), (p4, [2215, 2605, 3100, 3605], [])]
#fold_sl_pl=[(p3, [100, 605], [])]
for fold, sl, pl in fold_sl_pl:
    pl+=pgen(fold, sl)

dlist=[]
for fold, sl, pl in fold_sl_pl:
    for sl, p in zip(sl, pl):
        d=readechemtxt(p)
        d['platename']=os.path.split(fold)[1]
        dlist+=[d]

calcsegind_dlist(dlist)
SegSG_dlist(dlist, SGpts=15, order=2, k='I(A)')
SegSG_dlist(dlist, SGpts=15, order=1, k='Ewe(V)')

for d in dlist:
    pylab.figure()
    ax=pylab.subplot(111)
    for segd in d['segprops_dlist']:
        if segd['rising']:
            st='-'
            #ax2=pylab.twinx()
            inds2=numpy.where(d['I(A)_SG'][segd['inds']]>2.e-6)
            #ax2.plot(d['Ewe(V)_SG'][segd['inds']][inds2], numpy.log10(1000.*d['I(A)_SG'][segd['inds']][inds2]), 'r'+st)
        else:
            st=':'
        ax.plot(d['Ewe(V)_SG'][segd['inds']], 1000.*d['I(A)_SG'][segd['inds']], 'g'+st, linewidth=3)
        ax.plot(d['Ewe(V)'][segd['inds']], 1000.*d['I(A)'][segd['inds']], 'b'+st)
        
    pylab.title('%s,  Sample%d' %(d['platename'], d['Sample']) + ', '+''.join(['%s%.2f' %elc for elc in zip(['Ni', 'La', 'Co', 'Ce'], d['compositions'])]))
    ax.set_xlabel('E vs Ag/AgCl')
    ax.set_ylabel('I(mA)')
    #ax2.set_ylabel('log10 I(mA), rising, I>0.002mA')
pylab.show()
