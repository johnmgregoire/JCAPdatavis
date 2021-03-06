import time, csv
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


sys.path.append(os.path.join(PyCodePath,'ternaryplot'))
from myternaryutility import TernaryPlot
from myquaternaryutility import QuaternaryPlot
from quaternary_FOM_stackedtern2 import *
from quaternary_FOM_stackedtern5 import *
from quaternary_FOM_stackedtern20 import *
from quaternary_FOM_stackedtern30 import *


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

class MainMenu(QMainWindow):
    def __init__(self, previousmm, execute=True, ellabels=['A', 'B', 'C', 'D'], **kwargs):#, TreeWidg):
        super(MainMenu, self).__init__(None)
        #self.setupUi(self)
        self.setWindowTitle('Quaternay composition slices and FOM visualization')
        
        numslices=userinputcaller(self, inputs=[('Number of comp slices (5,10,20,30)', int, '30')], title='Choose visualization of composition space',  cancelallowed=False)[0]


        echem_all=echemmultiaxesWidget(self, ellabels=ellabels, numslices=numslices)
        echem_select=echemmultiaxesWidget(self, ellabels=ellabels, numslices=numslices)
        
        echem_select.show()
        echem_all.show()
        
        self.echem=quatsliceDialog(self, echem_select, echem_all, ellabels=ellabels, **kwargs)
        self.echem.show()
        #if execute:
            #self.echem.exec_()


class echemmultiaxesWidget(QDialog):
    def __init__(self, parent=None, ellabels=['A', 'B', 'C', 'D'], buttons=True, numslices=30):
        super(echemmultiaxesWidget, self).__init__(parent)
        
        if numslices==5:
            self.maketernaxes=make10ternaxes
            self.scatter_axes=scatter_10axes
        elif numslices==10:
            self.maketernaxes=make10ternaxes
            self.scatter_axes=scatter_10axes
        elif numslices==20:
            self.maketernaxes=make20ternaxes
            self.scatter_axes=scatter_20axes
        else:
            self.maketernaxes=make30ternaxes
            self.scatter_axes=scatter_30axes
        mainlayout=QVBoxLayout()
        self.ellabels=ellabels
        self.plotw=plotwidget(self)
        self.plotw.fig.clf()
        self.axl, self.stpl=self.maketernaxes(fig=self.plotw.fig, ellabels=self.ellabels)
        
        mainlayout.addWidget(self.plotw)
        if buttons:
            self.buttonBox = QDialogButtonBox(self)
            self.buttonBox.setGeometry(QRect(520, 195, 160, 26))
            self.buttonBox.setOrientation(Qt.Horizontal)
            self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)
            QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
            mainlayout.addWidget(self.buttonBox)
        QObject.connect(self.plotw, SIGNAL("genericclickonplot"), self.clickprocess)
        self.setLayout(mainlayout)
        self.terncalc=TernaryPlot(111)
    
    def plot(self, d, cb=True):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        self.scatter_axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])
        
    def clearandplot(self, d, cb=True, ellabels=None):
        if 'fomlabel' in d.keys():
            cblabel=d['fomlabel']
        else:
            cblabel=''
        self.plotw.fig.clf()
        if not ellabels is None:
            self.ellabels=ellabels
        self.axl, self.stpl=self.maketernaxes(fig=self.plotw.fig, ellabels=self.ellabels)
        self.scatter_axes(d['comps'], d['fom'], self.stpl, s=18, edgecolors='none', cb=cb, cblabel=cblabel, cmap=d['cmap'], norm=d['norm'])
        self.plotw.fig.canvas.draw()
    
    def clickprocess(self, coords_button):
        xc, yc, button=coords_button
        clickcomplist=self.terncalc.toComp(numpy.array([[xc, yc]]))
        print 'clicked ternary composition is ', clickcomplist[0]
            
