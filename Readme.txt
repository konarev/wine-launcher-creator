Wine Launcher Creator is a Python program (script) that creates Linux desktop launchers for Windows programs
(using Wine). The program does the following tasks:

   1. Find/extract ico files (using icoutils)
   2. Convert ico files to png files (using imagemagick)
   3. Present the user with graphical interface (using PyQt?), where he/she can choose the icon for launcher
   4. Create desktop launcher 

The program can be easily integrated in Nautilus (as nautilus-script).

Basic usage:
./wlcreator.[py path_to_exe_file [path_to_application_toplevel_directory]]

WLCreator will try to extract icons from exe file, and to search for all ico files in exe's directory and its
subdirectories, and to convert them to png files. Additionaly, it will search for png files in application's
main directory. After that, the user is presented with a graphical interface where he/she can choose the icon and
launcher's name. A few options are also available:
- Path for launcher creation (default is ~/Desktop/)
- Path for icon (default is ~/.icons/)
- Wine command for launching (default is wine)
Options are saved in ~/.config/wlcreator/ directory.

WLCreator uses wrestool (icoutils) to extract icons from exe files, and convert (imagemagick) to convert ico files
to png files. It uses Qt framework and PyQt bindings for Python, and also some bash commands.

Sometimes wrestool cannot extract icons, and this is the situation where icon extraction/finding must
be done separately by the user. When ico/png file is obtained, just put it alongside exe file and start wlcreator.

Also, convert sometimes cannot extract png from ico, and in this situation, easy solution is to open ico file with
gimp, and save as png (for this, wlcreator will save all extracted ico files in exe's directory).

Install.txt conatins installation instructions and steps needed to integrate the program in nautilus.
NoInternet.txt contains manual for forbidding internet access for (wine) programs, if needed.

