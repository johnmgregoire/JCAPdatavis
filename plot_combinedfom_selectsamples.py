import numpy, pylab, os, sys, csv
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

dp='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/combinedfom.txt'
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/parsedresults/allfom'



elkeys=['Ni', 'Fe', 'Co', 'Ce']
ellabels=elkeys
compverts=numpy.array([[.5, .37, .13, 0], [.25, 0, .25, .5]])
critdist=.05
betweenbool=True
invertbool=False


pointsize=20
opacity=.6
view_azim=-159
view_elev=18





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

dropd['compositions']=numpy.array([dropd[elkey] for elkey in elkeys]).T

pylab.figure()
#axq=pylab.subplot(111)
stpq=QuaternaryPlot(111, ellabels=ellabels)

comps=numpy.array([dropd[elkey] for elkey in elkeys]).T

selectinds, distfromlin, lineparameter=stpq.filterbydistancefromline(comps, compverts[0], compverts[1], critdist, betweenpoints=betweenbool, invlogic=invertbool, returnall=True)
dropd['lineparameter']=lineparameter
dropd['distfromlin']=distfromlin
lineparameter=lineparameter[selectinds]

cols=stpq.rgb_comp(comps[selectinds])
stpq.plotbycolor(comps[selectinds], cols, marker='o', markersize=5, alpha=.6)

stpq.line(compverts[0], compverts[1], lw=2)
#stpq.scatter(comps[selectinds], pointsize
stpq.set_projection(azim=view_azim, elev=view_elev)
stpq.label(fontsize=20)

pylab.savefig(os.path.join(savefolder, 'QuatPoints.png'))

pylab.figure()

for k, v in dropd.iteritems():
#    if k in elkeys or k in ellabels or k in ['Sample', 'x(mm)', 'y(mm)', 'compositions']:
#        continue
    pylab.clf()
    ax=pylab.subplot(111)
    fomselect=v[selectinds]
    stpq.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
    pylab.ylabel(k)
    pylab.subplots_adjust(bottom=.15, left=.15, right=.8)
    pylab.savefig(os.path.join(savefolder, k+'.png'))

pylab.clf()
ax=pylab.subplot(111)
for k, c, l, vsh in [('CP5Eave', 'b', '1 mA/cm$^2$', -(.187-.044)), ('CP4Eave', 'g', '10 mA/cm$^2$', -(.187-.044)), ('CP6Eave', 'r', '19 mA/cm$^2$', -(.187-.048))]:
    fomselect=(vsh+dropd[k][selectinds])*1000.
    stpq.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color=c, label=l, ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.legend(loc=3)
pylab.ylabel('OER overpotential (mV)')
pylab.subplots_adjust(bottom=.15, left=.15, right=.8)
pylab.savefig(os.path.join(savefolder, 'AllCP.png'))


pylab.clf()
ax=pylab.subplot(111)
for k, c, l, vsh in [ ('I300mVLinSub', 'r', '300 mV', 0.), ('I350mVLinSub', 'b', '350 mV', 0.), ('I400mVLinSub', 'g', '400 mV', 0.)]:
    fomselect=(vsh+dropd[k][selectinds])*100000.
    stpq.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color=c, label=l, ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.legend(loc=2)
pylab.ylabel('J$_{OER}$ from CV (mA/cm$^2$)')
pylab.subplots_adjust(bottom=.15, left=.15, right=.8)
pylab.savefig(os.path.join(savefolder, 'CVcurrents.png'))


pylab.clf()
ax=pylab.subplot(111)
for k, c, l, vsh in [ ('TafelCPLogExCurrent', 'b', '', 5.)]:
    fomselect=(vsh+dropd[k][selectinds])*1.
    stpq.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color=c, label=l, ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.legend(loc=2)
pylab.ylabel('Log(J$_{ex}$ / mA cm$-2$)')
pylab.subplots_adjust(bottom=.15, left=.15, right=.8)
pylab.savefig(os.path.join(savefolder, 'TafelCPexchange.png'))


pylab.clf()
ax=pylab.subplot(111)
for k, c, l, vsh in [ ('TafelCPSlopeVperdec', 'b', '', 0.)]:
    fomselect=(vsh+dropd[k][selectinds])*1000.
    stpq.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color=c, label=l, ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.legend(loc=2)
pylab.ylabel('dV/dLog(J$_{OER}$) (mV/decade)')
pylab.subplots_adjust(bottom=.15, left=.15, right=.8)
pylab.savefig(os.path.join(savefolder, 'TafelCPmVdecade.png'))


inds=[numpy.where(dropd['Sample']==smp)[0][0] for smp in [169, 170, 825, 1326, 1329]]

for k, v in dropd.iteritems():
    print k, v[inds]