class quatsliceDialog(QDialog):
    def __init__(self, parent, echem30_select, echem30_all, title='', folderpath=None, ellabels=['A', 'B', 'C', 'D']):
        super(quatsliceDialog, self).__init__(parent)
        self.parent=parent
        
        self.echem30_select=echem30_select
        self.echem30_all=echem30_all
        
        self.ellabels=ellabels
        self.dataclass=fomdatapreset()

        self.plotw_quat=plotwidget(self, projection3d=True)
        
        self.plotw_tern=plotwidget(self)

        
        axrect=[0.85, 0.1, 0.04, 0.8]

        
        self.plotw_tern.fig.subplots_adjust(left=0.1, right=axrect[0]-.08)
        self.cbax_tern=self.plotw_tern.fig.add_axes(axrect)
        
        QObject.connect(self.plotw_tern, SIGNAL("genericclickonplot"), self.ternclickprocess)

        
        self.plotw_quat.fig.subplots_adjust(left=0, right=axrect[0]-.08)
        self.cbax_quat=self.plotw_quat.fig.add_axes(axrect)




        
        ternskipComboBoxLabel=QLabel()
        ternskipComboBoxLabel.setText('Exclude for ternary:')
        self.ternskipComboBox=QComboBox()
        for i, l in enumerate(['A', 'B', 'C', 'D']):
            self.ternskipComboBox.insertItem(i, l)
        self.ternskipComboBox.setCurrentIndex(i)
        ternskiplayout=QHBoxLayout()
        ternskiplayout.addWidget(ternskipComboBoxLabel)
        ternskiplayout.addWidget(self.ternskipComboBox)
        
        self.compcutComboBox=QComboBox()
        for i, nam in enumerate(['1-D (pseudobinary)', '2-D (pseudoternnary)']):
            self.compcutComboBox.insertItem(i, nam)
        self.compcutComboBox.setCurrentIndex(0)
        
        self.systemsComboBox=QComboBox()
        self.systemsinds=[-1, 0]
        self.systemsComboBox.insertItem(999, 'select files')
        self.systemsComboBox.insertItem(999, 'update style')
        for ind, nam in self.dataclass.systemoptions:
            self.systemsComboBox.insertItem(999, nam)
            self.systemsinds+=[ind]

        self.systemsComboBox.setCurrentIndex(0)
        
        sl=['0.', '0.', '1.', '0.', '0.', '0.']
        self.complineeditlist=[]
        for i in range(3):
            self.complineeditlist+=[QLineEdit()]
            self.complineeditlist[-1].setText(', '.join(sl[2-i:2-i+4]))
        compLabel=QLabel()
        compLabel.setText('Composition points')
        
        folderButton=QPushButton()
        folderButton.setText("select\nfolder")
        QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfolder)
        
        plotButton=QPushButton()
        plotButton.setText("update\nfigures")
        QObject.connect(plotButton, SIGNAL("pressed()"), self.calcandplot)
        
        saveButton=QPushButton()
        saveButton.setText("Save figs\n+ Samples")
        QObject.connect(saveButton, SIGNAL("pressed()"), self.save)
        
        templab=QLabel()
        templab.setText('Crit Comp. Dist')
        self.critdistSpinBox=QDoubleSpinBox()
        self.critdistSpinBox.setDecimals(3)
        critdistlayout=QHBoxLayout()
        critdistlayout.addWidget(templab)
        critdistlayout.addWidget(self.critdistSpinBox)
        
        self.compboundCheckBox=QCheckBox()
        self.compboundCheckBox.setText('restrict composition\nselection boundaries')
        
        self.invertCheckBox=QCheckBox()
        self.invertCheckBox.setText('invert selection')
        
        self.revcmapCheckBox=QCheckBox()
        self.revcmapCheckBox.setText('reverse cmap?')
        
        templab=QLabel()
        templab.setText('min,max colorbar')
        self.vminmaxLineEdit=QLineEdit()
        vminmaxlayout=QVBoxLayout()
        vminmaxlayout.addWidget(templab)
        vminmaxlayout.addWidget(self.vminmaxLineEdit)


        templab=QLabel()
        templab.setText('azim,elev tetr.')
        self.azimelevLineEdit=QLineEdit()
        azimelevlayout=QVBoxLayout()
        azimelevlayout.addWidget(templab)
        azimelevlayout.addWidget(self.azimelevLineEdit)
        self.azimelevLineEdit.setText('-159,30')
        
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
        
        templab=QLabel()
        templab.setText('FOM shift:')
        self.fomshiftSpinBox=QDoubleSpinBox()
        self.fomshiftSpinBox.setDecimals(3)
        fomshiftlayout=QHBoxLayout()
        fomshiftlayout.addWidget(templab)
        fomshiftlayout.addWidget(self.fomshiftSpinBox)
        
        templab=QLabel()
        templab.setText('FOM scaling:')
        self.fomscaleSpinBox=QDoubleSpinBox()
        self.fomscaleSpinBox.setMaximum(1000.)
        self.fomscaleSpinBox.setMinimum(-1000.)
        self.fomscaleSpinBox.setValue(1.)
        fomscalelayout=QHBoxLayout()
        fomscalelayout.addWidget(templab)
        fomscalelayout.addWidget(self.fomscaleSpinBox)
        
        

        mainlayout=QGridLayout()
        ctrllayout=QGridLayout()
    
        
        ctrllayout.addWidget(plotButton, 0, 0)
        ctrllayout.addWidget(self.compcutComboBox, 0, 1)
        ctrllayout.addWidget(saveButton, 0, 2)
        ctrllayout.addWidget(self.systemsComboBox, 0, 3)
        
        ctrllayout.addWidget(compLabel, 1, 0)
        ctrllayout.addWidget(self.complineeditlist[0], 1, 1)
        ctrllayout.addWidget(self.complineeditlist[1], 1, 2)
        ctrllayout.addWidget(self.complineeditlist[2], 1, 3)
        
        ctrllayout.addWidget(self.compboundCheckBox, 2, 0)
        ctrllayout.addWidget(self.invertCheckBox, 2, 1,)
        ctrllayout.addLayout(critdistlayout, 2, 2, 1, 2)
        
        ctrllayout.addWidget(self.revcmapCheckBox, 3, 0)
        ctrllayout.addLayout(vminmaxlayout, 3, 1)
        ctrllayout.addLayout(outrangecollayout, 3, 2, 1, 2)
        
        
        ctrllayout.addLayout(ternskiplayout, 4, 0)
