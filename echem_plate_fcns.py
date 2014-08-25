import numpy
from matplotlib.ticker import FuncFormatter
import matplotlib.colors as colors
from echem_plate_math import *
import time

def myexpformat(x, pos):
    for ndigs in range(5):
        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e-')
        if eval(lab)==x:
            return lab
    return lab
ExpTickLabels=FuncFormatter(myexpformat)

are_paths_equivalent=lambda path1, path2:os.path.normcase(os.path.abspath(path1))==os.path.normcase(os.path.abspath(path2))

def attemptnumericconversion(s):
    if (s.replace('.', '', 1).replace('e', '', 1).replace('+', '', 1).replace('-', '', 1)).isalnum():
        try:
            return myeval(s)
        except:
            pass
    return s

def readechemtxtold(path):
    f=open(path, mode='r')
    lines=f.readlines()
    f.close()
    d={}
    z=[]
    for l in lines:
        if l.startswith('%'):
            a, b, c=l.strip('%').strip().partition('=')
            a=a.strip()
            c=c.strip()
            if a=='elements' or a=='column_headings' or a=='compositions':
                val=[]
                while len(c)>0:
                    b, garb, c=c.strip().partition('\t')
                    val+=[b]
                if a=='compositions':
                    val=[attemptnumericconversion(v) for v in val]
                    try:
                        val=numpy.float32(val)
                        print val
                        if numpy.any(numpy.isnan(val)):
                            val=numpy.ones(len(val), dtype='float32')/len(val)
                        print val
                        break
                    except:
                        pass
            elif a=='x' or a=='y':
                val=attemptnumericconversion(c.replace('mm', '').strip())
            else:
                val=attemptnumericconversion(c)
            d[a]=val
        else:
            a=[]
            c=l.strip()
            while len(c)>0:
                b, garb, c=c.strip().partition('\t')
                a+=[myeval(b)]
            if len(z)==0 or len(a)==len(z[-1]):
                z+=[a]
    for k, arr in zip(d['column_headings'], numpy.float32(z).T):
        d[k]=arr
    return d
   

def readechemtxt(path, mtime_path_fcn=None):
    try:#need to sometimes try twice so might as well try 3 times
        f=open(path, mode='r')
    except:
        try:
            f=open(path, mode='r')
        except:
            f=open(path, mode='r')
    lines=f.readlines()
    f.close()
    d={}
    z=[]
    for count, l in enumerate(lines):
        if l.startswith('%'):
            a, b, c=l.strip('%').strip().partition('=')
            a=a.strip()
            c=c.strip()
            if a=='elements' or a=='column_headings' or a=='compositions':
                val=[]
                while len(c)>0:
                    b, garb, c=c.strip().replace('\\t', '\t').partition('\t')
                    val+=[b]
                if a=='compositions':
                    val=[attemptnumericconversion(v) for v in val]
                    try:
                        val=numpy.float32(val)
                        if numpy.any(numpy.isnan(val)):
                            raise
                    except:
                        val=numpy.ones(len(val), dtype='float32')/len(val)
                        pass
            elif a=='x' or a=='y':
                val=attemptnumericconversion(c.replace('mm', '').strip())
            else:
                val=attemptnumericconversion(c)
            d[a]=val
        else:
            break
    if len(lines[count:])==0:
        return {}
    try:
        z=[map(float, l.strip().replace('\\t', '\t').split('\t')) for l in lines[count:] if len(l.strip())>0]
    except:
        print l
        print '\t' in l
        print l.split('\t')
        print map(float, l.split('\t')) 
        raise
    for k, arr in zip(d['column_headings'], numpy.float32(z).T):
        d[k]=arr
    d['path']=path
    if not mtime_path_fcn is None:
        d['mtime']=mtime_path_fcn(path)
    return d
    


def getarrfromkey(dlist, key):
    return numpy.array([d[key] for d in dlist])



def col_string(s):
    s=s.strip()
    if ('(' in s) and (')' in s):
        try:
            s=eval(s)
        except:
            return None
    cc=colors.ColorConverter()
    return cc.to_rgb(s)

def unroundcompositions(dropd):
    c=dropd['compositions']
    dropd['compositions']=numpy.round(c*30.)/30.
    return
def addcodetoplatemapgen1dlist(dlist=None, dropd=None):
    code2lims=[(2081, 2109), (4193, 4221), (6305, 6333)]
    code2inds=[]
    for a, b in code2lims:
        code2inds+=range(a, b)
    if not dlist is None:
        for d in dlist:
            s=d['Sample']
            cs=d['compositions'].sum()
            if s in code2inds and cs>0.:
                d['code']=2
            elif cs==0.:
                d['code']=1
            else:
                d['code']=0
    else:
        s=dropd['Sample']
        cs=dropd['compositions'].sum(axis=1)
        code=numpy.zeros(len(s), dtype='int32')
        code2bool=numpy.array([sv in code2inds for sv in s])
        code[code2bool&(cs>0.0)]=2
        code[cs==0.0]=1
        dropd['code']=code
    return
#p='C:/Users/Gregoire/Documents/CaltechWork/echemdrop/20120728NiFeCoTiplate1_test21Aug2012/Sample63_x131_y45_A67B33C0D0_CV2.txt'
#c=time.time()
#d=readechemtxt(p)
#print time.time()-c
#c=time.time()
#dold=readechemtxtold(p)
#print time.time()-c
