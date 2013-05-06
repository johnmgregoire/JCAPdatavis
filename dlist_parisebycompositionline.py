import pylab, numpy, sys, pickle
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myquaternaryutility import QuaternaryPlot


SYSTEM=0

if SYSTEM==0:
    elkeys=['Ni', 'Fe', 'Co', 'Ce']
    
    pl=[]
    pl+=['C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results/20130402NiFeCoCe_Plate1_5500_dlist.dat']
    pl+=['C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate2_5498_dlist.dat']
    pl+=['C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate3_4835_dlist.dat']
    compend1=numpy.array([.5, .5, .0, .0])
    compend2=numpy.array([.27, 0, .27, .46])
    critdist=.06
    savep='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline%.2f_plate123_dlist.dat' %critdist
    savep2='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline%.2f_linedetails.dat' %critdist
    savep3='C:/Users/gregoire/Documents/EchemDropRawData/NiFeCoCe/parsedresults/201304NiFeCoCe_compline%.2f_samples.txt' %critdist
    betweenpoints=False
    stpq=QuaternaryPlot(111)

platesdlist=[]
plotcomps=[]
lined={}
lined['distfromlin']=[]
lined['lineparameter']=[]
lined['compend1']=compend1
lined['compend2']=compend2
lined['critdist']=critdist
lined['betweenpoints']=betweenpoints
for p in pl:
    f=open(p, mode='r')
    dlist=pickle.load(f)
    f.close()
    comps=numpy.array([d['compositions'] for d in dlist])
    inds, distfromlin, lineparameter=stpq.filterbydistancefromline(comps, compend1, compend2, critdist, betweenpoints=betweenpoints, invlogic=False, returnall=True)
    platesdlist+=[dlist[i] for i in inds]
    plotcomps+=list(comps[inds])
    lined['distfromlin']+=list(distfromlin[inds])
    lined['lineparameter']+=list(lineparameter[inds])
    print len(inds),  ' points'

smpls=[d['Sample'] for d in platesdlist]
s='\n'.join(['%d' %x for x in smpls])

lined['distfromlin']=numpy.array(lined['distfromlin'])
lined['lineparameter']=numpy.array(lined['lineparameter'])

if 1:
    f=open(savep, mode='w')
    pickle.dump(platesdlist, f)
    f.close()
    f=open(savep2, mode='w')
    pickle.dump(lined, f)
    f.close()

if 1:
    f=open(savep3, mode='w')
    f.write(s)
    f.close()
    
if 1:
    plotcomps=numpy.array(plotcomps)
    stpq.scatter(plotcomps)
    pylab.show()


