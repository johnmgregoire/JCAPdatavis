import numpy, pylab, os, sys, csv, pickle
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot

#dp='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/combinedfom.txt'
#savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/parsedresults/allfom'

SYSTEM=21

bmcpavebool=True
if SYSTEM==-1:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summarytemp'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 0, 0, 1, 1]
    cpbools=[1, 0, 0, 0, 1, 1]
    bmcpavebool=False
elif SYSTEM==0:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 1, 1, 1, 1, 0]
    cpbools=[1, 1, 1, 1, 1, 0]
elif SYSTEM==1:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys1345'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 1, 1, 1, 0]
    cpbools=[1, 0, 1, 1, 1, 0]
elif SYSTEM==2:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys15'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 0, 0, 1, 0]
    cpbools=[1, 0, 0, 0, 1, 0]
elif SYSTEM==21:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys15indiv6'
    xlims=(250, 460)
    ylims=(-.8, 2.3)
    cvbools=[1, 0, 0, 0, 1, 1]
    cpbools=[1, 0, 0, 0, 1, 1]
    bmcpavebool=False
elif SYSTEM==3:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys3CP5'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[0, 0, 0, 0, 1, 0]
    cpbools=[0, 0, 1, 0, 1, 0]
elif SYSTEM==4:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys1CV3CP5'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 0, 0, 1, 0]
    cpbools=[0, 0, 1, 0, 1, 0]
elif SYSTEM==41:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys1CV3CP5indiv'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 0, 0, 1, 0]
    cpbools=[0, 0, 1, 0, 1, 0]
    bmcpavebool=False
elif SYSTEM==5:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys1345indiv'
    xlims=(250, 460)
    ylims=(-.8, 1.8)
    cvbools=[1, 0, 1, 1, 1, 0]
    cpbools=[1, 0, 1, 1, 1, 0]
    bmcpavebool=False
elif SYSTEM==6:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys1345indiv6'
    xlims=(220, 460)
    ylims=(-.8, 2.3)
    cvbools=[1, 0, 1, 1, 1, 1]
    cpbools=[1, 0, 1, 1, 1, 1]
    bmcpavebool=False
elif SYSTEM==7:
    savefolder='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/summary_sys15indiv6'
    xlims=(220, 460)
    ylims=(-.8, 2.3)
    cvbools=[1, 0, 0, 0, 1, 1]
    cpbools=[1, 0, 0, 0, 1, 1]
    bmcpavebool=False
    
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

#BMCP102010_dallindex=[\
#[numpy.array([0.355, 0.389, 0.374]), numpy.array([0.007, 0.014, 0.011])], \
#[numpy.array([0.376, 0.425, 0.380]), numpy.array([0.017, 0.033, 0.017])], \
#[numpy.array([0.377, 0.419, 0.379]), numpy.array([0.017, 0.034, 0.021])], \
#numpy.nan, numpy.nan]#indexed same as dall and then within is a list of 2 arrays, 0th is vs OER and 1st is STD from 3 repeat measurements





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

def CPTafel_sampleind(dallsamplei, cvbools=[1, 1, 1, 1, 1, 1], cpbools=[1, 1, 1, 1, 1, 1]):
    if cpbools[2]:
        d=dall3['Tafel'][dallinds3['Tafel'][dallsamplei]]
        dydx=1./(d['TafelCPSlopeVperdec']*1000.)
        y0=d['TafelCPLogExCurrent']+5.
        x=numpy.array(xlims)
        y=x*dydx+y0
        pylab.plot(x, y, 'r--', label='CP3fit')

def allbmcvfig_sampleind(dallsamplei):
    d1=dall5['bmcv'][dallinds5['bmcv'][dallsamplei]]
    for count, k in enumerate(['complete02', 'complete03', 'complete04']):
        d=d1[k]
#        x=d['Ewe(VOER)']*1000.
#        i=numpy.argmax(x)
#        x=x[:i]
#        y=d['I(mAcm2)'][:i]
        x=d['Ewe(VOER)_LinSub']*1000.
        y=d['I(mAcm2)_LinSub']
        posinds=numpy.where(y>1e-1)[0][1:]
        x=x[posinds]
        y=numpy.log10(y[posinds])
        if count==0:
            pylab.plot(x, y, '-', color='c', label='bmCVs')
        else:
            pylab.plot(x, y, '-', color='c')