#        ctrllayout.addLayout(fomshiftlayout, 4, 1)
#        ctrllayout.addLayout(fomscalelayout, 4, 2)
        ctrllayout.addLayout(azimelevlayout, 4, 1, 1, 2)
        
        mainlayout.addLayout(ctrllayout, 0, 0, 2, 1)
        mainlayout.addWidget(self.plotw_quat, 3, 0)
        mainlayout.addWidget(self.plotw_tern, 4, 0)
#        mainlayout.addWidget(self.plotw_30select, 0, 1, 2, 8)
#        mainlayout.addWidget(self.plotw_30all, 2, 1, 2, 8)
        
        self.setLayout(mainlayout)
        
        self.folderpath=folderpath
        

        self.ternskipComboBox.clear()
        for i, l in enumerate(self.ellabels):
            self.ternskipComboBox.insertItem(i, l)
        self.ternskipComboBox.setCurrentIndex(3)
        self.selectsystem=None
        self.quatcalc=QuaternaryPlot(111, ellabels=self.ellabels)
        self.resize(600, 850)
    
        
    def selectfolder(self, folder=None):

        if folder is None:
            self.folderpath=mygetdir(self, markstr='for saving')
        else:
            self.folderpath=folder
        
    def calcandplot(self):
        print '0'
        i=self.systemsinds[self.systemsComboBox.currentIndex()]
        if self.selectsystem is None or i==-1 or (i!=0 and i!=self.selectsystem):
            self.selectsystem=i
            self.dataclass.readdata(self.selectsystem, qparent=self)
            
            self.comps=self.dataclass.compsall
            self.fom=self.dataclass.fomall
            self.smp=self.dataclass.smpsall
            self.code=self.dataclass.codeall
