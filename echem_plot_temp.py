
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

#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/results/plate1/NiFeCoAl-F-Plate1_dlist.dat'
#f=open(p, mode='r')
#dlist=pickle.load(f)
#f.close()

#smp=numpy.array([d['Sample'] for d in dlist])
#i=numpy.where(smp==52)[0]
#d=dlist[i]

if 1:
    p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/20121029NiFeCoAl-F-Plate1/Sample52_x109_y69_Ni70Fe30Co0Al0_CP1.txt'
    d1=readechemtxt(p)

    p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20121108NiFeCoAl_F/20121025NiFeCoAl-F-Plate3/Sample5838_x31_y19_Ni10Fe17Co13Al60_CP1.txt'
    d2=readechemtxt(p)

    pylab.rc('font', family='serif', serif='Times New Roman', size=12)

    fig=pylab.figure(figsize=(3.5, 2.4))

    ax1=fig.add_axes((.2, .21, .74, .72))
    ax1.plot(d1['t(s)'], d1['Ewe(V)']-.2, 'b-', linewidth=1.2)
    ax1.plot(d2['t(s)'], d2['Ewe(V)']-.2, 'g-', linewidth=1.2)


    #ax1.set_xlim((-.1, .6))
    ax1.set_ylim((0, .4))

    #ax1.plot([.45, .45], ax1.get_ylim(), 'k--', linewidth=.8)

    ax1.set_xlabel('time at 0.1 mA (s)', fontsize=14)
    ax1.set_ylabel('Potential (V vs H$_2$O/O$_2$)', fontsize=14)

    pylab.show()

if 1:
    #smpstr='Sample659_x42_y50_A57B33C7D3'
    #smpstr='Sample647_x17_y50_A60B23C13D3'
    smpstr='Sample1009_x103_y40_A7B63C27D3'
    p=('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-12-03-surface area/%s' %smpstr)+'_CV%d.txt'
    
    
    dlist=[readechemtxt(p %i) for i in [1, 2, 3, 4, 5]]
    
    pylab.rc('font', family='serif', serif='Times New Roman', size=12)

    fig=pylab.figure(figsize=(3.5, 2.4))

    ax1=fig.add_axes((.2, .21, .74, .72))
    for d in dlist:
        i=len(d['I(A)'])//2
        ax1.plot(d['Ewe(V)'][-i:]-.2, d['I(A)'][-i:]*1.e6, linewidth=1.2)
    
    
    ax1.set_xlabel('Potential (V vs H$_2$O/O$_2$)', fontsize=14)
    ax1.set_ylabel('Current($\mu$A)', fontsize=14)
pylab.show()
