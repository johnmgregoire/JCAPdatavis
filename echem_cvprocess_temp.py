import matplotlib.cm as cm
import numpy
import pylab
import h5py, operator, copy, os, csv, sys
from echem_plate_fcns import *

PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern import *

#os.chdir(cwd)


def myeval(c):
    if c=='None':
        c=None
    else:
        temp=c.lstrip('0')
        if (temp=='' or temp=='.') and '0' in c:
            c=0
        else:
            c=eval(temp)
    return c
    

ellabels=['Fe', 'Co', 'Ni', 'Ti']

os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop')
rootstr='20120728NiFeCoTiplate1'
#expstr='CV2V_Ithresh'
#fomlabel='Potential for 0.1mA (V vs H$_2$0/O$_2$)'
#fomshift=-.2
#vmin=.3
#vmax=.6

expstr='CV2'
fomlabel='Potential for 0.02mA (V vs H$_2$0/O$_2$)'
fomshift=-.2
vmin=.21
vmax=.45


cmap=cm.jet_r

aboverangecolstr='k'
belowrangecolstr=''


dpl=['', '', '']
for root, dirs, files in os.walk(os.getcwd()):
    testfn=[fn for fn in files if (rootstr in fn) and (expstr in fn)]
    for fn in testfn:
        for count in range(3):
            if ('plate%d' %(count+1)) in fn:
                dpl[count]=os.path.join(root, fn)
            
print 'FOM file paths:'
for dp in dpl:
    print dp
    


savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTi_allplateresults'

dropdl=[]
for dp in dpl:
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


#pylab.show()
