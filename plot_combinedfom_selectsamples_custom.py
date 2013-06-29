import numpy, pylab, os, sys, csv
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
pylab.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

dp='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/combinedfom.txt'
savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/parsedresults/paperfom'



elkeys=['Ni', 'Fe', 'Co', 'Ce']
ellabels=elkeys
compvertsp=numpy.array([[.5, .5, 0, 0], [.5, 0, .5, 0], [0, 0, .1, .9]])
critdistp=.05
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
comps=numpy.array([dropd[elkey] for elkey in elkeys]).T


gridi=30
comps30=[(a*1./gridi, b*1./gridi, c*1./gridi, (gridi-a-b-c)*1./gridi) for a in numpy.arange(0,1+gridi) for b in numpy.arange(0,1+gridi-a) for c in numpy.arange(0,1+gridi-a-b)]


pylab.figure()
#axq=pylab.subplot(111)
stpq=QuaternaryPlot(111, ellabels=ellabels)


cols=stpq.rgb_comp(comps30)
stpq.plotbycolor(comps30, cols, marker='o', markersize=3, alpha=1)

stpq.set_projection(azim=view_azim, elev=view_elev)

pylab.savefig(os.path.join(savefolder, 'QuatPointsAll.png'))
pylab.savefig(os.path.join(savefolder, 'QuatPointsAll.eps'))


pylab.figure()
#axq=pylab.subplot(111)
stpqp=QuaternaryPlot(111, ellabels=ellabels)



selectinds, distfromplane, xyparr, xyp_verts,intriangle=stpqp.filterbydistancefromplane(comps, compvertsp[0], compvertsp[1], compvertsp[2], critdistp, withintriangle=betweenbool, invlogic=invertbool, returnall=True)
xyparr=xyparr[selectinds]



cols=stpqp.rgb_comp(comps[selectinds])
stpqp.plotbycolor(comps[selectinds], cols, marker='o', markersize=3, alpha=1)

stpqp.line(compvertsp[0], compvertsp[1], lw=2)
stpqp.line(compvertsp[2], compvertsp[1], lw=2)
stpqp.line(compvertsp[0], compvertsp[2], lw=2)

#stpqp.scatter(comps[selectinds], pointsize
stpqp.set_projection(azim=view_azim, elev=view_elev)
stpqp.label(fontsize=20)

pylab.savefig(os.path.join(savefolder, 'QuatPointsPlane.png'))
pylab.savefig(os.path.join(savefolder, 'QuatPointsPlane.eps'))


pylab.figure()
#axq=pylab.subplot(111)
stpql=QuaternaryPlot(111, ellabels=ellabels)



selectinds, distfromlin, lineparameter=stpql.filterbydistancefromline(comps, compverts[0], compverts[1], critdist, betweenpoints=betweenbool, invlogic=invertbool, returnall=True)
dropd['lineparameter']=lineparameter
dropd['distfromlin']=distfromlin
lineparameter=lineparameter[selectinds]

cols=stpql.rgb_comp(comps[selectinds])
stpql.plotbycolor(comps[selectinds], cols, marker='o', markersize=3, alpha=1)

stpql.line(compverts[0], compverts[1], lw=2)
stpql.line(compvertsp[0], compvertsp[1], lw=1.2)
stpql.line(compvertsp[2], compvertsp[1], lw=1.2)
stpql.line(compvertsp[0], compvertsp[2], lw=1.2)

#stpql.scatter(comps[selectinds], pointsize
stpql.set_projection(azim=view_azim, elev=view_elev)
stpql.label(fontsize=20)

pylab.savefig(os.path.join(savefolder, 'QuatPointsLin.png'))
pylab.savefig(os.path.join(savefolder, 'QuatPointsLin.eps'))



pylab.figure(figsize=(6, 4))
ax=pylab.subplot(111)
for k, c, l, vsh in [('CP5Eave', 'b', '1 mA/cm$^2$', -(.187-.044)), ('CP4Eave', 'g', '10 mA/cm$^2$', -(.187-.044)), ('CP6Eave', 'r', '19 mA/cm$^2$', -(.187-.048))]:
    fomselect=(vsh+dropd[k][selectinds])*1000.
    stpql.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color=c, label=l, labelfmtstr='%.2f', ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
#pylab.legend(loc=3)
pylab.ylim(290, 430)
pylab.text(.4,300,'$J$=1 mA cm$^{-2}$', color='b')
pylab.text(.3,358,'$J$=10 mA cm$^{-2}$', color='g')
pylab.text(.2,416,'$J$=19 mA cm$^{-2}$', color='r')
pylab.ylabel('$\eta$, OER overpotential (mV)')
pylab.subplots_adjust(bottom=.25, left=.15, right=.72)
pylab.savefig(os.path.join(savefolder, 'AllCP.png'))
pylab.savefig(os.path.join(savefolder, 'AllCP.eps'))




pylab.figure(figsize=(6, 4))
ax=pylab.subplot(111)
for k, c, l, vsh in [ ('TafelCPLogExCurrent', 'b', '', 5.)]:
    fomselect=(vsh+dropd[k][selectinds])*1.
    stpql.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color='k', label=l, labelfmtstr='%.2f', ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.ylabel('Log($J_{\eta=0}$ / mA cm$^{-2}$)')
pylab.subplots_adjust(bottom=.25, left=.15, right=.72)
pylab.savefig(os.path.join(savefolder, 'TafelCPexchange.png'))
pylab.savefig(os.path.join(savefolder, 'TafelCPexchange.eps'))


pylab.figure(figsize=(6, 4))
ax=pylab.subplot(111)
for k, c, l, vsh in [ ('TafelCPSlopeVperdec', 'b', '', 0.)]:
    fomselect=(vsh+dropd[k][selectinds])*1000.
    stpql.plotfomalonglineparameter(ax, lineparameter, fomselect, compend1=compverts[0], compend2=compverts[1], lineparticks=numpy.linspace(0, 1, 5), ls='none', marker='.', color='k', label=l, labelfmtstr='%.2f', ticklabelkwargdict=dict([('rotation', -20), ('horizontalalignment', 'left')]))
pylab.ylim(40, 95)
pylab.ylabel(r'$\alpha$'+'=d$\eta$/d$Log(J)$ (mV/decade)')
pylab.text(.16,60,'Fig.2a', color='k', ha='center')
pylab.text(.46,44,'Fig.2b', color='k', ha='center')
pylab.text(.91,64,'Fig.2c', color='k', ha='center')

pylab.subplots_adjust(bottom=.33, left=.15, right=.72)
pylab.savefig(os.path.join(savefolder, 'TafelCPmVdecade.png'))
pylab.savefig(os.path.join(savefolder, 'TafelCPmVdecade.eps'))


pylab.show()