#            self.codeorig=self.dataclass.codeorig
#            self.smpsorig=self.dataclass.smpsorig

            self.ellabels=self.dataclass.ellabels
            self.vminmaxLineEdit.setText(`self.dataclass.vmin`+','+`self.dataclass.vmax`)
            for le, v in zip([self.belowrangecolLineEdit, self.aboverangecolLineEdit], [self.dataclass.belowrangecolstr, self.dataclass.aboverangecolstr]):
                le.setText(`v`)
        
            i0=self.ternskipComboBox.currentIndex()
            self.ternskipComboBox.clear()
            for i, l in enumerate(self.ellabels):
                self.ternskipComboBox.insertItem(i, l)
            self.ternskipComboBox.setCurrentIndex(i0)
            
        self.calctype=self.compcutComboBox.currentIndex()
        critdist=self.critdistSpinBox.value()
        
        print '1'
        self.compverts=[]
        for i in range(2+self.calctype):
            sl=str(self.complineeditlist[i].text()).split(',')
            c=[myeval(s.strip()) for s in sl]
            c=c[:4]
            c+=[0.]*(4-len(c))
            c=numpy.float64(c)
            c/=c.sum()
            self.compverts+=[c]
        
        betweenbool=self.compboundCheckBox.isChecked()
        invertbool=self.invertCheckBox.isChecked()
        
        if self.calctype==0:
            self.selectinds, distfromlin, self.lineparameter=self.quatcalc.filterbydistancefromline(self.comps, self.compverts[0], self.compverts[1], critdist, betweenpoints=betweenbool, invlogic=invertbool, returnall=True)
            self.lineparameter=self.lineparameter[self.selectinds]
        elif self.calctype==1:
            self.selectinds, distfromplane, self.xyparr, self.xyp_verts,intriangle=self.quatcalc.filterbydistancefromplane(self.comps, self.compverts[0], self.compverts[1], self.compverts[2], critdist, withintriangle=betweenbool, invlogic=invertbool, returnall=True)
            self.xyparr=self.xyparr[self.selectinds]
        
        self.selectcomps=self.comps[self.selectinds]
        self.plot()
        

    def plot(self):
        s=25
        self.plotw_tern.axes.cla()
        self.plotw_quat.axes.cla()
        self.cbax_quat.cla()
        self.cbax_tern.cla()
        fom=self.fom
    
        azim=-159.
        elev=30.
        vstr=str(self.azimelevLineEdit.text()).strip()

        if ',' in vstr:
            a, b, c=vstr.partition(',')
            try:
                a=myeval(a.strip())
                c=myeval(c.strip())
                self.vmin=a
                self.vmax=c
            except:
                pass
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
        print '4'
        norm=colors.Normalize(vmin=self.vmin, vmax=self.vmax, clip=clip)
        print 'fom min, max, mean, std:', fom.min(), fom.max(), fom.mean(), fom.std()
        
        comps=self.comps
        #comment out this skipoutofrange becuase it could mess up the indexing
