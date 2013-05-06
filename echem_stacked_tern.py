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
    
if 0:
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
elif 0:
    ellabels=['Fe', 'Co', 'Ni', 'Ti']
    os.chdir('C:/Users/Gregoire/Documents/CaltechWork/echemdrop')
    rootstr='20120728NiFeCoTiplate'
    expstr='CP1Ess'
    fomlabel='Potential for 0.02mA (V vs H$_2$0/O$_2$)'
    fomshift=-.2
    fommult=1.
    vmin=.21
    vmax=.45
    cmap=cm.jet_r
    aboverangecolstr='k'
    belowrangecolstr=''
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTi_allplateresults'
elif 1:
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
    savefolder='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/'+rootstr.partition('late')[0][:-1]



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


pointsize=20
opacity=.6
view_azim=-159
view_elev=30

fig=pylab.figure(figsize=(9, 4.*len(dropdl)))
figquatall=[]
compsall=[]
fomall=[]
plateindall=[]
for count, dropd in enumerate(dropdl):
    #dropinds=numpy.arange(len(dropd['Sample']))
    dropinds=numpy.argsort(dropd['Sample'])
    x=dropd['x(mm)'][dropinds]
    y=dropd['y(mm)'][dropinds]

    fom=(dropd[expstr][dropinds]+fomshift)*fommult


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
    
    comp=numpy.array([[dropd['A'][i], dropd['B'][i], dropd['C'][i], dropd['D'][i]] for i in dropinds])
    
    comp=numpy.array([a/a.sum() for a in comp])
    figquat=pylab.figure(figsize=(8, 8))
    stp = QuaternaryPlot(111, minlist=[0., 0., 0., 0.], ellabels=ellabels)

    stp.scatter(comp, c=fom, s=pointsize, edgecolors='none', cmap=cmap, norm=norm)

    stp.label(ha='center', va='center', fontsize=16)

    stp.set_projection(azim=view_azim, elev=view_elev)
    caxquat=figquat.add_axes((.83, .3, .04, .4))
    cb=pylab.colorbar(stp.mappable, cax=caxquat, extend=extend)
    cb.set_label(fomlabel, fontsize=16)
    stp.ax.set_title('plate %d' %(count+1))
    compsall+=list(comp)
    fomall+=list(fom)
    figquatall+=[figquat]
    plateindall+=[count]*len(fom)
    
fig.subplots_adjust(left=.05, bottom=.03, top=.96, right=.83, hspace=.14)
cax=fig.add_axes((.85, .3, .04, .4))
cb=pylab.colorbar(mapbl, cax=cax, extend=extend)
cb.set_label(fomlabel, fontsize=20)

compsall=numpy.array(compsall)
fomall=numpy.array(fomall)
plateindall=numpy.array(plateindall)


axl, stpl=make10ternaxes(ellabels=ellabels)
pylab.figure(figsize=(8, 8))
stpquat=QuaternaryPlot(111, ellabels=ellabels)

stpquat.scatter(compsall, c=fomall, s=20, edgecolors='none', cmap=cmap, norm=norm)
scatter_10axes(compsall, fomall, stpl, s=20, edgecolors='none', cmap=cmap, norm=norm)
stpquat.label()

stpquat.set_projection(azim=view_azim, elev=view_elev)

figtemp=pylab.figure(stpquat.ax.figure.number)
cax10=figtemp.add_axes((.83, .3, .04, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cax10, extend=extend)
cb.set_label(fomlabel, fontsize=16)

figtemp=pylab.figure(axl[0].figure.number)
cax10=figtemp.add_axes((.85, .3, .04, .4))
cb=pylab.colorbar(stpquat.mappable, cax=cax10, extend=extend)
cb.set_label(fomlabel, fontsize=16)

purelfig=pylab.figure()
linestyle=['-', '--', '-.', ':']
for count, col in enumerate(['c', 'm', 'y', 'k']):
    c_el=compsall[:, count]
    inds=numpy.where(c_el>.99)
    fom_el=fomall[inds]
    plate_inds=plateindall[inds]
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

if 0:
    os.chdir(savefolder)
    pylab.figure(fig.number)
    pylab.savefig('%s_PlatesAll_Posn.png' %expstr)
    for count, fg in enumerate(figquatall):
        pylab.figure(fg.number)
        pylab.savefig('%s_Plate%d_Quat.png' %(expstr, count+1))
    pylab.figure(stpquat.ax.figure.number)
    pylab.savefig('%s_PlatesAll_Quat.png' %expstr)
    
    pylab.figure(axl[0].figure.number)
    pylab.savefig('%s_stackedtern.png' %expstr)
    
    pylab.figure(purelfig.number)
    pylab.savefig('%s_pureelements.png' %expstr)
    
pylab.show()
