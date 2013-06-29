import numpy, pylab, os, sys, csv
from echem_plate_fcns import *
from echem_plate_math import *
PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]
sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from echem_plate_ui import *
from echem_plate_math import *



#system 1
#dlistinfo=[\
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130402NiFeCoCe_Plate1_5500_dlist.dat', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate2_5498_dlist.dat', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate3_4835_dlist.dat', \
#      ], 'CV3'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130402NiFeCoCe_Plate1_5500_CP1Eave_dlist.pck', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate2_5498_CP1Eave_dlist.pck', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/20130403NiFeCoCe_Plate3_4835_CP1Eave_dlist.pck', \
#      ], 'CP1'), \
#    ]
#
#samples=[692, 693, 3022, 5047, 5050]
#savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results/selectsamplesnesteddlist.pck'

#system 2
#dlistinfo=[\
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130529NiFeCoCe_plate1_5577_dlist.dat', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130603NiFeCoCe_plate2_5498_dlist.dat', \
#      'C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/20130528NiFeCoCe_plate3_4835_dlist.dat', \
#      ], 'CV3'), \
#    ]
#
#samples=[692, 693, 3022, 5047, 5050]
#savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130528NiFeCoCe3platerescan/results/selectsamplesnesteddlist.pck'

#system 3
#dlistinfo=[\
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130605NiFeCoCe_plate1_CP_6220_CP4Eave_dlist.pck'], 'CP4'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130605NiFeCoCe_plate1_CP_6220_CP5Eave_dlist.pck'], 'CP5'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/2013060607NiFeCoCe_plate1_CP3_6220_CP6Eave_dlist.pck'], 'CP6'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130604NiFeCoCe_plate1_CV_6220_dlist.dat'], 'CV3'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/20130604NiFeCoCe_plate1_CV_6220_dlist_Tafelonly.dat'], 'Tafel'), \
#]
#samples=[169, 170, 725, 1326, 1329]+range(2049, 2056)+range(2057, 2064)+range(2065, 2072)+range(2073, 2079)
#savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130604NiFeCoCe/results/selectsamplesnesteddlist.pck'

##system 4
#dlistinfo=[\
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results/20130610NiFeCoCe_plate1_6321_dlist.dat'], 'CV3'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130612NiFeCoCe_plate1_CVpostCP_6321_dlist.dat'], 'CV3postCP'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130610NiFeCoCe_plate1_CP_6321_CP4Eave_dlist.pck'], 'CP4'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130610NiFeCoCe_plate1_CP_6321_CP5Eave_dlist.pck'], 'CP5'), \
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130612NiFeCoCesingle_6321/results/20130610NiFeCoCe_plate1_CP_6321_CP6Eave_dlist.pck'], 'CP6'), \
#]
#samples=[169, 170, 725, 1326, 1329]+range(2049, 2056)+range(2057, 2064)+range(2065, 2072)+range(2073, 2079)
#savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/20130610NiFeCoCesingle_6321/results/selectsamplesnesteddlist.pck'

##system 5
dlistinfo=[\
    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/benchmarkingCVs_dlist.pck'], 'bmcv'), \
    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/benchmarkingstepCPs_dlist.pck'], 'bmstepcp'), \
    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/benchmarkingstepCAs_dlist.pck'], 'bmstepca'), \
    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/benchmarking2hrCP_dlist.pck'], 'bm2hrcp'), \
]
samples=[170, 725, 1326]
savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/benchmarking/selectsamplesnesteddlist.pck'

##system 6
#dlistinfo=[\
#    (['C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/yunsamples/yunCV_dlist.pck'], 'CV'), \
#]
#samples=[169, 170, 725, 1326, 1329]+range(2049, 2056)+range(2057, 2064)+range(2065, 2072)+range(2073, 2079)
#savep='C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/yunsamples/selectsamplesnesteddlist.pck'

dall={}
for pl, lab in dlistinfo:
    for p in pl:
        f=open(p, mode='r')
        dlist=pickle.load(f)
        f.close()
        dlist=[d for d in dlist if d['Sample'] in samples]
        if lab in dall.keys():
            dall[lab]+=dlist
        else:
            dall[lab]=dlist

for k, v in dall.iteritems():
    print k, len(v)
    
f=open(savep, mode='w')
pickle.dump(dall, f)
f.close()
