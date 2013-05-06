import matplotlib.cm as cm
import numpy
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
SYSTEM=0
#29,34,39
pointsize=20
opacity=.6
view_azim=-159
view_elev=30
labelquat=True
#permuteelements=[1, 2, 0, 3]
permuteelements=[0, 1, 2, 3]
allposn=True

if SYSTEM==0:
    ellabels=['Ni', 'Fe', 'Co', 'Ce']
    os.chdir('C:/Users/Public/Documents/EchemDropAnalyzedData')
    rootstr='CV3Imax'
    expstr='CV3Imax'
    fomlabel='test'
    fomshift=0
    vmin=.0005
    vmax=.003
    fommult=1.
    savefolder='C:/Users/Public/Documents/EchemDropAnalyzedData'
    binarylegloc=1
    elkeys=ellabels
    cmap=cm.jet
    aboverangecolstr='.3'
    belowrangecolstr='k'
    savefolder=os.path.join(os.getcwd(), expstr)
    if not os.path.isdir(savefolder):
        os.mkdir(savefolder)

    
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
scatter_10axes(compsall[code0inds], fomall[code0inds], stpl, s=18, edgecolors='none', cmap=cmap, norm=norm, cb=True, cblabel=fomlabel)
if labelquat:
    stpquat.label(fontsize=20)

stpquat.set_projection(azim=view_azim, elev=view_elev)


axl30, stpl30=make30ternaxes(ellabels=ellabels)
scatter_30axes(compsall[code0inds], fomall[code0inds], stpl30, s=18, edgecolors='none', cmap=cmap, norm=norm, cb=True, cblabel=fomlabel)


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

#figtemp=pylab.figure(axl[0].figure.number)
#cbax=figtemp.add_axes((.85, .3, .04, .4))
#cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
#cb.set_label(fomlabel, fontsize=16)

#figtemp=pylab.figure(axl30[0].figure.number)
#cbax=figtemp.add_axes((.91, .3, .03, .4))
#cb=pylab.colorbar(stpquat.mappable, cax=cbax, extend=extend)
#cb.set_label(fomlabel, fontsize=18)

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
    
    pylab.figure(axl30[0].figure.number)
    pylab.savefig('%s_stackedtern30.png' %expstr)
    
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
if 0:
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat_hires.png' %expstr, dpi=600)
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern_hires.png' %expstr, dpi=600)
pylab.show()