#        print 'skipoutofrange', skipoutofrange
#        print len(fom)
#        if skipoutofrange[0]:
#            inds=numpy.where(fom>=self.vmin)
#            fom=fom[inds]
#            comps=comps[inds]
#        print len(fom)
#        if skipoutofrange[1]:
#            inds=numpy.where(fom<=self.vmax)
#            fom=fom[inds]
#            comps=comps[inds]
#        print len(fom)
        
        
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

        
        i=self.ternskipComboBox.currentIndex()
        inds=[j for j in range(4) if j!=i][:3]
        terncomps=numpy.array([c[inds]/c[inds].sum() for c in comps])
        reordercomps=comps[:, inds+[i]]
        reorderlabels=[self.ellabels[j] for j in inds+[i]]
        
        fomselect=fom[self.selectinds]
        compsselect=comps[self.selectinds]
        reordercompsselect=reordercomps[self.selectinds]
        
        
        
        fomlabel=self.dataclass.fomlabel
        self.stackedternplotdict=dict([('comps', reordercomps), ('fom', fom), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel), ('extend', extend)])
        self.echem30_all.clearandplot(self.stackedternplotdict, cb=True, ellabels=reorderlabels)
        
        print len(fomselect), ' samples selected'
        
        if len(fomselect)>0:
            
            self.stackedternplotdictselect=dict([('comps', reordercompsselect), ('fom', fomselect), ('cmap', cmap), ('norm', norm), ('ellabels', reorderlabels), ('fomlabel', fomlabel), ('extend', extend)])
            self.echem30_select.clearandplot(self.stackedternplotdictselect, cb=True, ellabels=reorderlabels)
            
            
            quat=QuaternaryPlot(self.plotw_quat.axes, ellabels=self.ellabels, offset=0)
            quat.label()
            quat.scatter(compsselect, c=fomselect, s=s, cmap=cmap, norm=norm,  edgecolor='none')#vmin=self.vmin, vmax=self.vmax,
            cb=self.plotw_quat.fig.colorbar(quat.mappable, cax=self.cbax_quat, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
            cb.set_label(fomlabel, fontsize=18)
            quat.set_projection(azim=azim, elev=elev)
            
            if self.calctype==0:
                quat.line(self.compverts[0], self.compverts[1])
                self.quatcalc.plotfomalonglineparameter(self.plotw_tern.axes, self.lineparameter, fomselect, compend1=self.compverts[0], compend2=self.compverts[1], lineparticks=numpy.linspace(0, 1, 4), ls='none', marker='.')
            elif self.calctype==1:
                self.quatcalc.plotfominselectedplane(self.plotw_tern.axes, self.xyparr, fomselect, xyp_verts=self.xyp_verts, vertcomps_labels=[self.compverts[0], self.compverts[1], self.compverts[2]], s=20, edgecolor='none', cmap=cmap, norm=norm)
                quat.line(self.compverts[0], self.compverts[1])
                quat.line(self.compverts[0], self.compverts[2])
                quat.line(self.compverts[2], self.compverts[1])

            
            cb=self.plotw_tern.fig.colorbar(quat.mappable, cax=self.cbax_tern, extend=extend, format=autocolorbarformat((fom.min(), fom.max())))
            cb.set_label(fomlabel, fontsize=18)

        self.plotw_quat.axes.mouse_init()
        self.plotw_quat.axes.set_axis_off()
        self.plotw_tern.fig.canvas.draw()
        self.plotw_quat.fig.canvas.draw()

        
    def ternclickprocess(self, coords_button):
        xc, yc, button=coords_button
        if self.calctype==0:
            clickindsel=numpy.argmin((self.lineparameter-xc)**2)
        elif self.calctype==1:
            clickindsel=numpy.argmin([(x-xc)**2+(y-yc)**2 for x, y in self.xyparr])
        
        cmp=self.selectcomps[clickindsel]
        
        clickind=numpy.argmin([((cmp-c)**2).sum() for c in self.comps])
        s=self.smp[clickind]
        print 'clicked composition is ', cmp,  '  sample is ', s
        
    def save(self):
        self.selectfolder(None)

        lab=str(self.systemsComboBox.currentText())
        lab+='_'+self.dataclass.expstr+'_'
        
        if self.calctype==0:
            lab+='1Dcut_'
        elif self.calctype==1:
            lab+='2Dcut_'
        
        pngname=lambda sn:os.path.join(self.folderpath, lab+'_'+sn+'.png')
        epsname=lambda sn:os.path.join(self.folderpath, lab+'_'+sn+'.eps')
    
        for fig, saven in zip([self.plotw_quat.fig, self.plotw_tern.fig, self.echem30_select.plotw.fig, self.echem30_all.plotw.fig], ['tetr', 'projection', 'stackedselect', 'stackedall']):
            fig.savefig(pngname(saven))
            fig.savefig(epsname(saven))
        
        s='\n'.join([`i` for i in self.smp[self.selectinds]])
        
        sp=os.path.join(self.folderpath, lab+'.txt')
        f=open(sp, mode='w')
        f.write(s)
        f.close()

        
        
        
        
        
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


class fomdatapreset():
    def __init__(self):
        self.systemoptions=[\
            (1, '201304NiFeCoCeVCP10'), \
            (2, '201304NiFeCoCeI350mV'), \
            (3, '201304NiFeCoCeI400mV'), \
            (4, '201304NiFeCoCeVCV3'), \
            (5, '201304NiFeCoCeVCV10'), \
            ]
    def readdata(self, SYSTEM=1, qparent=None):
        selectfilesbool=False
        if SYSTEM==1:
            ellabels=['Ni', 'Fe', 'Co', 'Ce']
            os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results')
            rootstr='201304'
            expstr='CP1Efin'
            fomlabel='V for 10 mA/cm$^2$ (V vs H$_2$0/O$_2$)'
            fomshift=-(.187-.045)
            fommult=1.
            vmin=.33
            vmax=.43
            cmap=cm.jet_r
            aboverangecolstr='k'
            belowrangecolstr='.3'
            savefolder=os.path.join(os.getcwd(), expstr)
            binarylegloc=1
            elkeys=['Ni', 'Fe', 'Co', 'Ce'] 
        elif SYSTEM==2:
            ellabels=['Ni', 'Fe', 'Co', 'Ce']
            os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results')
            rootstr='_I350mVLinSub.txt'
            expstr='I350mVLinSub'
            fomlabel='I at 350mV vs E$_{OER}$ (mA/cm$^2$)'
            fomshift=0.
            fommult=100000.
            vmin=1
            vmax=10
            cmap=cm.jet
            aboverangecolstr='pink'
            belowrangecolstr='k'
            savefolder=os.path.join(os.getcwd(), expstr)
            binarylegloc=1
            elkeys=['Ni', 'Fe', 'Co', 'Ce']
        elif SYSTEM==3:
            ellabels=['Ni', 'Fe', 'Co', 'Ce']
            os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results')
            rootstr='_I400mVLinSub.txt'
            expstr='I400mVLinSub'
            fomlabel='I at 400mV vs E$_{OER}$ (mA/cm$^2$)'
            fomshift=0.
            fommult=100000.
            vmin=1
            vmax=42
            cmap=cm.jet
            aboverangecolstr='pink'
            belowrangecolstr='k'
            savefolder=os.path.join(os.getcwd(), expstr)
            binarylegloc=1
            elkeys=['Ni', 'Fe', 'Co', 'Ce']

        elif SYSTEM==4:
            ellabels=['Ni', 'Fe', 'Co', 'Ce']
            os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results')
            rootstr='_V_IthreshCVLinSub_30.txt'
            expstr='V_IthreshCVLinSub_30'
            fomlabel='E for 3mA/cm$^2$ (mV vs E$_{OER}$)'
            fomshift=0.
            fommult=1000.
            vmin=280
            vmax=400
            cmap=cm.jet_r
            aboverangecolstr='k'
            belowrangecolstr='pink'
            savefolder=os.path.join(os.getcwd(), expstr)
            binarylegloc=1
            elkeys=['Ni', 'Fe', 'Co', 'Ce']

        elif SYSTEM==5:
            ellabels=['Ni', 'Fe', 'Co', 'Ce']
            os.chdir('C:/Users/Public/Documents/EchemDropRawData/NiFeCoCe/results')
            rootstr='_V_IthreshCVLinSub_100.txt'
            expstr='V_IthreshCVLinSub_100'
            fomlabel='E for 10mA/cm$^2$ (mV vs E$_{OER}$)'
            fomshift=0.
            fommult=1000.
            vmin=350
            vmax=440
            cmap=cm.jet_r
            aboverangecolstr='k'
            belowrangecolstr='pink'
            savefolder=os.path.join(os.getcwd(), expstr)
            binarylegloc=1
            elkeys=['Ni', 'Fe', 'Co', 'Ce']
        
        else:
            dpl=mygetopenfiles(parent=qparent, markstr='FOM .txt files', filename='.txt')
            f=open(dpl[0], mode='r')
            l=f.readline()
            f.close()
            ks=l.split('\t')
            ks=[k.strip() for k in ks]
            
            elkeys=ks[3:7]
            expstr=ks[7]
            ellabels=elkeys
            
            fomshift=0.
            fommult=1.
            selectfilesbool=True
        
        
        #ellabels=['A', 'B', 'C', 'D']
        
        if not selectfilesbool:
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
            if dp=='':
                dropdl+=[None]
                continue
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


        figquatall=[]
        compsall=[]
        fomall=[]
        plateindall=[]
        codeall=[]
        smpsall=[]
        for count, dropd in enumerate(dropdl):
            if dropd is None:
                continue
            print dropd.keys()
            #dropinds=numpy.arange(len(dropd['Sample']))
            try:
                dropd['compositions']=numpy.array([dropd[elkey] for elkey in elkeys]).T
            except:
                dropd['compositions']=numpy.array([dropd[elkey] for elkey in ['A', 'B', 'C', 'D']]).T
            
            addcodetoplatemapgen1dlist(dlist=None, dropd=dropd)
            
            dropinds=numpy.argsort(dropd['Sample'])
            dropinds=dropinds[numpy.logical_not(numpy.isnan(dropd[expstr][dropinds]))]
            x=dropd['x(mm)'][dropinds]
            y=dropd['y(mm)'][dropinds]
            sample=dropd['Sample'][dropinds]
            fom=(dropd[expstr][dropinds]+fomshift)*fommult
            
            comp=dropd['compositions'][dropinds]
            code=dropd['code'][dropinds]
            
            comp=numpy.array([a/a.sum() for a in comp])
            smpsall+=list(sample)
            compsall+=list(comp)
            fomall+=list(fom)
            plateindall+=[count]*len(fom)
            codeall+=list(code)

        smpsall=numpy.array(smpsall)

        compsall=numpy.array(compsall)
        fomall=numpy.array(fomall)
        plateindall=numpy.array(plateindall)
        codeall=numpy.array(codeall)
        

        
        self.smpsorig=smpsall
        self.codeorig=codeall
        #these codes are not accurate - they are "made up" from addcodetoplatemapgen1dlist
        code0inds=numpy.where(codeall==0)
        code02inds=numpy.where(codeall!=1)
        code2inds=numpy.where(codeall==2)

        compsall=compsall[code0inds]
        fomall=fomall[code0inds]
        smpsall=smpsall[code0inds]
        codeall=codeall[code0inds]
        
        self.compsall=compsall
        self.fomall=fomall
        self.smpsall=smpsall
        self.codeall=codeall
        self.ellabels=ellabels
        self.expstr=expstr
        if selectfilesbool:
            self.vmin=fomall.min()
            self.vmax=fomall.max()
            self.aboverangecolstr='pink'
            self.belowrangecolstr='k'
            self.fomlabel=expstr
        else:
            self.vmin=vmin
            self.vmax=vmax
            self.aboverangecolstr=aboverangecolstr
            self.belowrangecolstr=belowrangecolstr
            self.fomlabel=fomlabel
        


def start(previousmm=None):
    mainapp=QApplication(sys.argv)

    form=MainMenu(previousmm)
    form.show()
    form.setFocus()
    global PARENT
    PARENT=form
    mainapp.exec_()
    return form
mm=None
mm=start()
