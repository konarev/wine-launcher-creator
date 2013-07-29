About
-----
WLCreator is a Python program (script) that creates Linux desktop launchers for
Windows programs (using Wine). The program does the following tasks:

   1. Find/extract ico files (using icoutils)
   2. Convert ico files to png files (using icoutils)
   3. Present the user with graphical interface, where he/she can choose the icon for launcher, and
   4. Create desktop launcher


Usage
-----
WLCreator will try to extract icons from exe file, and to search for all ico
files in exe's directory and its subdirectories, and to convert them to png
files. Additionaly, it will search for png files in application's main
directory. After that, the user is presented with a graphical interface where
he/she can choose the icon and launcher's name. A few options are also
available:

    * Toplevel application path - path to search for program's icon
      (Windows games often have their executable in some subdirectory under the
      main game directory - usually you should choose main game directory for
      icon search)
    * Path for launcher creation (default is ~/Desktop/)
      (a copy of launcher is also created in ~/.local/share/applications/wlcreator/)
    * Path for icon (default is ~/.local/share/icons/wlcreator/)
    * Wine command for launching (default is wine)
    * Path for wine configuration directory (default is ~/.wine)

Options are saved in ~/.config/wlcreator/ directory.

WLCreator uses wrestool (icoutils) to extract icons from exe files, and icotool
(icoutils) to convert ico files to png files. It uses Qt framework and PyQt
bindings for Python, and also some bash commands.

Sometimes wrestool cannot extract icons, and this is the situation where icon
extraction/finding must be done separately by the user. When ico/png file is
obtained, just put it alongside exe file and start wlcreator.

Also, icotool sometimes cannot extract png from ico, and in this situation, easy
solution is to open ico file with GIMP, and save as png (for this, wlcreator
will save all extracted ico files in exe's directory).


Integration
-----------
To use it as nautilus action, you need to install nautilus-actions package.
After that, you can use appropriate option in Settings section to install this
script as nutilus action:
 - for Gnome 2 select Gnome 2 (maybe works in Mate)
 - for Gnome 3/Unity select Gnome 3 (maybe works in Cinnamon)
or alternatively, you can use System->Preferences->Nautilus Actions Configuration
to import /usr/local/share/wlcreator/wlcaction.xml

To use it as nautilus script, you need to have nautilus-scripts-manager package
installed. You can enable it using appropriate option in Settings section,
or alternatively, you can enable it using System->Preferences->Nautilus scripts manager

To use it as a KDE 4 Dolphin Service, select appropriate option in Settings section.

IMPORTANT: Gnome 3 users need to logout/login before new launcher is active, or alternatively,
press ALT+F2 and enter "r" to restart the shell.

Integration is tested on Ubuntu 12.04 (Unity), OpenSUSE 12.3 (KDE 4) and Fedora 17 (Gnome 3).


Command line
------------
You can also run it from command line with:

wlcreator.py [path_to_exe_file [path_to_application_toplevel_directory]]


Disabling network access
------------------------
Additional information about restricting internet access to (untrusted)
(Windows) application can be found in NoInternet.txt
(/usr/local/share/wlcreator/NoInternet.txt)

