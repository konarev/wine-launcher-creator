#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Wine Launcher Creator (c) 2011  Žarko Živanov

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

VERSION="1.0.6"

import sys
import glob
import os
import tempfile
import subprocess
import shlex
import shutil
import ConfigParser
import urllib

from PyQt4.QtGui import *
from PyQt4.QtCore import *

def check_output(*popenargs, **kwargs):
    """This function is copied from python 2.7.1 subprocess.py
       Copyright (c) 2003-2005 by Peter Astrand <astrand@lysator.liu.se>
       Licensed to PSF under a Contributor Agreement.
       See http://www.python.org/2.4/license for licensing details."""
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output

def bash(command, workdir=None):
    """Helper function to execute bash commands"""
    command = shlex.split(command.encode("utf-8"))
    #print "COMMAND:",command
    try:
        code = subprocess.call(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, cwd=workdir)
    except:
        code = 127
    #print "CODE:",code
    return code

def checkDependencies():
    """Helper function to check for imagemagick/icoutils"""
    missing = False
    missingText = ""
    #check icoutils
    if bash("wrestool --version") > 0:
        if missingText != "":
            missingText += "\n"
        missingText += "Missing dependencie: icoutils"
        missing = True
    if missing:
        dialog = QMessageBox(QMessageBox.Critical,"Missing dependencies",missingText)
        dialog.exec_()
    return not missing

class BrowseControl(QHBoxLayout):
    """Control containing label, edit field and button
       Used to browse for files and directories"""
    def __init__(self, label, browseTitle, toolTip, callback=None, extensions="", browseDirectory=False,
                 setStatus=None, showHidden=False, parent=None):
        super(BrowseControl, self).__init__(parent)

        #control's label
        self.label = QLabel(label+":")
        self.addWidget(self.label)
        #control's edit
        self.edit = QLineEdit()
        self.addWidget(self.edit,1)
        self.edit.setToolTip(toolTip)
        self.connect(self.edit, SIGNAL("textChanged(QString)"), self.edited)
        #control's button
        self.button = QPushButton("Browse")
        self.addWidget(self.button)
        self.connect(self.button, SIGNAL("clicked()"), self.browse)

        #function to call after successful change of path
        self.callback = callback
        #text for file dialog
        self.browseTitle = browseTitle
        #allowed extensions
        self.extensions = extensions
        #select file or directory
        self.browseDirectory = browseDirectory
        #show or hide hidden files
        self.showHidden = showHidden
        #function for setStatus display
        self.setStatus = setStatus
        #text for invalid path
        self.setStatusNotValid = label+" not valid!"
        #python string containing selected path
        self.path = ""
        #should callback be called
        self.noCallback = False
        #is path valid
        self.pathValid = True

    def browse(self):
        """callback for Browse button"""
        if self.browseDirectory:
            #dialog for selecting directories
            dialog = QFileDialog(None,self.browseTitle,self.edit.text())
            dialog.setFileMode(QFileDialog.Directory)
            if self.showHidden:
                dialog.setFilter(QDir.AllEntries | QDir.Hidden )
        else:
            #dialog for selecting files
            dialog = QFileDialog(None,self.browseTitle,os.path.dirname(self.path),self.extensions)
            if self.pathValid:
                dialog.selectFile(self.path)
            dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        if dialog.exec_() == QDialog.Accepted:
            #if user selected something
            self.path = unicode(dialog.selectedFiles()[0])
            self.pathValid = True
            self.noCallback = True
            self.edit.setText(self.path)
            self.noCallback = False
            if self.setStatus != None: self.setStatus()
            if self.callback != None: self.callback()

    def edited(self):
        """callback for edit control"""
        self.path = unicode(self.edit.text())
        self.pathValid = os.access(self.path, os.F_OK)
        if self.pathValid:
            if self.setStatus != None: self.setStatus()
        else:
            if self.setStatus != None: self.setStatus(self.setStatusNotValid)
            return
        if self.noCallback: return
        elif self.callback != None: self.callback()

class EditControl(QHBoxLayout):
    """control containing label and edit control"""
    def __init__(self, label, toolTip, callback=None, parent=None): 
        super(EditControl, self).__init__(parent)

        #control's label
        self.label = QLabel(label+":")
        self.addWidget(self.label)
        #control's edit
        self.edit = QLineEdit()
        self.addWidget(self.edit,1)
        self.callback = callback
        self.edit.setToolTip(toolTip)
        self.connect(self.edit, SIGNAL("textChanged(QString)"), self.edited)

    def edited(self):
        """callback for edit control"""
        self.text = unicode(self.edit.text())
        if self.callback != None: self.callback()

