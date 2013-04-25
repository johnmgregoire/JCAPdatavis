
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

p1='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate1_dlist_52.pck'
#p2='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate3_dlist_5742.pck'
p2='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots/20121031NiFeCoTi_P_plate3_dlist_5838.pck'

os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121031NiFeCoTi_P/results/echemplots')

vshift=-.177
imult=1.e5
cai0, cai1=(0, 6500)



f=open(p1, mode='r')
d1=pickle.load(f)
f.close()

f=open(p2, mode='r')
d2=pickle.load(f)
f.close()


segd1up, segd1dn=d1['segprops_dlist']

i1up=d1['I(A)'][segd1up['inds']][4:]
lin1up=i1up-d1['I(A)_LinSub'][segd1up['inds']][4:]
v1up=d1['Ewe(V)'][segd1up['inds']][4:]+vshift
#i1dn=d1['I(A)'][segd1dn['inds']]
#v1dn=d1['Ewe(V)'][segd1dn['inds']]+vshift
i1up*=imult
#i1dn*=imult
lin1up*=imult

segd2up, segd2dn=d2['segprops_dlist']

i2up=d2['I(A)'][segd2up['inds']][4:]
lin2up=i2up-d2['I(A)_LinSub'][segd2up['inds']][4:]
v2up=d2['Ewe(V)'][segd2up['inds']][4:]+vshift
#i2dn=d2['I(A)'][segd2dn['inds']]
#v2dn=d2['Ewe(V)'][segd2dn['inds']]+vshift
i2up*=imult
#i2dn*=imult
lin2up*=imult


pylab.rc('font', family='serif', serif='Times New Roman', size=11)

fig=pylab.figure(figsize=(3.5, 2.4))
#ax1=pylab.subplot(211)
#ax2=pylab.subplot(212)
#ax1=fig.add_axes((.2, .6, .74, .35))
#ax2=fig.add_axes((.2, .11, .6, .35))
#ax3=ax2.twinx()
ax1=fig.add_axes((.2, .21, .74, .72))
ax1.plot(v1up, i1up, 'g-', linewidth=1.2)
ax1.plot(v1up, lin1up, 'g:', linewidth=1.)
#ax1.plot(v1dn, i1dn, 'g--', linewidth=1.)

ax1.plot(v2up, i2up, 'b-', linewidth=1.2)
ax1.plot(v2up, lin2up, 'b:', linewidth=1.)
#ax1.plot(v2dn, i2dn, 'b--', linewidth=1.)


ax1.set_xlim((-.1, .6))
ax1.set_ylim((-5, 120))

ax1.plot([.45, .45], ax1.get_ylim(), 'k--', linewidth=.8)

ax1.set_xlabel('Potential (V vs H$_2$O/O$_2$)', fontsize=12)
ax1.set_ylabel('Current density (mA cm$^{-2}$)', fontsize=12)

#ax2.plot(tca, ica, 'k-')
#ax2.plot(tca, icadiff, 'b--', linewidth=2)
#ax2.set_xlim((0, 6.5))
#ax2.set_ylim((0, 0.4))
#
#ax3.plot(tca_cycs, iphoto_cycs, 'ro-')
#ax3.set_ylim((0, 0.1))
#ax2.set_xlabel('Elapsed time (s)', fontsize=12)
#ax2.set_ylabel('Current ($\mu$A)', fontsize=12)
#ax3.set_ylabel('Photocurrent ($\mu$A)', fontsize=12)
pylab.show()

#print ''.join(['%s%.3f' %tup for tup in zip(dill['elements'], dill['compositions'])])
print ''.join(['%s%.3f' %tup for tup in zip(d1['elements'], d1['compositions'])])
print ''.join(['%s%.3f' %tup for tup in zip(d2['elements'], d2['compositions'])])
