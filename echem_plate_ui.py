import time
import os, os.path
import sys
import numpy
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import operator
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import numpy.ma as ma
import matplotlib.colors as colors
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pylab
import pickle
from echem_plate_math import *
from echem_plate_fcns import *

PyCodePath=os.path.split(os.path.split(os.path.realpath(__file__))[0])[0]

from matplotlib.ticker import FuncFormatter
from matplotlib.ticker import ScalarFormatter
def myexpformat_4digs(x, pos):
    return '%.3e' %x
#    for ndigs in range(4):
#        lab=(('%.'+'%d' %ndigs+'e') %x).replace('e+0','e').replace('e+','e').replace('e0','').replace('e-0','e')
#        if eval(lab)==x:
#            return lab
#    return lab

ExpTickLabels=FuncFormatter(myexpformat_4digs)
RegTickLabels=matplotlib.ticker.ScalarFormatter()

def autotickformat(ax, x=False, y=False, ndec=3):
    for bl, xax, lims in zip([x, y], [ax.xaxis, ax.yaxis], [ax.get_xlim(), ax.get_ylim()]):
        if bl:
            try:
                doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
                doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
            except:
                print 'error on axis formatter for lims ', lims
                continue
            if doit:
                xax.set_major_formatter(ExpTickLabels)
            else:
                xax.set_major_formatter(RegTickLabels)

def autocolorbarformat(lims, ndec=3):
    try:
        doit=numpy.max(numpy.log10(numpy.abs(numpy.array(lims))))<(-ndec)
        doit=doit or numpy.min(numpy.log10(numpy.abs(numpy.array(lims))))>ndec
    except:
        print 'error on axis formatter for lims ', lims
        return
    if doit:
        return ExpTickLabels
    else:
        return RegTickLabels

wd=os.getcwd()


sys.path.append(os.path.join(PyCodePath,'PythonCompositionPlots'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_stackedtern20 import *
from quaternary_FOM_stackedtern30 import *
from quaternary_FOM_bintern import *

sys.path.append(os.path.join(PyCodePath,'JCAPPyDBComm'))
from mysql_dbcommlib import *

sys.path.append(os.path.join(PyCodePath, 'PythonCodeSecureFiles'))
from paths import *
if os.path.isdir(EchemSavePath):
    os.chdir(EchemSavePath)


    
class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 0, 0)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        
def mygetopenfile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getOpenFileName(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getOpenFileName(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetopenfiles(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfns=QFileDialog.getOpenFileNames(xparent,''.join(['Select file to open:', markstr]),os.path.join(xpath, filename).replace('\\','/'))
        xparent.destroy()
        xapp.quit()
    else:
        returnfns=QFileDialog.getOpenFileNames(parent,''.join(['Select file to open: ', markstr]),os.path.join(xpath, filename).replace('\\','/'))
    return [str(s) for s in returnfns]

def mygetsavefile(parent=None, xpath="%s" % os.getcwd(),markstr='', filename='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getSaveFileName(xparent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getSaveFileName(parent,''.join(['Select file for save: ', markstr]),os.path.join(xpath, filename).replace('\\','/')))

def mygetdir(parent=None, xpath="%s" % os.getcwd(),markstr='' ):
    if parent is None:
        xapp = QApplication(sys.argv)
        xparent = QWidget()
        returnfn = unicode(QFileDialog.getExistingDirectory(xparent,''.join(['Select directory:', markstr]), xpath))
        xparent.destroy()
        xapp.quit()
        return returnfn
    return unicode(QFileDialog.getExistingDirectory(parent,''.join(['Select directory:', markstr]), xpath))
    

def userinputcaller(parent, inputs=[('testnumber', int)], title='Enter values',  cancelallowed=True):
    problem=True
    while problem:
        idialog=userinputDialog(parent, inputs, title)
        idialog.exec_()
        problem=idialog.problem
        if not idialog.ok and cancelallowed:
            return None
        inputs=[(tup[0], tup[1], s) for tup, s  in zip(inputs, idialog.inputstrlist)]
        
    return idialog.ans

class userinputDialog(QDialog):
    def __init__(self, parent, inputs=[('testnumber', int, '')], title='Enter values'):
        super(userinputDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
        self.parent=parent
        self.inputs=inputs
        self.lelist=[]
        for i, tup in enumerate(self.inputs):
            lab=QLabel()
            lab.setText(tup[0])
            le=QLineEdit()
            if len(tup)>2:
                le.setText(tup[2])
            self.lelist+=[le]
            mainlayout.addWidget(lab, 0, i, 1, 1)
            mainlayout.addWidget(le, 1, i, 1, 1)    
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox, 2, 0, len(inputs), 1)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        
        self.setLayout(mainlayout)
        
        
        QMetaObject.connectSlotsByName(self)
        
        self.problem=False
        self.ok=False

    def ExitRoutine(self):
        self.ok=True
        self.problem=False
        self.ans=[]
        self.inputstrlist=[str(le.text()).strip() for le in self.lelist]
        for s, tup in zip(self.inputstrlist, self.inputs):
            if tup[1]==str:
                try:
                    self.ans+=[s]
                except:
                    self.problem=True
                    break
            else:
                try:
                    n=myeval(s)
                    self.ans+=[tup[1](n)]
                except:
                    self.problem=True
                    break
        if self.problem:
            idialog=messageDialog(self, 'problem with conversion of ' + tup[0])
            idialog.exec_()

class selectdbsessionsDialog(QDialog):
    def __init__(self, parent, ex_trange_techl, maxsessions=15, title='Select DB experiment sessions to analyze'):
        super(selectdbsessionsDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QVBoxLayout()
        
        self.cblist=[]
        self.cbinds=[]
        for count,  (ex, (t0, t1), techl) in enumerate(ex_trange_techl[:maxsessions]):
            cb=QCheckBox()
            cb.setText('exp %d: %s to %s, %s' %(ex, str(t0), str(t1), ','.join(techl)))
            cb.setChecked(False)
            mainlayout.addWidget(cb)
            self.cblist+=[cb]
            self.cbinds+=[[count]]
        if len(ex_trange_techl)>maxsessions:
            cb=QCheckBox()
            ex, (t0, t1), techl=ex_trange_techl[maxsessions]
            ex2, (t02, t12), techl2=ex_trange_techl[-1]
            techl=list(set(techl+techl2))
            cb.setText('exp %d-%d: %s to %s, %s' %(ex, ex2, str(t0), str(t12), ','.join(techl)))
            cb.setChecked(True)
            mainlayout.addWidget(cb)
            self.cblist+=[cb]
            self.cbinds+=[range(maxsessions, len(ex_trange_techl))]
        cb.setChecked(True)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
         
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
        self.setLayout(mainlayout)
        QMetaObject.connectSlotsByName(self)
    def ExitRoutine(self):
        self.selectinds=[]
        for cb, l in zip(self.cblist, self.cbinds):
            if cb.isChecked():
                self.selectinds+=l
                
class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        #self.setupUi(self)
        self.setWindowTitle('Echem Visualization')
        self.echem=echemvisDialog(self, **kwargs)
        if execute:
            self.echem.exec_()
        if self.echem.dbdatasource is 1:
            try:
                self.echem.dbc.db.close()
            except:
                pass

class echem10axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem10axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make10ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
    def plot(self, d, cb=True):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        scatter_10axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])
        
class echem20axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem20axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make20ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
    def plot(self, d, cb=True):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        scatter_20axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])

class echem30axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem30axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make30ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
    def plot(self, d, cb=True):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        scatter_30axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])
        
        
