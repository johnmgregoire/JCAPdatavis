import matplotlib.cm as cm
import numpy
import pylab
import h5py, operator, copy, os, csv
from echem_plate_fcns import *
from echem_plate_math import *

os.chdir('C:/Users/gregoire/Documents/PythonCode/ternaryplot')

from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern import *
from quaternary_FOM_bintern import *
#os.chdir(cwd)


elkeys=['A', 'B', 'C', 'D']

ellabels=['Fe', 'Co', 'Ni', 'Ti']
os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop/2012-9_FeCoNiTi/results')
rootstr='2012-9_FeCoNiTi_500C_fastCV_plate1_dlist.dat_'
expstrl=['SegIndStart_LinSub','LinLen_LinSub','Intercept_LinSub','dIdt_LinSub', 'ImaxCVLinSub', 'V_IthreshCVLinSub']
#fomlabel='V to reach 2E-5 A in CV (V vs H$_2$0/O$_2$)'
#fomshift=-.2
#fommult=1.
#vmin=.35
#vmax=.45
cmapl=[cm.jet, cm.jet, cm.jet, cm.jet, cm.jet, cm.jet_r]
aboverangecolstr='k'
belowrangecolstr='.3'
elkeys=ellabels
    

pointsize=20
opacity=.6



for expstr, cmap in zip(expstrl, cmapl):
    for fn in os.listdir(os.getcwd()):
        if rootstr in fn and expstr in fn:
            dp=os.path.join(os.getcwd(), fn)
            break
    print expstr, dp
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
    
    print dropd.keys()


    dropinds=numpy.argsort(dropd['Sample'])
    dropinds=dropinds[numpy.logical_not(numpy.isnan(dropd[expstr][dropinds]))]
    x=dropd['x(mm)'][dropinds]
    y=dropd['y(mm)'][dropinds]

    #fom=(dropd[expstr][dropinds]+fomshift)*fommult
    fom=dropd[expstr][dropinds]
    vmin=fom.min()
    vmax=fom.max()
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


    fig=pylab.figure(figsize=(9, 5.))
    ax2=fig.add_subplot(111)
    ax2.set_aspect(1)
    mapbl=ax2.scatter(x, y, c=fom, s=60, marker='s', edgecolors='none', cmap=cmap, norm=norm)
    ax2.set_xlim(x.min()-2, x.max()+2)
    ax2.set_ylim(y.min()-2, y.max()+2)
    ax2.set_title(expstr)
    fig.subplots_adjust(left=.05, bottom=.05, top=.94, right=.83, hspace=.14)
    cax=fig.add_axes((.85, .2, .04, .6))
    cb=pylab.colorbar(mapbl, cax=cax, extend=extend)
    #cb.set_label(expstr, fontsize=20)

    pylab.savefig(dp[:-4]+'.png')
    
pylab.show()