class MainWindow(QMainWindow):
    """main application window"""
    def __init__(self, parent=None): 
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Wine Launcher Creator")
        self.setWindowIcon(QIcon.fromTheme('wine'))

        self.centralWidget = QWidget()
        self.centralWidgetLayout = QVBoxLayout()
        self.centralWidget.setLayout(self.centralWidgetLayout)
        self.setCentralWidget(self.centralWidget)

        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("setStatusbar")
        self.setStatusBar(self.statusBar)

        #widget containing main interface
        self.widget1 = QWidget()
        self.layout1 = QVBoxLayout()
        self.layout1.setAlignment(Qt.AlignTop)
        self.widget1.setLayout(self.layout1)
        self.centralWidgetLayout.addWidget(self.widget1)

        self.executable = BrowseControl("Exe path", "Select exe file", "Path to an Windows executable file",
            self.exeCallback, "exe (*.exe *.EXE)", setStatus=self.setStatus)
        self.layout1.addLayout(self.executable)

        self.application = BrowseControl("Toplevel app path", "Select toplevel application path", "Path to application's toplevel directory"+
            "\n(used to search for additional ico/png files and to guess application name)", self.appCallback, browseDirectory=True, setStatus=self.setStatus)
        self.layout1.addLayout(self.application)

        self.name = EditControl("Name","Launcher's name")
        self.layout1.addLayout(self.name)

        label = QLabel("Select application icon:")
        self.layout1.addWidget(label)

        self.iconWidget = QListWidget()
        self.layout1.addWidget(self.iconWidget)
        self.iconWidget.setViewMode(QListView.IconMode)
        self.iconWidget.setMovement(QListView.Static)
        self.iconWidget.setResizeMode(QListView.Adjust)
        self.iconWidget.setIconSize(QSize(256,256))

        self.prefix = BrowseControl("Wine prefix path", "Select Wine prefix path", 
            "Path to directory containing Wine bottle", browseDirectory=True, setStatus=self.setStatus, showHidden=True)
        self.layout1.addLayout(self.prefix)

        #always visible buttons
        layout = QHBoxLayout()
        self.centralWidgetLayout.addLayout(layout)
        button = QPushButton("Settings")
        self.settings = button
        button.setCheckable(True)
        layout.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.settingsToggle)
        button = QPushButton("Create exe launcher")
        layout.addWidget(button,1)
        self.connect(button, SIGNAL("clicked()"), self.createLauncher)
        button = QPushButton("About")
        layout.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.about)

        #widget containing options interface
        self.widget2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.layout2.setAlignment(Qt.AlignTop)
        self.widget2.setLayout(self.layout2)
        self.centralWidgetLayout.addWidget(self.widget2)
        self.widget2.hide()

        self.launcher = BrowseControl("Launcher path", "Select launcher path",
            "Path to directory for launcher creation", browseDirectory=True, setStatus=self.setStatus)
        self.layout2.addLayout(self.launcher)

        self.icons = BrowseControl("Icons path", "Select icons path", "Path to directory for storing icons",
            browseDirectory=True, setStatus=self.setStatus)
        self.layout2.addLayout(self.icons)

        self.wine = EditControl("Wine command", "Command used to run Windows applications")
        self.layout2.addLayout(self.wine)

        button = QPushButton("Install Wine Launcher Creator as Gnome 2 Nautilus Action")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.nautilus2Action)

        button = QPushButton("Install Wine Launcher Creator as Gnome 3 Nautilus Action")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.nautilus3Action)

        button = QPushButton("Install Wine Launcher Creator as Nautilus Script")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.nautilusScript)

        button = QPushButton("Install Wine Launcher Creator as KDE 4 Dolphin Service menu")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.dolphinMenu)

        label = QLabel("""Additional information about restricting internet access to (untrusted) (Windows)
            <br>application can be found in /usr/local/share/wlcreator/NoInternet.txt""")
        label.setTextFormat(Qt.RichText)
        self.layout2.addWidget(label)

        button = QPushButton("Open NoInternet.txt")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.openNoInternet)

        button = QPushButton("Revert settings to default values")
        self.layout2.addWidget(button)
        self.connect(button, SIGNAL("clicked()"), self.defaultConfig)

        #temorary directory for icon extraction
        self.temporary = tempfile.mkdtemp()
        #first argument is path to exe file
        path = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else ""
        path = urllib.unquote(path)
        self.executable.edit.setText(path.decode("utf-8"))
        #second argument is path to main application directory (ico files search path/initial name guess)
        path = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.dirname(self.executable.path).encode("utf-8")
        path = urllib.unquote(path)
        self.application.edit.setText(path.decode("utf-8"))

        #user's desktop location
        self.desktopPath = check_output(["xdg-user-dir", "DESKTOP"]).decode("utf-8")
        while self.desktopPath[-1] == "\n": self.desktopPath = self.desktopPath[:-1]

        #default config options
        self.cfgDefaults = {'Launcher': self.desktopPath,
                            'Icons': os.path.expanduser("~/.local/share/icons/wlcreator"),
                            'Wine': "wine",
                            'WinePrefix': os.path.expanduser("~/.wine")}

        #directory for program's configuration file
        self.config = os.path.expanduser("~/.config/wlcreator")
        self.loadConfig()

        self.populateIconList()
        self.resize(QSize(700,500))
        if self.executable.path == "": self.setStatus("Select an exe file.")

    def cleanup(self):
        """executed at the end"""
        self.saveConfig()
        self.clearTemporary()
        os.rmdir(self.temporary)

    def clearTemporary(self):
        """removes all files in temporary directory"""
        if self.temporary != "":
            fileList = glob.glob( os.path.join(self.temporary, '*.*') )
            for f in fileList:
                os.remove(f)

    def setStatus(self,text=None):
        """display of setStatus text"""
        if text == None: text = "OK."
        self.statusBar.showMessage(text)

    def exeCallback(self):
        """callback for executable path"""
        path = os.path.dirname(self.executable.path)
        if path != self.application.path:
            self.application.edit.setText(path)
        else:
            self.populateIconList()

    def appCallback(self):
        """callback for application path"""
        self.name.edit.setText(os.path.basename(self.application.path))
        self.populateIconList()

    def populateIconList(self):
        """extracts and finds all icons for specified exe and app"""
        self.iconWidget.clear()
        self.clearTemporary()
        extractedList = None
        if self.executable.path != "":
            #extract icons from all exe files in exe file's directory
            path = os.path.dirname(self.executable.path)
            exeList = glob.glob( os.path.join(path, '*.exe') )
            EXEList = glob.glob( os.path.join(path, '*.EXE') )
            exeList.extend(EXEList)
            for exe in exeList:
                bash("wrestool -x -t 14 -o \"" + self.temporary + "\" \"" + exe + "\"")
            extractedList = glob.glob( os.path.join(self.temporary, '*.ico') )
        if self.application.path != "":
            #copy all found ico files from the application directory (recursive)
            bash("find \"" + self.application.path + "/\" -iname \"*.ico\" -exec cp '{}' \"" + self.temporary + "\"/ \\;")
            #copy all found png files from the application directory
            bash("find \"" + self.application.path + "/\" -maxdepth 1 -iname \"*.png\" -exec cp '{}' \"" + self.temporary + "\"/ \\;")
            #png files are searched only in selected directory (non-recursive) because many games have a lot of png files
        #check if there are any icon files
        if len(os.listdir(self.temporary)) == 0:
            self.setStatus("Could not extract/find any icons! Try using wrestool manually.")
            return

        #convert ico files to png files
        icoList = glob.glob( os.path.join(self.temporary, '*.ico') )
        for ico in icoList:
            bash("icotool -x " + "\""+ico+"\"", self.temporary)

        #create list of png files
        pngList = glob.glob( os.path.join(self.temporary, '*.png') )
        PNGList = glob.glob( os.path.join(self.temporary, '*.PNG') )
        pngList.extend(PNGList)
        if len(pngList) == 0:
            self.setStatus("Could not convert ico(s) to png(s)! Try using icotool manually, or try GIMP.")
            #copy extracted icons to app directory
            if len(extractedList) > 0:
                for f in extractedList: bash("cp \"" + f + "\" \"" + self.application.path + "\"")
            return
        #insert png files in iconWidget
        for png in pngList:
            pixmap = QPixmap(png)
            icon = QIcon(pixmap)
            widget = QListWidgetItem(icon,str(pixmap.width())+"x"+str(pixmap.height())+"x"+str(pixmap.depth()))
            widget.setData(Qt.UserRole,png)
            widget.setToolTip("Width:"+str(pixmap.width())+"\nHeight:"+str(pixmap.height())+"\nDepth:"+str(pixmap.depth()))
            self.iconWidget.addItem(widget)
        self.setStatus("Icons extracted/found. Select one.")

    def createLauncher(self):
        """creates .desktop file"""
        if not self.executable.pathValid: return
        if not self.application.pathValid: return
        #create icons directory, if it doesn't exist
        if not os.access(self.icons.path, os.F_OK):
            os.makedirs(self.icons.path)
        #get selected icon
        items = self.iconWidget.selectedItems()
        if len(items) == 0:
            self.setStatus("You need to select an icon first.")
            return
        #full path to selected icon
        iconSource = unicode(items[0].data(Qt.UserRole).toString())
        #icon's name
        iconName = os.path.basename(iconSource)
        #full path to destination icon
        iconDestination = os.path.join(self.icons.path,iconName)
        #copy icon file
        shutil.copyfile(iconSource,iconDestination)
        #directory of exe file
        exeDirectory = os.path.dirname(self.executable.path)
        #generate launcher's contents
        launcherText = "#!/usr/bin/env xdg-open"
        launcherText += "\n[Desktop Entry]"
        launcherText += "\nVersion=1.0"
        launcherText += "\nType=Application"
        launcherText += "\nTerminal=false"
        launcherText += "\nExec=env WINEPREFIX=\"" + self.prefix.path + "\" " + \
                        self.wine.text + " \"" + self.executable.path + "\""
        launcherText += "\nPath=" + exeDirectory
        launcherText += "\nName=" + self.name.text
        launcherText += "\nIcon=" + iconDestination
        #full path to launcher
        launcherPath = os.path.join(self.launcher.path, self.name.text+".desktop")
        #write launcher's contents
        launcherFile = open(launcherPath, "w")
        launcherFile.write(launcherText.encode("utf-8"))
        launcherFile.close()
        #make it executable
        bash("chmod 755 \"" + launcherPath + "\"")
        launcherLocalAppPath = os.path.expanduser("~/.local/share/applications/wlcreator/")
        if not os.access(launcherLocalAppPath, os.F_OK):
            os.makedirs(launcherLocalAppPath)
        launcherLocalAppPath = os.path.join(launcherLocalAppPath, self.name.text+".desktop")
        if launcherPath != launcherLocalAppPath:
            shutil.copyfile(launcherPath,launcherLocalAppPath)
            bash("chmod 755 \"" + launcherLocalAppPath + "\"")
            self.setStatus("Launcher created in "+self.launcher.path+". A copy is also in ~/.local/share/applications/wlcreator/")
        else:
            self.setStatus("Launcher created in "+self.launcher.path)

    def defaultConfig(self):
        """creates default configuration options"""
        self.launcher.edit.setText(self.cfgDefaults['Launcher'])
        self.icons.edit.setText(self.cfgDefaults['Icons'])
        self.wine.edit.setText(self.cfgDefaults['Wine'])
        self.prefix.edit.setText(self.cfgDefaults['WinePrefix'])

    def loadConfig(self):
        """load configuration options"""
        cfgfile = os.path.join(self.config,"settings.ini")
        cfgRead = False
        if os.access(cfgfile, os.F_OK):
            #if config exists, load it
            cfg = ConfigParser.SafeConfigParser(self.cfgDefaults)
            cfg.read(cfgfile)
            if "WLCreator" in cfg.sections():
                self.launcher.edit.setText(cfg.get("WLCreator","Launcher").decode("utf-8"))
                self.icons.edit.setText(cfg.get("WLCreator","Icons").decode("utf-8"))
                self.wine.edit.setText(cfg.get("WLCreator","Wine").decode("utf-8"))
                self.prefix.edit.setText(cfg.get("WLCreator","WinePrefix").decode("utf-8"))
                cfgRead = True
        if not cfgRead:
            self.defaultConfig()

    def saveConfig(self):
        """save configuration options"""
        #create config directory, if it doesn't exist
        if not os.access(self.config, os.F_OK):
            os.makedirs(self.config)
        cfgfile = open(os.path.join(self.config,"settings.ini"),"w")
        cfg = ConfigParser.SafeConfigParser()
        if not cfg.has_section("WLCreator"):
            cfg.add_section("WLCreator")
        cfg.set("WLCreator","Launcher",self.launcher.path.encode("utf-8"))
        cfg.set("WLCreator","Icons",self.icons.path.encode("utf-8"))
        cfg.set("WLCreator","Wine",self.wine.text.encode("utf-8"))
        cfg.set("WLCreator","WinePrefix",self.prefix.path.encode("utf-8"))
        cfg.write(cfgfile)

    def settingsToggle(self):
        """toggle between main interface and options"""
        if self.settings.isChecked():
            self.widget1.hide()
            self.statusBar.hide()
            self.widget2.show()
        else:
            self.widget1.show()
            self.statusBar.show()
            self.widget2.hide()

    def nautilus2Action(self):
        bash("gconftool-2 --load /usr/local/share/wlcreator/wlcaction.xml")

    def nautilus3Action(self):
        path = os.path.expanduser("~/.local/share/file-manager/actions/")
        bash("mkdir -p " + path)
        bash("cp /usr/local/share/wlcreator/wlcreatorGnome.desktop " + path)

    def nautilusScript(self):
        path = os.path.expanduser("~/.gnome2/nautilus-scripts/")
        bash("mkdir -p " + path)
        bash("ln -s /usr/local/bin/wlcreator.py " + path + "/Wine\ Launcher\ Creator")

    def dolphinMenu(self):
        path = os.path.expanduser("~/.kde4/share/kde4/services/ServiceMenus/")
        bash("mkdir -p " + path)
        bash("cp /usr/local/share/wlcreator/wlcreatorKDE.desktop " + path)
        #alternative path; probably can be deleted
        path = os.path.expanduser("~/.kde/share/kde4/services/ServiceMenus/")
        bash("mkdir -p " + path)
        bash("cp /usr/local/share/wlcreator/wlcreatorKDE.desktop " + path)

    def openNoInternet(self):
        bash("xdg-open /usr/local/share/wlcreator/NoInternet.txt")

    def about(self):
        """displays about dialog"""
        text = u"Wine Launcher Creator v"+VERSION+u" (c) 2011  Žarko Živanov"
        text += "<br>E-Mail: zzarko@gmail.com"
        text += "<br><br>University of Novi Sad, Faculty Of Technical Sciences"
        text += "<br>Chair for Applied Computer Science"
        text += ', <a href="http://www.acs.uns.ac.rs/">http://www.acs.uns.ac.rs</a>'
        text += "<br><br>Linux User Group of Novi Sad"
        text += ', <a href="http://www.lugons.org/">http://www.lugons.org/</a>'

        gpl = "<br><br>This program is free software: you can redistribute it and/or modify"
        gpl += "it under the terms of the GNU General Public License as published by"
        gpl += "the Free Software Foundation, either version 3 of the License, or"
        gpl += "(at your option) any later version."
        gpl += "<br><br>This program is distributed in the hope that it will be useful,"
        gpl += "but WITHOUT ANY WARRANTY; without even the implied warranty of"
        gpl += "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
        gpl += "GNU General Public License for more details."
        gpl += "<br><br>You should have received a copy of the GNU General Public License"
        gpl += "along with this program. If not, see "
        gpl += "<a href=http://www.gnu.org/licenses>http://www.gnu.org/licenses</a>."

        dialog = QMessageBox(QMessageBox.Information,"About",text+gpl)
#        dialog.setInformativeText(gpl)
        dialog.setTextFormat(Qt.RichText)
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if checkDependencies():
        main = MainWindow()
        main.show()
        app.exec_()
        main.cleanup()

"""
History of changes

Version 1.0.6
    - Fix for missing 'WLCreator' section in config file
    - Makefile doesn't create '/usr/share/nautilus-scripts/Wine Launcher Creator' anymore
    - Makefile gets program version from wlcreator.py
    - Readme was made better, program page on google also
    - Added button to reset configuration options
    - Fixed png from ico extraction
    - Fixed file copy for integration into gnome/kde
    - Main window made a slightly wider

Version 1.0.5
    - Added Wine prefix setting and changed Exec part of the launcher to include it
    - Default icons path changed to ~/.local/share/icons/wlcreator/
    - gpl text in About dilaog converted to RichText
    - Added program icon - I used 'Wine' icon, as I'm no artist - any contribution is welcome
    - Added various ways to install in Nautilus and Dolphin directly from GUI
    - Added wlcreator.desktop and wlcreatorKDE.desktop for Nautilus 3 and Dolphin integration
    - Removed ImageMagick dependency from deb file
"""