def allbmcpfig_sampleind(dallsamplei, avebool=True, plot2hr=True):#booleans not implemented yet
    d1=dall5['bmstepcp'][dallinds5['bmstepcp'][dallsamplei]]
    xarr=[]
    yarr=[]
    for k in ['complete02', 'complete03', 'complete04']:
        d=d1[k]
        xarr+=[d['Ewe(VOER)']*1000.]
        yarr+=[d['I(mAcm2)']]
    xarr=numpy.array(xarr)
    yarr=numpy.array(yarr)
    if avebool:
        x=xarr.mean(axis=0)
        xe=xarr.std(axis=0)
        y=numpy.log10(yarr.mean(axis=0))
        
        pylab.errorbar(x, y, xerr=xe, ls='None', color='m', marker='s', mec='m', mfc='none', mew=.9, label='bmCP')
    else:
        for count, (x, y) in enumerate(zip(xarr, yarr)):
            y=numpy.log10(y)
            if count==0:
                pylab.plot(x, y, ls='None', color='m', marker=r'$'+`count+2`+'$', mfc='none', label='bmCP')
            else:
                pylab.plot(x, y, ls='None', color='m', marker=r'$'+`count+2`+'$', mfc='none')

    if plot2hr:
        d1=dall5['bm2hrcp'][dallinds5['bm2hrcp'][dallsamplei]]
        xarr=[]
        yarr=[]
        for k in ['complete02', 'complete03', 'complete04']:
            d=d1[k]
            xarr+=[d['Ewe(VOER)']*1000.]
            yarr+=[d['I(mAcm2)']]
        xarr=numpy.array(xarr)
        yarr=numpy.array(yarr)
        x2=xarr.mean()
        xe2=xarr.std()
        y2=numpy.log10(yarr.mean())
        if avebool:
            pylab.errorbar(x2, y2, xerr=xe2, ls='None', color='m', marker='s', mec='m', mfc='m', mew=.9, label='bmCP 2hr')
        else:
            for count, (x, y) in enumerate(zip(xarr, yarr)):
                y=numpy.log10(y)
                if count==0:
                    pylab.plot(x, y, ls='None', color='m', marker=r'$'+`count+2`+"'$", mfc='none', label='bmCP 2hr')
                else:
                    pylab.plot(x, y, ls='None', color='m', marker=r'$'+`count+2`+"'$", mfc='none')

    
def allLogIvsVfig_sampleind(dallsamplei, cvsmoothpts=8, cvbools=[1, 1, 1, 1, 1, 1], cpbools=[1, 1, 1, 1, 1, 1]):
    
    d=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
    vsh=-(.187-0.045)
    d1=d
    if cvbools[0]:
        segd=d['segprops_dlist'][0]
        x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
        x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(A)_LinSub'][segd['inds']]
        y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-6)[0][5:]
        x=x[posinds]
        y=numpy.log10(y[posinds])+5.
        pylab.plot(x, y, '-', color='k', label='CVv1')
    
    if cvbools[1]:
        d=dall2['CV3'][dallinds2['CV3'][dallsamplei]]
        vsh=-(.187-0.045)
        segd=d['segprops_dlist'][0]
        x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
        x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(A)_LinSub'][segd['inds']]
        y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-6)[0][5:]
        x=x[posinds]
        y=numpy.log10(y[posinds])+5.
        pylab.plot(x, y, '-', color='b', label='CVv2')

    if cvbools[2]:
        d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
        vsh=-(.187-0.045)
        segd=d['segprops_dlist'][0]
        x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
        x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(A)_LinSub'][segd['inds']]
        y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-6)[0][5:]
        x=x[posinds]
        y=numpy.log10(y[posinds])+5.
        pylab.plot(x, y, '-', color='r', label='CVv3')

    if cvbools[3]:
        d=dall4['CV3'][dallinds4['CV3'][dallsamplei]]
        vsh=-(.187-0.045)
        segd=d['segprops_dlist'][0]
        x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
        x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(A)_LinSub'][segd['inds']]
        y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-6)[0][5:]
        x=x[posinds]
        y=numpy.log10(y[posinds])+5.
        pylab.plot(x, y, '-', color='y', label='CVv4')
    
    if cvbools[3]:
        d=dall4['CV3postCP'][dallinds4['CV3postCP'][dallsamplei]]
        vsh=-(.187-0.045)
        segd=d['segprops_dlist'][0]
        x=(d['Ewe(V)'][segd['inds']]+vsh)*1000.
        x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(A)_LinSub'][segd['inds']]
        y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-6)[0][5:]
        x=x[posinds]
        y=numpy.log10(y[posinds])+5.
        pylab.plot(x, y, '-', color='g', label='CVv4postCP')
    

        
    if cpbools[0]:
        d=dall1['CP1'][dallinds1['CP1'][dallsamplei]]
        vsh=-(.187-0.045)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='k', label='CPv1')

    if cpbools[2]:
        d=dall3['CP4'][dallinds3['CP4'][dallsamplei]]
        vsh=-(.187-0.043)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='r', label='CPv3')

        d=dall3['CP5'][dallinds3['CP5'][dallsamplei]]
        vsh=-(.187-0.043)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='r')

        d=dall3['CP6'][dallinds3['CP6'][dallsamplei]]
        vsh=-(.187-0.045)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='r')
    if cpbools[3]:
        d=dall3['CP4'][dallinds3['CP4'][dallsamplei]]
        vsh=-(.187-0.045)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='g', label='CPv4')

        d=dall3['CP5'][dallinds3['CP5'][dallsamplei]]
        vsh=-(.187-0.045)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='g')

        d=dall3['CP6'][dallinds3['CP6'][dallsamplei]]
        vsh=-(.187-0.045)
        x=(d['FOM']+vsh)*1000.
        y=d['I(A)'].mean()
        y=numpy.log10(y)+5.
        pylab.plot(x, y, 'o', color='g')
    #
    #pylab.legend(loc=4)
