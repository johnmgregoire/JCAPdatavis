import numpy, scipy

from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from echem_plate_math import *
import time, pickle
from echem_plate_fcns import *
from echem_FCVSsurfacearea3 import *

#folder='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835'
#savefolder='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe_3V_FCV_4835'

folder='C:/Users/Public/Documents/EchemDropRawData/full plate FCV/20130530 NiFeCoCe_plate1_FCV_5577'
savefolder='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe/20130530 NiFeCoCe_plate1_FCV_5577'

#folder='C:/Users/Public/Documents/EchemDropRawData/full plate FCV/20130602 2nd NiFeCoCe_plate2_FCV_5498'
#savefolder='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe/20130602 2nd NiFeCoCe_plate2_FCV_5498'

#folder='C:/Users/Public/Documents/EchemDropRawData/full plate FCV/20130524 NiFeCoCe_plate3_FCV_4835'
#savefolder='C:/Users/Public/Documents/EchemDropAnalyzedData/FCVdata/20130523 NiFeCoCe/20130524 NiFeCoCe_plate3_FCV_4835'

if not os.path.exists(savefolder):
    os.mkdir(savefolder)
startpath_fom=os.path.join(savefolder, os.path.split(folder)[1])
fns=os.listdir(folder)
ext='txt'
fns=numpy.array([fn for fn in fns if 'FCVS' in fn and fn.endswith(ext) and fn.startswith('Sample')])
fnstartarr=numpy.array([fn.partition('_')[0] for fn in fns])

fnstartset=set(fnstartarr)

pathliststoread=[[os.path.join(folder, fn) for fn in fns[numpy.where(fnstartarr==fnstart)]] for fnstart in fnstartset]

dlist=[]
for pl in pathliststoread:
    saven=os.path.split(pl[0])[1].partition('_')[0]
    saven+='_FCVSanalysis.png'
    savep=os.path.join(savefolder, saven)
    pylab.figure(num=1)
    try:
        Capac, CurrIntercept, CapacFitR2, d=calccapacitivecurrent(pl, vscanrangefrac=(.15, .85), vendrangefrac=(.02, .98), vendtol=0.01, plotfignum=1, plotsavepath=savep, returndict=True)
    except:
        pylab.clf()
        print 'Failed analysis on ', pl
        continue
    dtemp={}
    for k  in ['Sample', 'elements', 'compositions', 'x', 'y', 'vstartinds_seg', 'vlen_seg','dEdt_seg', 'dIdE_seg', 'dEdtmean_cycs', 'delI_cycs', 'CC_dEdtfitpars', 'CC_dEdtfitR2', 'Capac', 'CurrIntercept', 'dIdt_fwdrevratio']:
        dtemp[k]=d[k]
#    dtemp['Capac']=Capac
#    dtemp['CurrIntercept']=CurrIntercept
#    dtemp['CapacFitR2']=CapacFitR2
    dlist+=[dtemp]
    pylab.clf()
#Capac, CurrIntercept=calccapacitivecurrent([p, p2],plotfignum=1)
#pylab.show()

def writefile(p, dlist, savedlist=True, fomkey='FOM'):
    
    if len(dlist)==0:
        print 'no data to save'
        return

    labels=['Sample', 'x(mm)', 'y(mm)']
    labels+=dlist[0]['elements']
    labels+=[fomkey]
    kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), (fomkey, '%.6e')]
    arr=[]
    for d in dlist:
        arr2=[]
        for k, fmt in kv_fmt:
            v=d[k]
            if isinstance(v, numpy.ndarray) or isinstance(v, list):
                for subv in v:
                    arr2+=[fmt %subv]
            else:
                arr2+=[fmt %v]
        arr+=['\t'.join(arr2)]
    s='\t'.join(labels)+'\n'
    s+='\n'.join(arr)
    
    f=open(p, mode='w')
    f.write(s)
    f.close()
    
    if savedlist:
        f=open(p[:-4]+'_dlist.pck', mode='w')
        pickle.dump(dlist, f)
        f.close()





for fomkey in ['Capac', 'CurrIntercept', 'CC_dEdtfitR2', 'dIdt_fwdrevratio']:
    p=startpath_fom+'_'+fomkey+'.txt'
    #p=p[::-1].replace('plate'[::-1], 'plate1'[::-1], 1)[::-1]#temporary fix for file naming for stacked_tern4
    writefile(p, dlist, savedlist=(fomkey=='Capac'), fomkey=fomkey)

dlist=[d for d in dlist if d['CC_dEdtfitR2']>.8]

for fomkey in ['Capac', 'CurrIntercept', 'CC_dEdtfitR2', 'dIdt_fwdrevratio']:
    p=startpath_fom+'_'+fomkey+'_filterR2.txt'
    #p=p[::-1].replace('plate'[::-1], 'plate1'[::-1], 1)[::-1]#temporary fix for file naming for stacked_tern4
    writefile(p, dlist, savedlist=(fomkey=='Capac'), fomkey=fomkey)

dlist=[d for d in dlist if (d['dIdt_fwdrevratio']>.8)&(d['dIdt_fwdrevratio']<1.25)] #lets the fwd:rev be between 4:5 and 5:4

for fomkey in ['Capac', 'CurrIntercept', 'CC_dEdtfitR2', 'dIdt_fwdrevratio']:
    p=startpath_fom+'_'+fomkey+'_filterR2fwdrevratio.txt'
    #p=p[::-1].replace('plate'[::-1], 'plate1'[::-1], 1)[::-1]#temporary fix for file naming for stacked_tern4
    writefile(p, dlist, savedlist=(fomkey=='Capac'), fomkey=fomkey)