class echem4axesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echem4axesWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=make4ternaxes(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
    def plot(self, d, cb=True):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        scatter_4axes(d['comps'], d['fom'], self.stpl, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])


class echembinWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D']):
        super(echembinWidget, self).__init__(parent)
        
        mainlayout=QVBoxLayout()
        
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axbin, self.axbininset=plotbinarylines_axandinset(fig=self.plotw.fig, ellabels=ellabels)
        
        mainlayout.addWidget(self.plotw)
        
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        mainlayout.addWidget(self.buttonBox)
        
        self.setLayout(mainlayout)
    
    def plot(self, d, cb=True, ellabels=['A', 'B', 'C', 'D']):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        plotbinarylines_quat(self.axbin, d['comps'], d['fom'], markersize=10, ellabels=d['ellabels'], linewidth=2)
        self.axbin.set_xlabel('binary composition', fontsize=16)
        self.axbin.set_ylabel(cblabel, fontsize=16)
        
        
class echemvisDialog(QDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(echemvisDialog, self).__init__(parent)
        self.parent=parent
#        self.echem30=echem30axesWidget()
#        self.echem30.show()
        self.plotillumkey=None
        
		#Uncomment out next line to disable db access
        #folderpath=PyCodePath
        if folderpath is None:
            self.dbdatasource=userinputcaller(self, inputs=[('DBsource?', int, '1')], title='Change to 0 to read for local harddrive.')[0]
            if self.dbdatasource is 1:
                self.dbc=None#self.createdbsession()
            elif self.dbdatasource is 2:
                if sys.platform.startswith('linux'):
                    self.kcomputers='/media/hteshare/computers'
                    self.kexperiments='/media/hteshare/experiments'
                elif sys.platform.startswith('win'):
                    self.kcomputers='K:\\computers'
                    self.kexperiments='K:\\experiments'
                elif sys.platform.startswith('darwin'):
                    self.kcomputers='/Volumes/HTEshare/home/computers'
                    self.kexperiments='/Volumes/HTEshare/home/experiments'
            else:
                self.kcomputers="%s" % os.getcwd()
                self.kexperiments="%s" % os.getcwd()
            print 'kcomputers is ' + self.kcomputers
        else:
            self.dbdatasource=0

        self.techniquedictlist=[]
        
        self.plotw_select=plotwidget(self)
#        self.plotw_select.axes.set_xlabel('')
#        self.plotw_select.axes.set_ylabel('')
        #self.plotw_select.axes.set_aspect(1)
        
        self.plotw_plate=plotwidget(self)
#        self.plotw_plate.axes.set_xlabel('')
#        self.plotw_plate.axes.set_ylabel('')
        self.plotw_plate.axes.set_aspect(1)
        
        self.plotw_tern=plotwidget(self)
#        self.plotw_tern.axes.set_xlabel('')
#        self.plotw_tern.axes.set_ylabel('')
        #self.plotw_tern.axes.set_aspect(1)
        
        self.plotw_quat=plotwidget(self, projection3d=True)
#        self.plotw_quat.axes.set_xlabel('')
#        self.plotw_quat.axes.set_ylabel('')
        #self.plotw_quat.axes.set_aspect(1)
        
        self.plotw_aux=plotwidget(self)
#        self.plotw_aux.axes.set_xlabel('')
#        self.plotw_aux.axes.set_ylabel('')
        #self.plotw_aux.axes.set_aspect(1)
        
        axrect=[0.82, 0.1, 0.04, 0.8]
        
        
        self.plotw_plate.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_plate=self.plotw_plate.fig.add_axes(axrect)
        
        self.plotw_tern.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_tern=self.plotw_tern.fig.add_axes(axrect)
        
        self.plotw_quat.fig.subplots_adjust(left=0, right=axrect[0]-.01)
        self.cbax_quat=self.plotw_quat.fig.add_axes(axrect)
        
        self.plotw_select.fig.subplots_adjust(left=.2)
        self.plotw_aux.fig.subplots_adjust(left=.2)


        QObject.connect(self.plotw_plate, SIGNAL("genericclickonplot"), self.plateclickprocess)
        
#in options, always make an option that does not require user input at index 0
        CVops=[\
        ['Imax', ['I(A)'], []], \
        ['Imin', ['I(A)'], []], \
        ['E_Ithresh', ['I(A)','Ewe(V)'], [['Ithresh(A)', float, '1e-5'], ['Num consec points', int, '20'], ['0 for below, 1 for above', int, '1'], ['Thresh not reached value', float, '1']]], \
        ['Eh in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
        ['Io in I=Io Exp(E/Eh)', ['I(A)', 'Ewe(V)'], []], \
        ['Iphoto_max', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Iphoto_min', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
        ['None', ['I(A)', 'Ewe(V)'], []], \
        ]
        
        OCVops=[\
        ['Efin', ['Ewe(V)'], []], \
        ['Eave', ['Ewe(V)', 't(s)'], [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        CPops=[\
        ['Efin', ['Ewe(V)'], []], \
        ['Eave', ['Ewe(V)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Ess', ['Ewe(V)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Ephoto', ['Illum', 'Ewe(V)', 'I(A)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        CAops=[\
        ['Ifin', ['I(A)'], []], \
        ['Iave', ['I(A)', 't(s)'],  [['Interval(s)', float, '2.'], ['Num StdDev outlier', float, '2.'], ['Num Pts in Window', int, '999999'], ['0 from beginning, 1 from end', int, '1']]], \
        ['Iss', ['I(A)'], [['Weight Exponent for NumPts', float, '1.'], ['NumPts test interval', int, '10']]], \
        ['Iphoto', ['Illum', 'I(A)', 'Ewe(V)', 't(s)'], [['frac of Illum segment start', float, '0.4'], ['frac of Illum segment end', float, '0.95'], ['frac of Dark segment start', float, '0.4'], ['frac of Dark segment end', float, '0.95'], ['Illum signal key', str, 'Toggle'], ['Illum signal time shift (s)', float, '0.'], ['Illum Threshold', float, '0.5'], ['Illum Invert', int, '0'], ['num illum cycles', int, '2'], ['0 from beginning, 1 from end', int, '1']]], \
        ]
        
        Bubbleops=[\
        ['slopefin', ['Maxslope'], []], \
        ['Intfin', ['Intensity'], []], \
        ]
        
        
        self.expmnt_calc_options=[['OCV', OCVops], ['CP', CPops], ['CA', CAops], ['CV', CVops], ['Bubble', Bubbleops]]
        self.expmnt_calc_lastusedvals=[[[] for calcopt in opslist] for opname, opslist in self.expmnt_calc_options]
        expmntComboBoxLabel=QLabel()
        expmntComboBoxLabel.setText('Technique type:')
        self.expmntComboBox=QComboBox()
        for i, tup in enumerate(self.expmnt_calc_options):
            self.expmntComboBox.insertItem(i, tup[0])
        self.expmntComboBox.setCurrentIndex(0)
        
        calcoptionComboBoxLabel=QLabel()
        calcoptionComboBoxLabel.setText('FOM:')
        self.calcoptionComboBox=QComboBox()
        
        ternskipComboBoxLabel=QLabel()
        ternskipComboBoxLabel.setText('Exclude for ternary:')
        self.ternskipComboBox=QComboBox()
        for i, l in enumerate(['A', 'B', 'C', 'D']):
            self.ternskipComboBox.insertItem(i, l)
        self.ternskipComboBox.setCurrentIndex(i)
        
        QObject.connect(self.expmntComboBox,SIGNAL("activated(QString)"),self.fillcalcoptions)
        QObject.connect(self.calcoptionComboBox,SIGNAL("activated(QString)"),self.getcalcparams)
        
        self.xplotchoiceComboBox=QComboBox()
        self.yplotchoiceComboBox=QComboBox()
        self.plotkeys=['t(s)', 'I(A)', 'Ewe(V)', 'Ece(V)', 'Ewe-E0(V)', 'I*Is(A)']
        #keys=['Intensity', 'Fit', 'Maxslope']
        for i, nam in enumerate(self.plotkeys):
            self.xplotchoiceComboBox.insertItem(i, nam)
            self.yplotchoiceComboBox.insertItem(i, nam)
        self.xplotchoiceComboBox.setCurrentIndex(0)
        self.yplotchoiceComboBox.setCurrentIndex(1)
        
        xplotchoiceComboBoxLabel=QLabel()
        xplotchoiceComboBoxLabel.setText('x-axis')
        yplotchoiceComboBoxLabel=QLabel()
        yplotchoiceComboBoxLabel.setText('y-axis')
        
        expmntLineEditLabel=QLabel()
        expmntLineEditLabel.setText('Technique Name:')
        self.expmntLineEdit=QLineEdit()
        self.expmntLineEdit.setText('OCV0')
        
        folderButton=QPushButton()
        folderButton.setText("select\nfolder")
        QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfolder)
        
        plotButton=QPushButton()
        plotButton.setText("update\nfigures")
        QObject.connect(plotButton, SIGNAL("pressed()"), self.calcandplot)
        QObject.connect(plotButton, SIGNAL("pressed()"), self.writefileauto)
        
        updateButton=QPushButton()
        updateButton.setText("update\ndata")
        QObject.connect(updateButton, SIGNAL("pressed()"), self.calcandplotwithupdate)
        
        saveButton=QPushButton()
        saveButton.setText("save FOM\nspreadhseet")
        QObject.connect(saveButton, SIGNAL("pressed()"), self.writefile)
        
        savesampleButton=QPushButton()
        savesampleButton.setText("save select\nsample IDs")
        QObject.connect(savesampleButton, SIGNAL("pressed()"), self.writesamplelist)
        
        savebuttonlayout=QHBoxLayout()
        savebuttonlayout.addWidget(folderButton)
        savebuttonlayout.addWidget(plotButton)
        savebuttonlayout.addWidget(updateButton)
        savebuttonlayout.addWidget(saveButton)
        savebuttonlayout.addWidget(savesampleButton)
#        savebuttonlayout=QHBoxLayout()
#        savebuttonlayout.addWidget(saveButton)
#        savebuttonlayout.addWidget(savesampleButton)
        
        self.infoLabel=QLabel()
        self.infodef='Q=10,15,40,80 1/nm -> \nd=0.63,0.42,0.16,0.079 nm\n'
        
        self.revcmapCheckBox=QCheckBox()
        self.revcmapCheckBox.setText('reverse cmap?')
        
        templab=QLabel()
        templab.setText('min,max colorbar')
        
        self.vminmaxLineEdit=QLineEdit()
        
        vminmaxlayout=QVBoxLayout()
        vminmaxlayout.addWidget(templab)
        vminmaxlayout.addWidget(self.vminmaxLineEdit)

        templab=QLabel()
        templab.setText('below,above range colors:\nEnter a char,0-1 gray,tuple,\n"None" for ignore')
        
        self.aboverangecolLineEdit=QLineEdit()
        self.aboverangecolLineEdit.setText('k')
        self.belowrangecolLineEdit=QLineEdit()
        self.belowrangecolLineEdit.setText('0.9')
        
        outrangecollayout=QGridLayout()
        outrangecollayout.addWidget(templab, 0, 0, 2, 1)
        outrangecollayout.addWidget(self.belowrangecolLineEdit, 0, 1)
        outrangecollayout.addWidget(self.aboverangecolLineEdit, 1, 1)
        
        self.statusLineEdit=QLineEdit()
        self.statusLineEdit.setReadOnly(True)
        
        templab=QLabel()
        templab.setText('DAQ time')
        self.daqtimeLineEdit=QLineEdit()
        daqtimelayout=QVBoxLayout()
        daqtimelayout.addWidget(templab)
        daqtimelayout.addWidget(self.daqtimeLineEdit)
        
        stackedtern10Button=QPushButton()
        stackedtern10Button.setText("Create stacked\ntern at 10%")
        QObject.connect(stackedtern10Button, SIGNAL("pressed()"), self.stackedtern10window)
        
        stackedtern20Button=QPushButton()
        stackedtern20Button.setText("Create stacked\ntern at 5%")
        QObject.connect(stackedtern20Button, SIGNAL("pressed()"), self.stackedtern20window)
        
        stackedtern30Button=QPushButton()
        stackedtern30Button.setText("Create stacked\ntern at 3.33%")
        QObject.connect(stackedtern30Button, SIGNAL("pressed()"), self.stackedtern30window)
        
        tern4Button=QPushButton()
        tern4Button.setText("Create ternary\nfaces")
        QObject.connect(tern4Button, SIGNAL("pressed()"), self.tern4window)

        binlinesButton=QPushButton()
        binlinesButton.setText("Create binary\nlines")
        QObject.connect(binlinesButton, SIGNAL("pressed()"), self.binlineswindow)        
        
        templab=QLabel()
        templab.setText('E0=Equil.Pot.(V):')
        self.E0SpinBox=QDoubleSpinBox()
        self.E0SpinBox.setDecimals(3)
        self.E0SpinBox.setMaximum(10)
        self.E0SpinBox.setMinimum(-10)
        self.E0SpinBox.setValue(0)
        E0layout=QHBoxLayout()
        E0layout.addWidget(templab)
        E0layout.addWidget(self.E0SpinBox)
        
        templab=QLabel()
        templab.setText('Is=I scaling:')
        self.IsSpinBox=QDoubleSpinBox()
        self.IsSpinBox.setMaximum(10.)
        self.IsSpinBox.setMinimum(-10.)
        self.IsSpinBox.setValue(1.)
        Islayout=QHBoxLayout()
        Islayout.addWidget(templab)
        Islayout.addWidget(self.IsSpinBox)
        
        self.overlayselectCheckBox=QCheckBox()
        self.overlayselectCheckBox.setText("overlay on\n'select' plot")
        self.legendselectLineEdit=QLineEdit()
        self.legendselectLineEdit.setText('4')
        templab=QLabel()
        templab.setText("'select' plot\nlegend loc (int)")
        legendlayout=QVBoxLayout()
        legendlayout.addWidget(templab)
        legendlayout.addWidget(self.legendselectLineEdit)
        
        
        
        selectbuttonlayout=QHBoxLayout()
        selectbuttonlab=QLabel()
        selectbuttonlab.setText("Select samples by mouse right-click\n  OR filter FOM in this range:")
        #selectbuttonlayout.addWidget(templab, 0, 0, 1, 3)
        
        selectbelowButton=QPushButton()
        selectbelowButton.setText("(-INF,min)")
        QObject.connect(selectbelowButton, SIGNAL("pressed()"), self.selectbelow)
        selectbuttonlayout.addWidget(selectbelowButton)#, 1, 0)
        
        selectbetweenButton=QPushButton()
        selectbetweenButton.setText("[min,max)")
        QObject.connect(selectbetweenButton, SIGNAL("pressed()"), self.selectbetween)
        selectbuttonlayout.addWidget(selectbetweenButton)#, 1, 1)
        
        selectaboveButton=QPushButton()
        selectaboveButton.setText("[max,INF)")
        QObject.connect(selectaboveButton, SIGNAL("pressed()"), self.selectabove)
        selectbuttonlayout.addWidget(selectaboveButton)#, 1, 2)
    
        
        selectsamplelab=QLabel()
        selectsamplelab.setText("sample IDs selected for export")
        #selectsamplelayout=QVBoxLayout()
        #selectsamplelayout.addWidget(templab)
        self.selectsamplesLineEdit=QLineEdit()
        #selectsamplelayout.addWidget(self.selectsamplesLineEdit)
        
        self.ctrlgriditems=[\
        (expmntComboBoxLabel, self.expmntComboBox, 0, 0), \
        (calcoptionComboBoxLabel, self.calcoptionComboBox, 0, 1), \
        (expmntLineEditLabel, self.expmntLineEdit, 0, 2), \
        (xplotchoiceComboBoxLabel, self.xplotchoiceComboBox, 1, 0), \
        (yplotchoiceComboBoxLabel, self.yplotchoiceComboBox, 1, 1), \
        (ternskipComboBoxLabel, self.ternskipComboBox, 1, 2), \
        ]
        
        mainlayout=QGridLayout()
        ctrllayout=QGridLayout()
        for labw, spw, i, j in self.ctrlgriditems:
            templayout=QHBoxLayout()
            templayout.addWidget(labw)
            templayout.addWidget(spw)
            ctrllayout.addLayout(templayout, i+1, j)
        
#        ctrllayout.addWidget(folderButton, 0, 0)
#        ctrllayout.addWidget(plotButton, 0, 1)
        ctrllayout.addLayout(savebuttonlayout, 0, 0, 1, 4)
        
        ctrllayout.addWidget(self.revcmapCheckBox, i+2, 0)
        ctrllayout.addLayout(vminmaxlayout, i+2, 1)
        ctrllayout.addLayout(outrangecollayout, i+2, 2)
        
        ctrllayout.addWidget(self.statusLineEdit, i+3, 0)
        ctrllayout.addWidget(self.overlayselectCheckBox, i+3, 1)
        ctrllayout.addLayout(legendlayout, i+3, 2)
        
        ctrllayout.addLayout(daqtimelayout, i+4, 0)
        ctrllayout.addWidget(stackedtern10Button, i+4, 1)
        ctrllayout.addWidget(stackedtern30Button, i+4, 2)
        ctrllayout.addWidget(stackedtern20Button, i+5, 0)
        ctrllayout.addWidget(tern4Button, i+5, 1)
        ctrllayout.addWidget(binlinesButton, i+5, 2)
        
        ctrllayout.addLayout(E0layout, i+6, 0, 1, 2)
        ctrllayout.addLayout(Islayout, i+6, 2, 1, 2)
        
        ctrllayout.addWidget(selectbuttonlab, i+7, 0)
        #ctrllayout.addLayout(selectsamplelayout, i+6, 1, 1, 2)
        ctrllayout.addWidget(selectsamplelab, i+7, 1, 1, 2)
        
        ctrllayout.addLayout(selectbuttonlayout, i+8, 0)
        ctrllayout.addWidget(self.selectsamplesLineEdit, i+8, 1, 1, 2)
        
        mainlayout.addLayout(ctrllayout, 0, 0)
        mainlayout.addWidget(self.plotw_select, 0, 1)
        mainlayout.addWidget(self.plotw_aux, 0, 2)
        mainlayout.addWidget(self.plotw_plate, 1, 0)
        mainlayout.addWidget(self.plotw_quat, 1, 1)
        mainlayout.addWidget(self.plotw_tern, 1, 2)
        
        
        self.setLayout(mainlayout)
        
        self.fillcalcoptions()
        self.statusLineEdit.setText('idle')
        self.plate_id=None
        if folderpath is None:
            self.folderpath=None
            self.selectfolder()
            self.calcandplot()
        else:
            self.folderpath=folderpath
        self.resize(1600, 750)
    
    def createdbsession(self):        
        ans=userinputcaller(self, inputs=[('user:', str, ''), ('password:', str, '')], title='Enter database credentials', cancelallowed=True)
        if ans is None:
            return
        self.dbc=dbcomm(user=ans[0].strip(), password=ans[1].strip(),db='hte_echemdrop_proto')
        
    def selectfolder(self, plate_id=None, selectexids=None, folder=None):
        self.statusLineEdit.setText('waiting for folder input')
        if self.dbdatasource is 1:
            if not self.dbc is None:
                self.dbc.db.close()
            self.createdbsession()
            
            if self.folderpath is None:
                self.folderpath=mygetdir(self, markstr='select folder for saving results')
            if plate_id is None:
                ans=userinputcaller(self, inputs=[('plate ID:', int, '')], title='Enter plate ID for analysis', cancelallowed=not self.plate_id is None)[0]
                if ans is None:
                    return
                self.plate_id=ans
            else:
                self.plate_id=plate_id
            fields=['id', 'sample_no','created_at', 'experiment_no', 'technique_name', 'dc_data__t_v_a_c_i']
            self.dbrecarrd=self.dbc.getarrd_scalarfields('plate_id', self.plate_id, fields, valcvtcstr='%d')
            print len(self.dbrecarrd['id']),  ' records found'
            if len(self.dbrecarrd['id'])==0:
                print 'NO DB RECORDS FOUND FOR PLATE ', self.plate_id
                return
            if selectexids is None:
                self.userselectdbinds()
            else:
                self.selectexids=selectexids
            inds=numpy.concatenate([numpy.where(self.dbrecarrd['experiment_no']==exid)[0] for exid in self.selectexids])        
            for k, v in self.dbrecarrd.iteritems():
                self.dbrecarrd[k]=v[inds]
        else:
            if folder is None:
                self.folderpath=mygetdir(self, markstr='containing echem data .txt for single plate', xpath=self.kcomputers)
            else:
                self.folderpath=folder
            os.chdir(self.kexperiments)
        self.statusLineEdit.setText('idle')
        self.setWindowTitle(str(os.path.split(self.folderpath)[1]))
        #self.calcandplot()
        
        
        
#        id=numpy.array(self.dbrecarrd['id'])
#        sn=numpy.array(self.dbrecarrd['sample_no'])
#        tn=numpy.array(self.dbrecarrd['technique_name'])
    def userselectdbinds(self):
        t=self.dbrecarrd['created_at']
        ex=self.dbrecarrd['experiment_no']
        tn=self.dbrecarrd['technique_name']
        
        exset=sorted(list(set(ex)))
        ex_trange_techl=[(exv, numpy.sort(t[ex==exv])[[0,-1]], list(set(tn[[ex==exv]]))) for exv in exset]
        
        idialog=selectdbsessionsDialog(self, ex_trange_techl=ex_trange_techl)
        idialog.exec_()
        exsetinds=idialog.selectinds
        self.selectexids=[exset[i] for i in exsetinds]
        



    
    def fillcalcoptions(self, batchmode=False):
        i=self.expmntComboBox.currentIndex()
        self.calcoptionComboBox.clear()
        for i, tup in enumerate(self.expmnt_calc_options[i][1]):
            self.calcoptionComboBox.insertItem(i, tup[0])
        self.calcoptionComboBox.setCurrentIndex(0)
        if not batchmode:
            self.getcalcparams()
        exstr=str(self.expmntComboBox.currentText())
        if not exstr in str(self.expmntLineEdit.text()):
            self.expmntLineEdit.setText('%s0' %exstr)
            for i in range(1, 10):
                techstr='%s%d' %(exstr, i)
                if True in [techstr in d['path'] for d in self.techniquedictlist]:
                    self.expmntLineEdit.setText(techstr)
                    break
                    
    def getcalcparams(self):
        i=self.expmntComboBox.currentIndex()
        j=self.calcoptionComboBox.currentIndex()
        tup=self.expmnt_calc_options[i][1][j]
        inputs=tup[2]
        if len(self.expmnt_calc_lastusedvals[i][j])==len(inputs):
            for count, v in enumerate(self.expmnt_calc_lastusedvals[i][j]):
                inputs[count][2]=(isinstance(v, str) and (v,) or (`v`,))[0]
        if len(inputs)>0:
            self.CalcParams=userinputcaller(self, inputs=inputs, title='Enter Calculation Parameters')
            self.expmnt_calc_lastusedvals[i][j]=self.CalcParams
            print type(self.expmnt_calc_lastusedvals[i][j]), self.expmnt_calc_lastusedvals[i][j]
        #self.CalcAllFOM()
        #self.plot()
    
    def CalcFOM(self):
        self.plotillumkey=None
        techdict=self.techniquedictlist[self.selectind]
        i=self.expmntComboBox.currentIndex()
        j=self.calcoptionComboBox.currentIndex()
        tup=self.expmnt_calc_options[i][1][j]
        fcnnam=tup[0]
        self.calckeys=tup[1]
        if fcnnam=='Ifin' or fcnnam=='Efin':
            returnval=techdict[self.calckeys[0]][-1]
        elif fcnnam=='Imax' or fcnnam=='Emax':
            returnval=numpy.max(techdict[self.calckeys[0]])
        elif fcnnam=='Imin' or fcnnam=='Emin':
            returnval=numpy.min(techdict[self.calckeys[0]])
        elif fcnnam=='Iss' or fcnnam=='Ess':
            returnval=CalcArrSS(techdict[self.calckeys[0]], WeightExp=self.CalcParams[0], TestPts=self.CalcParams[1])
        elif fcnnam=='Iave' or fcnnam=='Eave':
            x=techdict[self.calckeys[0]]
            t=techdict[self.calckeys[1]]
            if self.CalcParams[3]:
                x=x[::-1]
                t=t[::-1]
            x=x[numpy.abs(t-t[0])<self.CalcParams[0]]
            x=removeoutliers_meanstd(x, self.CalcParams[2]//2, self.CalcParams[1])
            returnval=x.mean()
        elif fcnnam=='Eh in I=Io Exp(E/Eh)' or fcnnam=='Io in I=Io Exp(E/Eh)':
            print 'not implemented yet'
            returnval=0.
        elif fcnnam=='E_Ithresh':
            i=techdict[self.calckeys[0]]
            v=techdict[self.calckeys[1]]
            icrit=self.CalcParams[0]
            if not self.CalcParams[2]:
                i*=-1
                icrit*=-1
            b=numpy.int16(i>=icrit)
            n=self.CalcParams[1]
            bconsec=[b[i:i+n].prod() for i in range(len(b)-n)]
            if True in bconsec:
                i=bconsec.index(True)
                returnval=v[i:i+n].mean()
            else:
                returnval=self.CalcParams[3]
        elif 'photo' in fcnnam:
            ikey=self.CalcParams[4]
            tshift=self.CalcParams[5]
            if tshift!=0:
                newikey='IllumMod'
                techdict[newikey]=illumtimeshift(techdict, ikey, self.calckeys[3], tshift)
                ikey=newikey
                if self.CalcParams[7]!=0:
                    techdict[ikey]*=-1
            elif self.CalcParams[7]!=0:
                newikey='IllumMod'
                techdict[newikey]=-1*techdict[ikey]
                ikey=newikey
            
            illkey=self.calckeys[1]+'_illdiff'
            err=calcdiff_ill_caller(techdict, ikey=ikey, thresh=self.CalcParams[6], ykeys=[self.calckeys[1]], xkeys=list(self.calckeys[2:]), illfracrange=(self.CalcParams[0], self.CalcParams[1]), darkfracrange=(self.CalcParams[2], self.CalcParams[3]))
            try:
				if err or len(techdict[illkey])==0:
					return 0
				self.plotillumkey='IllumBool'
				
				ncycs=self.CalcParams[8]
				fromend=self.CalcParams[9]
				if fromend:
					arr=techdict[illkey][::-1]
				else:
					arr=techdict[illkey]
				arr=arr[:ncycs]
				
				if 'min' in fcnnam:
					returnval=min(arr)
				elif 'max' in fcnnam:
					returnval=max(arr)
				else:
					returnval=numpy.mean(arr)
            except:
				return 0
        else:
            print 'FOM function not understood'
            return 0.
        if fcnnam.startswith('I'):
            return returnval*self.IsSpinBox.value()
        if fcnnam.startswith('E'):
            return returnval-self.E0SpinBox.value()
        else:
            return returnval
            
    def CalcAllFOM(self):
        for i, d in enumerate(self.techniquedictlist):
            self.selectind=i
            d['FOM']=self.CalcFOM()

    def get_techniquedictlist(self, ext='.txt', nfiles=99999, dbupdate=False):
        self.statusLineEdit.setText('calculating FOM')
        dlist=[]
        existpaths=[d['path'] for d in self.techniquedictlist]
        existmtimes=[d['mtime'] for d in self.techniquedictlist]
        self.selectind=-1
        
        techname=str(self.expmntLineEdit.text())
        
        if self.dbdatasource is 1:
            if len(techname)==0 and len(self.techniquedictlist)==0:
                technamedflt=self.dbrecarrd['technique_name'][0]
                for i, tup in enumerate(self.expmnt_calc_options):
                    if technamedflt.startswith(tup[0]):
                        self.expmntComboBox.setCurrentIndex(i)
                        self.expmntLineEdit.setText(technamedflt)
                        self.fillcalcoptions()
                        break
            
            if dbupdate:
                ##this line for getting updated data
                self.selectfolder(plate_id=self.plate_id, selectexids=self.selectexids)
            
            fns=self.dbrecarrd['dc_data__t_v_a_c_i'][self.dbrecarrd['technique_name']==techname]
            
            pathstoread=[os.path.join(os.path.join('J:/hte_echemdrop_proto/data','%d' %self.plate_id), fn) for fn in fns]
            updateexcludebool=True
            
            dlist=[(p in existpaths and (self.techniquedictlist[existpaths.index(p)],) or (readechemtxt(p, mtime_path_fcn=self.getepoch_path),))[0] for p in pathstoread[:nfiles]]

        else:
            fns=os.listdir(self.folderpath)
            if len(techname)==0 and len(self.techniquedictlist)==0:
                for i, tup in enumerate(self.expmnt_calc_options):
                    techstr='%s0' %tup[0]
                    if True in [techstr in fn for fn in fns]:
                        self.expmntComboBox.setCurrentIndex(i)
                        self.expmntLineEdit.setText(techstr)
                        self.fillcalcoptions()
                        break
            pathstoread=[os.path.join(self.folderpath, fn) for fn in fns if techname in fn and fn.endswith(ext) and fn.startswith('Sample')]
        
            updateexcludebool=True
            
            for p in pathstoread[:nfiles]:
                mtime=self.getepoch_path(p)#os.path.getmtime(p)
                if p in existpaths and existmtimes[existpaths.index(p)]==mtime:
                    dlist+=[self.techniquedictlist[existpaths.index(p)]]
                    updateexcludebool=False
                else:
                    d=readechemtxt(p)
                    d['path']=p
                    d['mtime']=mtime
                    dlist+=[d]

        inds=numpy.argsort(getarrfromkey(dlist, 'mtime'))
        self.techniquedictlist=[dlist[i] for i in inds]
        if len(self.techniquedictlist)>0:
            d=self.techniquedictlist[0]
            maxlen=max([len(v) for k, v in d.items() if isinstance(v, numpy.ndarray)])
            plotkeys=set([k for k, v in d.items() if isinstance(v, numpy.ndarray) and len(v)==maxlen])
            #plotkeys=set(.keys())-set(['path', 'mtime'])
            if set(self.plotkeys)!=plotkeys:
                self.plotkeys=list(plotkeys)
                self.xplotchoiceComboBox.clear()
                self.yplotchoiceComboBox.clear()
                for i, nam in enumerate(self.plotkeys):
                    self.xplotchoiceComboBox.insertItem(i, nam)
                    self.yplotchoiceComboBox.insertItem(i, nam)
                self.xplotchoiceComboBox.setCurrentIndex(0)
                self.yplotchoiceComboBox.setCurrentIndex(1)
    def getepoch_path(self, p, readbytes=1000):
        try:
            #print os.path.exists(p), p
            try:#need to sometimes try twice so might as well try 3 times
                f=open(p, mode='r')
            except:
                try:
                    f=open(p, mode='r')
                except:
                    f=open(p, mode='r')
            s=f.read(readbytes)
            f.close()
            return eval (s.partition('Epoch=')[2].partition('\n')[0].strip())
        except:
            return 0.
    
    def calcandplotwithupdate(self, ext='.txt'):
        self.calcandplot(ext='.txt', dbupdate=True)
        
    def calcandplot(self, ext='.txt', dbupdate=False):
        self.get_techniquedictlist(ext=ext, dbupdate=dbupdate)
        
        for i, d in enumerate(self.techniquedictlist):
            self.selectind=i
            #if not 'FOM' in d.keys(): 
            d['FOM']=self.CalcFOM()
        
        i0=self.ternskipComboBox.currentIndex()
        if len(self.techniquedictlist)>0: #and updateexcludebool
            self.ternskipComboBox.clear()
            for i, l in enumerate(self.techniquedictlist[0]['elements']):
                self.ternskipComboBox.insertItem(i, l)
            self.ternskipComboBox.setCurrentIndex(i0)
        self.statusLineEdit.setText('idle')
        self.plot()
        

    def plot(self):
        self.statusLineEdit.setText('plotting')
        s=25
        
        self.plotw_tern.axes.cla()
        self.plotw_quat.axes.cla()
        self.plotw_plate.axes.cla()
        self.plotw_aux.axes.cla()
        self.cbax_quat.cla()
        self.cbax_tern.cla()
        self.cbax_plate.cla()
        
        if len(self.techniquedictlist)==0:
            self.statusLineEdit.setText('idle')
            return
#        m=self.plotw_tern.axes.scatter(self.detx, self.detz, c=self.dsp, s=s, edgecolors='none')
#        cb=self.plotw_tern.fig.colorbar(m, cax=self.cbax_tern)
#        cb.set_label('d-spacing (nm)')
        
        getarr=lambda k:getarrfromkey(self.techniquedictlist, k)
        fom=getarr('FOM')
        sample=getarr('Sample')
        
        if self.revcmapCheckBox.isChecked():
            cmap=cm.jet_r
        else:
            cmap=cm.jet
        
        clip=True
        skipoutofrange=[False, False]
        self.vmin=fom.min()
        self.vmax=fom.max()
        vstr=str(self.vminmaxLineEdit.text()).strip()
        if ',' in vstr:
            a, b, c=vstr.partition(',')
            try:
                a=myeval(a.strip())
                c=myeval(c.strip())
                self.vmin=a
                self.vmax=c
                for count, (fcn, le) in enumerate(zip([cmap.set_under, cmap.set_over], [self.belowrangecolLineEdit, self.aboverangecolLineEdit])):
                    vstr=str(le.text()).strip()
                    vstr=vstr.replace('"', '').replace("'", "")
                    print '^^^', vstr, 'none' in vstr or 'None' in vstr
                    if 'none' in vstr or 'None' in vstr:
                        skipoutofrange[count]=True
                        continue
                    if len(vstr)==0:
                        continue
                    c=col_string(vstr)
                    try:
                        fcn(c)
                        clip=False
                    except:
                        print 'color entry not understood:', vstr
                
            except:
                pass
        
        norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
        print 'fom min, max, mean, std:', fom.min(), fom.max(), fom.mean(), fom.std()
        
        comps=getarr('compositions')
        x=getarr('x')
        y=getarr('y')
        print 'skipoutofrange', skipoutofrange
        print len(fom)
        if skipoutofrange[0]:
            inds=numpy.where(fom>=self.vmin)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]
        print len(fom)
        if skipoutofrange[1]:
            inds=numpy.where(fom<=self.vmax)
            fom=fom[inds]
            comps=comps[inds]
            x=x[inds]
            y=y[inds]
        print len(fom)
        
        
        if numpy.any(fom>self.vmax):
            if numpy.any(fom<self.vmin):
                extend='both'
            else:
                extend='max'
        elif numpy.any(fom<self.vmin): 
            extend='min'
        else:
            extend='neither'
        print 'extend ', extend
        m=self.plotw_plate.axes.scatter(x, y, c=fom, s=s, marker='s', cmap=cmap, norm=norm)
        cb=self.plotw_plate.fig.colorbar(m, cax=self.cbax_plate, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        #cb.set_label('|Q| (1/nm)')
        
        
        comps=numpy.array([c[:4]/c[:4].sum() for c in comps])
        i=self.ternskipComboBox.currentIndex()
        inds=[j for j in range(4) if j!=i][:3]
        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
        reordercomps=comps[:, inds+[i]]
        self.ellabels=self.techniquedictlist[0]['elements']
        reorderlabels=[self.ellabels[j] for j in inds+[i]]
        
        
        quat=QuaternaryPlot(self.plotw_quat.axes, ellabels=self.ellabels, offset=0)
        quat.label()
        quat.scatter(comps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
        cb=self.plotw_quat.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        
        fomlabel=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText())))
        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel)])
        
        tern=TernaryPlot(self.plotw_tern.axes, ellabels=reorderlabels[:3], offset=0)
        tern.label()
        tern.scatter(terncomps, c=fom, s=s, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
        cb=self.plotw_tern.fig.colorbar(tern.mappable, cax=self.cbax_tern, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
        
        self.plotw_aux.axes.plot(fom, 'g.-')
        self.plotw_aux.axes.set_xlabel('sorted by experiment time')
        self.plotw_aux.axes.set_ylabel('FOM')
        autotickformat(self.plotw_aux.axes, x=0, y=1)
        
        self.plotw_quat.axes.mouse_init()
        self.plotw_quat.axes.set_axis_off()
        self.plotw_tern.fig.canvas.draw()
        self.plotw_quat.fig.canvas.draw()
        self.plotw_plate.fig.canvas.draw()
        self.plotw_aux.fig.canvas.draw()
        
        self.selectind=-1
        self.plotselect()
        self.statusLineEdit.setText('idle')

    def stackedtern10window(self):
        d=self.stackedternplotdict
        self.echem10=echem10axesWidget(parent=self.parent, ellabels=d['ellabels'])
        self.echem10.plot(d, cb=True)
        
        #scatter_10axes(d['comps'], d['fom'], self.echem10.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
        self.echem10.exec_()
        
    def stackedtern30window(self):
        d=self.stackedternplotdict
        self.echem30=echem30axesWidget(parent=None, ellabels=d['ellabels'])
        self.echem30.plot(d, cb=True)

        #scatter_30axes(d['comps'], d['fom'], self.echem30.stpl, s=18, edgecolors='none', cmap=d['cmap'], norm=d['norm'])
        #self.echem30.show()
        self.echem30.exec_()

    def stackedtern20window(self):
        d=self.stackedternplotdict
        self.echem20=echem20axesWidget(parent=None, ellabels=d['ellabels'])
        self.echem20.plot(d, cb=True)
        self.echem20.exec_()

    def tern4window(self):
        d=self.stackedternplotdict
        self.echem4=echem4axesWidget(parent=None, ellabels=d['ellabels'])
        self.echem4.plot(d, cb=True)
        self.echem4.exec_()

    def binlineswindow(self):
        d=self.stackedternplotdict
        self.echembin=echembinWidget(parent=None, ellabels=d['ellabels'])
        self.echembin.plot(d, cb=True)
        self.echembin.exec_()

    def plotselect(self):
        overlaybool=self.overlayselectCheckBox.isChecked()
        if not overlaybool:
            self.plotw_select.axes.cla()
        d=self.techniquedictlist[self.selectind]
        
        xk=str(self.xplotchoiceComboBox.currentText())
        yk=str(self.yplotchoiceComboBox.currentText())
        
        xshift=0.
        xmult=1.
        yshift=0.
        ymult=1.
        if '-E0' in xk:
            xshift=-1.*self.E0SpinBox.value()
            xk=xk.replace('-E0', '')
        if '*Is' in xk:
            xmult=self.IsSpinBox.value()
            xk=xk.replace('*Is', '')
        if '-E0' in yk:
            yshift=-1.*self.E0SpinBox.value()
            yk=yk.replace('-E0', '')
        if '*Is' in yk:
            ymult=self.IsSpinBox.value()
            yk=yk.replace('*Is', '')
            
        if not xk in d.keys():
            print 'cannot plot the selected x-y graph because %s not found' %xk
            return
        if not yk in d.keys():
            print 'cannot plot the selected x-y graph because %s not found' %yk
            return
        x=d[xk]*xmult+xshift
        y=d[yk]*ymult+yshift
        lab=''.join(['%s%d' %(el, c*100.) for el, c in zip(d['elements'], d['compositions'])])+'\n'
        if 'FOM' in d.keys():
            lab+='%d,%.2e' %(d['Sample'], d['FOM'])
        else:
            lab+='%d' %d['Sample']
        self.plotw_select.axes.plot(x, y, '.-', label=lab)

        autotickformat(self.plotw_select.axes, x=0, y=1)

        if (not self.plotillumkey is None) and self.plotillumkey in d.keys() and not overlaybool:
            illuminds=numpy.where(d[self.plotillumkey])[0]
            self.plotw_select.axes.plot(x[illuminds], y[illuminds], 'y.')
        self.plotw_select.axes.set_xlabel(xk)
        self.plotw_select.axes.set_ylabel(yk)
        legtext=unicode(self.legendselectLineEdit.text())
        if len(legtext)>0:
            legloc=myeval(legtext)
            if isinstance(legloc, int) and legloc>=0:
                self.plotw_select.axes.legend(loc=legloc)
        self.plotw_select.fig.canvas.draw()
        t=d['mtime']-2082844800.
        print '^^^^^^^^', t
        if not isinstance(t, str):
            try:
                t=time.ctime(t)
            except:
                t='error'
        print t
        self.daqtimeLineEdit.setText(t)

    def plateclickprocess(self, coords_button):
        if len(self.techniquedictlist)==0:
            return
        critdist=3.
        xc, yc, button=coords_button
        x=getarrfromkey(self.techniquedictlist, 'x')
        y=getarrfromkey(self.techniquedictlist, 'y')
        dist=((x-xc)**2+(y-yc)**2)**.5
        if min(dist)<critdist:
            self.selectind=numpy.argmin(dist)
            self.plotselect()
        if button==3:
            self.addtoselectsamples([self.techniquedictlist[self.selectind]['Sample']])
    def selectbelow(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']<vmin:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def selectbetween(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']>=vmin and d['FOM']<vmax:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def selectabove(self):
        try:
            vmin, vmax=(self.vmin, self.vmax)
        except:
            print 'NEED TO PERFORM A PLOT TO DEFINE THE MIN,MAX RANGE BEFORE SELECTING SAMPLES'
        idlist=[]
        for d in self.techniquedictlist:
            if d['FOM']>=vmax:
                idlist+=[d['Sample']]
        if len(idlist)>0:
            self.addtoselectsamples(idlist)
            
    def addtoselectsamples(self, idlist):
        instr=str(self.selectsamplesLineEdit.text()).strip().split(',')
        instr+=[`n` for n in idlist if len(`n`)>0]
        s=','.join(instr).strip().strip(',').strip()
        self.selectsamplesLineEdit.setText(s)
        
    def writesamplelist(self, p=None, explab='selectsamples'):
        self.statusLineEdit.setText('writing file')
        idstr=str(self.selectsamplesLineEdit.text()).split(',')
        try:
            ids=[int(myeval(s.strip())) for s in idstr]
        except:
            print 'data conversion problem for this list of strings:', idstr
            return
        if len(ids)==0:
            print 'no data to save'
            return
        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt', xpath=self.kexperiments)
        elif os.path.isdir(p):
            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
            print p
        if not p:
            print 'save aborted'
            return
        ids=list(set(ids))
        ids.sort()
        savestr='\n'.join([`n` for n in ids])
        
        f=open(p, mode='w')
        f.write(savestr)
        f.close()
        
        self.statusLineEdit.setText('idle')
        
    def writefile(self, p=None, explab=None, savedlist=False):
        self.statusLineEdit.setText('writing file')
        if len(self.techniquedictlist)==0:
            print 'no data to save'
            return
        if explab is None:
            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText())))
        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet string', filename=os.path.split(self.folderpath)[1]+'_'+explab+'.txt', xpath=self.kexperiments)
        elif os.path.isdir(p):
            p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
            print p
        if not p:
            print 'save aborted'
            return
            
        labels=['Sample', 'x(mm)', 'y(mm)']
        labels+=self.techniquedictlist[0]['elements']
        labels+=[explab]
        kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), ('FOM', '%.6e')]
        arr=[]
        for d in self.techniquedictlist:
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
            pickle.dump(self.techniquedictlist, f)
            f.close()
        
        self.statusLineEdit.setText('idle')

    def writefileauto(self, p=None, explab=None, savedlist=False):
        self.statusLineEdit.setText('writing file')
        if len(self.techniquedictlist)==0:
            print 'no data to save'
            return
        if explab is None:
            explab=''.join((str(self.expmntLineEdit.text()), str(self.calcoptionComboBox.currentText())))
        
        #try to get plate id from folder name; if successful (finds a string of digits) and dbdatasource=2, create folder in K: experiments; works on *nix and Windows, untested on OSX
        idfromfolder=os.path.split(self.folderpath)[1].rsplit('_',1)[1].split(' ',1)[0]
        exptypes=('eche', 'ecqe')
        if idfromfolder.isdigit():
            if self.dbdatasource is 2:
                for exp in exptypes:
                    if exp in self.folderpath:
                        fompath=os.path.join(self.kexperiments, exp, idfromfolder)
                        try:
                            os.mkdir(fompath)
                        except:
                            pass
                        p=fompath

        p=os.path.join(p, os.path.split(self.folderpath)[1]+'_'+explab+'.txt')
        if not p:
            print 'save aborted'
            return
        labels=['Sample', 'x(mm)', 'y(mm)']
        labels+=self.techniquedictlist[0]['elements']
        labels+=[explab]
        kv_fmt=[('Sample', '%d'), ('x', '%.2f'), ('y', '%.2f'), ('compositions', '%.4f'), ('FOM', '%.6e')]
        arr=[]
        for d in self.techniquedictlist:
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
            pickle.dump(self.techniquedictlist, f)
            f.close()
        
        self.statusLineEdit.setText('idle')

class messageDialog(QDialog):
    def __init__(self, parent=None, title=''):
        super(messageDialog, self).__init__(parent)
        self.setWindowTitle(title)
        mainlayout=QGridLayout()
  
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
        QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)
        mainlayout.addWidget(self.buttonBox, 0, 0)
    
        QObject.connect(self.buttonBox,SIGNAL("accepted()"),self.ExitRoutine)
    def ExitRoutine(self):
        return
        
class plotwidget(FigureCanvas):
    def __init__(self, parent, width=12, height=6, dpi=72, projection3d=False):

        #plotdata can be 2d array for image plot or list of 2 1d arrays for x-y plot or 2d array for image plot or list of lists of 2 1D arrays
        
        self.fig=Figure(figsize=(width, height), dpi=dpi)
        if projection3d:
            self.axes=self.fig.add_subplot(111, navigate=True, projection='3d')
        else:
            self.axes=self.fig.add_subplot(111, navigate=True)
        
        self.axes.hold(True)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        #self.parent=parent
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #NavigationToolbar(self, parent)
        NavigationToolbar(self, self)
        
        self.mpl_connect('button_press_event', self.myclick)
        self.clicklist=[]
    
    def myclick(self, event):
        if not (event.xdata is None or event.ydata is None):
            arrayxy=[event.xdata, event.ydata]
            print 'clicked on image: array indeces ', arrayxy, ' using button', event.button
            self.clicklist+=[arrayxy]
            self.emit(SIGNAL("genericclickonplot"), [event.xdata, event.ydata, event.button])


