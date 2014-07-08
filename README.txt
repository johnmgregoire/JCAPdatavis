John M Gregoire 24 Mar 2013, 

All code written by John Gregoire. Code is a work in progress for visualizing JCAP-HTE data.

 

Dan Guevarra  30 Apr 2014,

Visualization tool is launched via "eche_plate_visualize.py" and requires additional repository in the same root directory as JCAPdatavis:

	PythonCompositionPlots
	https://github.com/johnmgregoire/PythonCompositionPlots


The default Anaconda (Python 2.7) install contains all but two module dependencies:

	MySQL-python
	https://pypi.python.org/pypi/MySQL-python

	PyQt4
	https://pypi.python.org/pypi/PyQt4

**Anaconda's default Qt4 backend must be changed from 'PySide' to 'PyQt4' in matplotlibrc.
http://matplotlib.org/1.3.1/users/customizing.html

Linux, OSX, and Windows installers for Anaconda are available here:
	
	http://continuum.io/downloads

Great resource for unofficial windows binaries such as MySQL-python:

	http://www.lfd.uci.edu/~gohlke/pythonlibs/
