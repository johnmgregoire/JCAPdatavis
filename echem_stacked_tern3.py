import matplotlib.cm as cm
import numpy
import pylab
import h5py, operator, copy, os, csv
from echem_plate_fcns import *
from echem_plate_math import *

os.chdir('C:/Users/gregoire/Documents/PythonCode/ternaryplot')

from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_bintern import *
#os.chdir(cwd)

pylab.rc('font', family='serif', serif='Times New Roman')

elkeys=['A', 'B', 'C', 'D']
SYSTEM=11

pointsize=20
opacity=.6
view_azim=-159
view_elev=30

allposn=True

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
    fommult=1000.
    vmin=.03
    vmax=.3
    cmap=cm.jet
    aboverangecolstr='k'
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
    fommult=1000.
    vmin=.03
    vmax=.3
    cmap=cm.jet
    aboverangecolstr='k'
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
#stpquat.label(fontsize=20)

stpquat.set_projection(azim=view_azim, elev=view_elev)

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
    sortinds=numpy.argsort(c_el[inds])
    fom_el=fomel[inds][sortinds]
    plate_inds=plateindel[inds][sortinds]
    try:
        fom_plate_thick=numpy.array([fom_el[plate_inds==i][-4:] for i in range(3)])#everything was rodered by Sample so now it will be ordered by thickness
    except:
        continue
    if fom_plate_thick.shape!=(3, 4):
        continue
    for thickcount, (fom_plate, ls) in enumerate(zip(fom_plate_thick.T, linestyle)):
        if count==3 or thickcount==0:
            pylab.plot([1, 2, 3], fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13, label='%s,thick. %d' %(ellabels[count], thickcount+1))
#        elif thickcount==0:
#            pylab.plot([1, 2, 3], fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13, label='%s' %(ellabels[count],) )
        else:
            pylab.plot([1, 2, 3], fom_plate, col+ls, marker=r'$%d$' %(thickcount+1),markersize=13)
pylab.xlim(.7, 4.3)
pylab.xlabel('plate number')
pylab.ylabel('fom')
pylab.title('PURE ELEMENTS. color=element(CMYK). #=thickness')
pylab.legend(loc=1)

if SYSTEM==1:
    axbin.set_ylim(.23, .7)
if SYSTEM==6:
    axbin.set_ylim(.38, .5)

os.chdir(savefolder)
if 0:
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
    
    pylab.figure(axl_tern[0].figure.number)
    pylab.savefig('%s_ternfaces.png' %expstr)
    
    pylab.figure(axbin.figure.number)
    pylab.savefig('%s_binaries.png' %expstr)
    
    pylab.figure(purelfig.number)
    pylab.savefig('%s_pureelements.png' %expstr)

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
if 1:
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat_hires.png' %expstr, dpi=600)
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern_hires.png' %expstr, dpi=600)
#pylab.show()
