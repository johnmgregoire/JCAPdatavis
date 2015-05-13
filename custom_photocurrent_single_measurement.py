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

matplotlib.rcParams['backend.qt4'] = 'PyQt4'

def myexpformat_2digs(x, pos):
    return '%.2e' %x

ExpTickLabels=FuncFormatter(myexpformat_2digs)
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


class tempDialog(QDialog):
    def __init__(self, parent=None, title='', folderpath=None):
        super(tempDialog, self).__init__(parent)
        self.parent=parent
#        self.echem30=echem30axesWidget()
#        self.echem30.show()
        self.plotillumkey=None


        self.techniquedictlist=[]


        self.plotw_0=plotwidget(self)
        self.plotw_1=plotwidget(self)
        self.plotw_2=plotwidget(self)
        self.plotw_3=plotwidget(self)

        self.plotw_0.fig.subplots_adjust(left=.2)
        self.plotw_1.fig.subplots_adjust(left=.2)
        self.plotw_2.fig.subplots_adjust(left=.2)
        self.plotw_3.fig.subplots_adjust(left=.2)


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
        

        folderButton=QPushButton()
        folderButton.setText("select\nfile")
        QObject.connect(folderButton, SIGNAL("pressed()"), self.selectfile)


        updateButton=QPushButton()
        updateButton.setText("update\ndata")
        QObject.connect(updateButton, SIGNAL("pressed()"), self.calcandplot)

        saveButton=QPushButton()
        saveButton.setText("save\nspreadhseet")
        QObject.connect(saveButton, SIGNAL("pressed()"), self.writeillumtxt)

        paramsButton=QPushButton()
        paramsButton.setText("edit params")
        QObject.connect(paramsButton, SIGNAL("pressed()"), self.getcalcparams)
        
        addButton=QPushButton()
        addButton.setText("add to\nfig 4")
        QObject.connect(addButton, SIGNAL("pressed()"), self.addplot)
        
        self.labelLineEdit=QLineEdit()
        self.overlayselectCheckBox=QCheckBox()
        self.overlayselectCheckBox.setText("overlay")
        
        savebuttonlayout=QHBoxLayout()
        savebuttonlayout.addWidget(folderButton)
        savebuttonlayout.addWidget(paramsButton)
        savebuttonlayout.addWidget(updateButton)
        savebuttonlayout.addWidget(saveButton)
        savebuttonlayout.addWidget(addButton)
        savebuttonlayout.addWidget(self.labelLineEdit)
        savebuttonlayout.addWidget(self.overlayselectCheckBox)



        mainlayout=QGridLayout()
        mainlayout.addLayout(savebuttonlayout, 0, 0, 1, 2)

        mainlayout.addWidget(self.plotw_0, 1, 0)
        mainlayout.addWidget(self.plotw_1, 1,1)
        mainlayout.addWidget(self.plotw_2, 2, 0)
        mainlayout.addWidget(self.plotw_3, 2, 1)



        self.setLayout(mainlayout)
        
        self.resize(1100, 850)
        self.selectfile()
        self.getcalcparams()
        self.calcandplot()

    def selectfile(self, plate_id=None, selectexids=None, folder=None):

        self.p=mygetopenfile(self, markstr='select CA photo .txt file')
        self.techdict=readechemtxt(self.p)

    def getcalcparams(self):
        i=2
        j=3
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
        i=2
        j=3
        tup=self.expmnt_calc_options[i][1][j]
        fcnnam=tup[0]
        self.calckeys=tup[1]

        ikey=self.CalcParams[4]
        tshift=self.CalcParams[5]
        if tshift!=0:
            newikey='IllumMod'
            self.techdict[newikey]=illumtimeshift(self.techdict, ikey, self.calckeys[3], tshift)
            ikey=newikey
            if self.CalcParams[7]!=0:
                self.techdict[ikey]*=-1
        elif self.CalcParams[7]!=0:
            newikey='IllumMod'
            self.techdict[newikey]=-1*self.techdict[ikey]
            ikey=newikey

        illkey=self.calckeys[1]+'_illdiff'
        err=calcdiff_ill_caller(self.techdict, ikey=ikey, thresh=self.CalcParams[6], ykeys=[self.calckeys[1]], xkeys=list(self.calckeys[2:]), illfracrange=(self.CalcParams[0], self.CalcParams[1]), darkfracrange=(self.CalcParams[2], self.CalcParams[3]))
        try:
            if err or len(self.techdict[illkey])==0:
                return 0
            self.plotillumkey='IllumBool'

            ncycs=self.CalcParams[8]
            fromend=self.CalcParams[9]
            if fromend:
                arr=self.techdict[illkey][::-1]
            else:
                arr=self.techdict[illkey]
            arr=arr[:ncycs]

            if 'min' in fcnnam:
                returnval=min(arr)
            elif 'max' in fcnnam:
                returnval=max(arr)
            else:
                returnval=numpy.mean(arr)
        except:
            print 'ERROR PHOTOCURRENT CALCULATION'
            return None
        return returnval


    def calcandplot(self, ext='.txt', dbupdate=False):

        fom=self.CalcFOM()
        if fom is None:
            return
        print 'FOM:', fom
        self.plotw_0.axes.cla()
        self.plotw_0.axes.plot(self.techdict['t(s)'], self.techdict['I(A)'],'b.-')
        self.plotw_0.axes.set_xlabel('t(s)')
        self.plotw_0.axes.set_ylabel('I(A)')
        autotickformat(self.plotw_0.axes, x=0, y=1)
        self.plotw_0.fig.canvas.draw()
        
        self.plotw_1.axes.cla()
        self.plotw_1.axes.plot(self.techdict['t(s)'], self.techdict['I(A)'],'b-')
        self.plotw_1.axes.plot(self.techdict['t(s)_dark'], self.techdict['I(A)_dark'],'g.')
        self.plotw_1.axes.plot(self.techdict['t(s)_ill'], self.techdict['I(A)_ill'],'k.')
        self.plotw_1.axes.set_xlabel('t(s)')
        self.plotw_1.axes.set_ylabel('I(A)')
        autotickformat(self.plotw_1.axes, x=0, y=1)
        self.plotw_1.fig.canvas.draw()
        
        self.plotw_2.axes.cla()
        self.plotw_2.axes.plot(self.techdict['t(s)_ill'], self.techdict['I(A)_illdiff'],'k.-')
        self.plotw_2.axes.set_xlabel('t(s)')
        self.plotw_2.axes.set_ylabel('Iphoto(A)')
        autotickformat(self.plotw_2.axes, x=0, y=1)
        self.plotw_2.fig.canvas.draw()
    
        
    def addplot(self):
        lab=str(self.labelLineEdit.text())
        if not self.overlayselectCheckBox.isChecked():
            self.plotw_3.axes.cla()
        self.plotw_3.axes.plot(self.techdict['t(s)_ill'], self.techdict['I(A)_illdiff'],'.-', label=lab)
        self.plotw_3.axes.set_xlabel('t(s)')
        self.plotw_3.axes.set_ylabel('Iphoto(A)')
        autotickformat(self.plotw_3.axes, x=0, y=1)
        self.plotw_3.axes.legend(loc=0).draggable()
        self.plotw_3.fig.canvas.draw()
    def writeillumtxt(self, p=None, explab=None, saved=False):

        if p is None:
            p=mygetsavefile(parent=self, markstr='save spreadsheet of dark and illum photocurrent', xpath=self.p)

        if not p:
            print 'save aborted'
            return

        labels=['t(s)_dark', 'I(A)_dark', 't(s)_ill', 'I(A)_ill', 'I(A)_illdiff']
        lines=['%column_headings='+'\t'.join(labels)]
        lines+=['\t'.join(tup) for tup in zip(*[['%.3e' %v for v in self.techdict[k]] for k in labels])]
        s='\n'.join(lines)
        
        f=open(p, mode='w')
        f.write(s)
        f.close()

        if saved:
            f=open(p[:-4]+'.pck', mode='w')
            pickle.dump(self.techdict, f)
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



if __name__ == "__main__":
    class MainMenu(QMainWindow):
        def __init__(self, previousmm, execute=True, **kwargs):#, TreeWidg):
            super(MainMenu, self).__init__(None)
            #self.setupUi(self)
            self.expui=tempDialog(self, title='Custom Photocurrent Calculator', **kwargs)
            #self.expui.importruns(pathlist=['20150422.145113.donex.zip'])
            #self.expui.importruns(pathlist=['uvis'])
            if execute:
                self.expui.exec_()                
    #os.chdir('//htejcap.caltech.edu/share/home/users/hte/demo_proto')
    mainapp=QApplication(sys.argv)
    form=MainMenu(None)
    form.show()
    form.setFocus()
    
    #form.expui.exec_()
    
    mainapp.exec_()
