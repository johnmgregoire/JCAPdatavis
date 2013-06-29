import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

#from matplotlib import rcParams
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Helvetica']

#pylab.rc('font',**{'family':'sans','sans':['Helvetica']})
#dp='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/combinedfom.txt'
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/parsedresults/allfom'

savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summarypaper1figs'
xlims=(225, 450)
ylims=(-1.05, 2.25)

p1='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/selectsamplesnesteddlist.pck'
p2='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/selectsamplesnesteddlist.pck'
p3='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/selectsamplesnesteddlist.pck'
p4='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results/selectsamplesnesteddlist.pck'
p5='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/selectsamplesnesteddlist.pck'
p6='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/yunsamples/selectsamplesnesteddlist.pck'
dallsamples=[[693, 693, 170, 170, 170, 170], [3022, 3022, 725, 725, 725, 725], [5047, 5047, 1326, 1326, 1326, 1326], [5050, 5050, 1329, 1329, 1329, 1329], [692, 692, 169, 169, 169, 169]]# list of "compositions" in in terms of sample number. for each composition there should be a corresponding sample number for each of the dall

if not os.path.exists(savefolder):
    os.mkdir(savefolder)
os.chdir(savefolder)


f=open(p1, mode='r')
dall1=pickle.load(f)
f.close()
f=open(p2, mode='r')
dall2=pickle.load(f)
f.close()
f=open(p3, mode='r')
dall3=pickle.load(f)
f.close()
f=open(p4, mode='r')
dall4=pickle.load(f)
f.close()
f=open(p5, mode='r')
dall5=pickle.load(f)
f.close()
f=open(p6, mode='r')
dall6=pickle.load(f)
f.close()

dallinds1={}
dallinds2={}
dallinds3={}
dallinds4={}
dallinds5={}
dallinds6={}

for sl in dallsamples:
    il=[]
    for s, da, di in zip(sl, [dall1, dall2, dall3, dall4, dall5, dall6], [dallinds1, dallinds2, dallinds3, dallinds4, dallinds5, dallinds6]):
        for k, dl in da.iteritems():
            stemp=[d['Sample'] for d in dl]
            if not k in di.keys():
                di[k]=[]
            if s in stemp:
                di[k]+=[stemp.index(s)]
            else:
                di[k]+=[numpy.nan]
                print 'no data found for sample ', s, k

#-------------------------------------------------
pylab.figure(figsize=(6, 4))

dallsamplei=0
k='complete03'
cvsmoothpts=8
    
d=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
vsh=-(.187-0.045)

segd=d['segprops_dlist'][0]
x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
y=d['I(A)_LinSub'][segd['inds']]
y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
posinds=numpy.where(y>1e-6)[0][5:]
x=x[posinds]
y=numpy.log10(y[posinds])+5.
pylab.plot(x, y, '-', color='k', label='SDC CV')

d=dall1['CP1'][dallinds1['CP1'][dallsamplei]]
vsh=-(.187-0.045)
x=(d['FOM']+vsh)*1000.
y=d['I(A)'].mean()
y=numpy.log10(y)+5.
pylab.plot(x, y, 'o', color='g', label='SDC CP')