#    pylab.ylabel('Log(J / mA cm$^{-2}$)')
#    pylab.xlabel('Potential (mV vs OER)')
#
#    t='Sample%d,%d:' %(d1['Sample'], d['Sample'])
#    t+=''.join([el+'%d' %(100*v) for el, v in zip(d['elements'], d['compositions'])])
#    pylab.title(t)



def yuncvplot(dallsamplei):
    if cvbools[5]:
        d=dall6['CV'][dallinds6['CV'][dallsamplei]]['sample1cv']

        x=d['Ewe(VOER)_LinSub']*1000.
        #x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(mAcm2)_LinSub']
        #y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-1)[0]
        x=x[posinds]
        y=numpy.log10(y[posinds])
        pylab.plot(x, y, '-', color='brown', label='CVv6')
        

def LinIvsVfig_sampleind(dallsamplei, cvsmoothpts=8, cvbools=[1, 1, 1, 1, 1, 1], cpbools=[1, 1, 1, 1, 1, 1]):
    if cvbools[0]:
        d=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
        vsh=-(.187-0.045)
        d1=d
        if cvbools[0]:
            segd=d['segprops_dlist'][0]
            x=(d['Ewe(V)']+vsh)*1000.
            x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
            y=d['I(A)']*1.e5
            y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
            x=x[15:-15]
            y=y[15:-15]
            pylab.plot(x, y, '-', color='k', label='CVv1')
    if cvbools[4]:
        d1=dall5['bmcv'][dallinds5['bmcv'][dallsamplei]]
        for count, k in enumerate(['complete02', 'complete03', 'complete04']):
            d=d1[k]
            x=d['Ewe(VOER)']*1000.
            y=d['I(mAcm2)']

            if count==0:
                pylab.plot(x, y, '-', color='c', label='bmCVs')
            else:
                pylab.plot(x, y, '-', color='c')
            
    if cvbools[5]:
        d=dall6['CV'][dallinds6['CV'][dallsamplei]]['sample1cv']

        x=d['Ewe(VOER)']*1000.
        #x=savgolsmooth(x, nptsoneside=cvsmoothpts, order=1)
        y=d['I(mAcm2)']
        #y=savgolsmooth(y, nptsoneside=cvsmoothpts, order=2)
        posinds=numpy.where(y>1e-1)[0]
        pylab.plot(x, y, '-', color='brown', label='CVv6')

for dallsamplei in range(5):
    pylab.figure(num=dallsamplei)
    allLogIvsVfig_sampleind(dallsamplei, cvbools=cvbools, cpbools=cpbools)
    CPTafel_sampleind(dallsamplei, cvbools=cvbools, cpbools=cpbools)
if cpbools[4]:
    for dallsamplei in range(3):
        pylab.figure(num=dallsamplei)
        allbmcpfig_sampleind(dallsamplei, avebool=bmcpavebool, plot2hr=True)

if cvbools[4]:
    for dallsamplei in range(3):
        pylab.figure(num=dallsamplei)
        allbmcvfig_sampleind(dallsamplei)

if cvbools[5]:
    for dallsamplei in [2]:
        pylab.figure(num=dallsamplei)
        yuncvplot(dallsamplei)

for dallsamplei in range(5):
    pylab.figure(num=dallsamplei)  
    pylab.legend(loc = 'lower right', bbox_to_anchor = (1.12, 0.))
    pylab.ylabel('Log(J / mA cm$^{-2}$)')
    pylab.xlabel('Potential (mV vs OER)')
    
    d1=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
    d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
    t='Sample%d-%d_' %(d1['Sample'], d['Sample'])
    t+=''.join([el+'%d' %(int(round(100*v))) for el, v in zip(d['elements'], d['compositions'])])
    pylab.title(t)
    pylab.xlim(xlims)
    pylab.ylim(ylims)
    
    pylab.savefig(t+'.png')
    pylab.savefig(t+'.eps')

for dallsamplei in [2]:
    pylab.figure()
    LinIvsVfig_sampleind(dallsamplei)
    pylab.legend(loc = 'upper left')
    pylab.ylabel('J / mA cm$^{-2}$')
    pylab.xlabel('Potential (mV vs OER)')
    
    d1=dall1['CV3'][dallinds1['CV3'][dallsamplei]]
    d=dall3['CV3'][dallinds3['CV3'][dallsamplei]]
    t='Sample%d-%d_' %(d1['Sample'], d['Sample'])
    t+=''.join([el+'%d' %(int(round(100*v))) for el, v in zip(d['elements'], d['compositions'])])
    pylab.title(t)
    pylab.xlim(-100, 460)
    pylab.ylim(-8, 180)
    t+='LinCV'
    pylab.savefig(t+'.png')
    pylab.savefig(t+'.eps')
pylab.show()