d1=dall5['bmcv'][dallinds5['bmcv'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)_LinSub']*1000.
y=d['I(mAcm2)_LinSub']
posinds=numpy.where(y>1e-1)[0][1:]
x=x[posinds]
y=numpy.log10(y[posinds])
pylab.plot(x, y, '-', color='c', label='RDE CV')


d1=dall5['bmstepcp'][dallinds5['bmstepcp'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)']*1000.
y=d['I(mAcm2)']
y=numpy.log10(y)
pylab.plot(x, y, ls='None', mec='purple', mfc='purple', marker='s', label='RDE CP')


d1=dall5['bmstepca'][dallinds5['bmstepca'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)']*1000.
y=d['I(mAcm2)']
y=numpy.log10(y)
pylab.plot(x, y, ls='None', mec='b', mfc='b', marker='d', label='RDE CA')



pylab.legend(loc = 'lower right', bbox_to_anchor = (1.12, 0.))
#$pylab.ylabel('Log(J / mA cm$^{-2}$)')
pylab.yticks([-1, 0, 1, 2], ['0.1', '1', '10', '100'])
pylab.ylabel('Current Density (mA cm$^{-2}$)')
pylab.xlabel('Potential (mV vs OER)')

d1=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
t='Sample%d-%d_' %(d1['Sample'], d['Sample'])
t+=''.join([el+'%d' %(int(round(100*v))) for el, v in zip(d['elements'], d['compositions'])])
pylab.title(t)
pylab.xlim(xlims)
pylab.ylim(ylims)
pylab.subplots_adjust(bottom=.12, left=.15)
pylab.savefig(t+'.png')
pylab.savefig(t+'.eps')
pylab.savefig(t+'.svg')

#-------------------------------------------------
pylab.figure(figsize=(6, 4))

dallsamplei=2
k='complete04'
cvsmoothpts=8
    
d=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
vsh=-(.187-0.045)

segd=d['segprops_dlist'][0]
x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
y=d['I(A)_LinSub'][segd['inds']]
y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
posinds=numpy.where(y>1e-6)[0][5:]
x=x[posinds]
y=numpy.log10(y[posinds])+5.
pylab.plot(x, y, '-', color='k', label='SDC CV')

d=dall1['CP1'][dallinds1['CP1'][dallsamplei]]
vsh=-(.187-0.045)
x=(d['FOM']+vsh)*1000.
y=d['I(A)'].mean()
y=numpy.log10(y)+5.
pylab.plot(x, y, 'o', color='g', label='SDC CP')



d1=dall5['bmcv'][dallinds5['bmcv'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)_LinSub']*1000.
y=d['I(mAcm2)_LinSub']
posinds=numpy.where(y>1e-1)[0][1:]
x=x[posinds]
y=numpy.log10(y[posinds])
pylab.plot(x, y, '-', color='c', label='RDE CV')


d1=dall5['bmstepcp'][dallinds5['bmstepcp'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)']*1000.
y=d['I(mAcm2)']
y=numpy.log10(y)
pylab.plot(x, y, ls='None', mec='purple', mfc='purple', marker='s', label='RDE CP')


d1=dall5['bmstepca'][dallinds5['bmstepca'][dallsamplei]]
d=d1[k]
x=d['Ewe(VOER)']*1000.
y=d['I(mAcm2)']
y=numpy.log10(y)
pylab.plot(x, y, ls='None', mec='b', mfc='b', marker='d', label='RDE CA')

d=dall6['CV'][dallinds6['CV'][dallsamplei]]['sample1cv']

x=d['Ewe(VOER)_LinSub']*1000.
#x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
y=d['I(mAcm2)_LinSub']
#y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
posinds=numpy.where(y>1e-1)[0]
x=x[posinds]
y=numpy.log10(y[posinds])
pylab.plot(x, y, '-', color='r', label='edep CV')



pylab.legend(loc = 'lower right', bbox_to_anchor = (1.12, -.02))
#pylab.ylabel('Log(J / mA cm$^{-2}$)')
pylab.yticks([-1, 0, 1, 2], ['0.1', '1', '10', '100'])
pylab.ylabel('Current Density (mA cm$^{-2}$)')
pylab.xlabel('Potential (mV vs OER)')

d1=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
t='Sample%d-%d_' %(d1['Sample'], d['Sample'])
t+=''.join([el+'%d' %(int(round(100*v))) for el, v in zip(d['elements'], d['compositions'])])
pylab.title(t)
pylab.xlim(xlims)
pylab.ylim(ylims)
pylab.subplots_adjust(bottom=.12, left=.15)
pylab.savefig(t+'.png')
pylab.savefig(t+'.eps')
pylab.savefig(t+'.svg')

#def LinIvsVfig_sampleind(dallsamplei, cvsmoothpts=8, cvbools=[1, 1, 1, 1, 1, 1], cpbools=[1, 1, 1, 1, 1, 1]):
#    if cvbools[0]:
#        d=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
#        vsh=-(.187-0.045)
#        d1=d
#        if cvbools[0]:
#            segd=d['segprops_dlist'][0]
#            x=(d['Ewe(V)']+vsh)*1000.
#            x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
#            y=d['I(A)']*1.e5
#            y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
#            x=x[15:-15]
#            y=y[15:-15]
#            pylab.plot(x, y, '-', color='k', label='CVv1')
#    if cvbools[4]:
#        d1=dall5['bmcv'][dallinds5['bmcv'][dallsamplei]]
#        for count, k in enumerate(['complete02', 'complete03', 'complete04']):
#            d=d1[k]
#            x=d['Ewe(VOER)']*1000.
#            y=d['I(mAcm2)']
#
#            if count==0:
#                pylab.plot(x, y, '-', color='c', label='bmCVs')
#            else:
#                pylab.plot(x, y, '-', color='c')
#            
#    if cvbools[5]:
#        d=dall6['CV'][dallinds6['CV'][dallsamplei]]['sample1cv']
#
#        x=d['Ewe(VOER)']*1000.
#        #x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
#        y=d['I(mAcm2)']
#        #y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
#        posinds=numpy.where(y>1e-1)[0]
#        pylab.plot(x, y, '-', color='brown', label='CVv6')
#        
#for dallsamplei in [2]:
#    pylab.figure()
#    LinIvsVfig_sampleind(dallsamplei)
#    pylab.legend(loc = 'upper left')
#    pylab.ylabel('J / mA cm$^{-2}$')
#    pylab.xlabel('Potential (mV vs OER)')
#    
#    d1=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
#    d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
#    t='Sample%d-%d_' %(d1['Sample'], d['Sample'])
#    t+=''.join([el+'%d' %(int(round(100*v))) for el, v in zip(d['elements'], d['compositions'])])
#    pylab.title(t)
#    pylab.xlim(-100, 460)
#    pylab.ylim(-8, 180)
#    t+='LinCV'
#    pylab.savefig(t+'.png')
#    pylab.savefig(t+'.eps')
pylab.show()





