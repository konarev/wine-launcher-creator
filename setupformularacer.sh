#!/bin/bash
#script to make a local copy of "Angry Animals" game by http://www.flashninjaclan.com/
#Version: 1.0
#Date:    04 April 2011
#Author:  Zarko Zivanov zzarko@gmail.com

NAME="Formula Racer"
GAMEDIR=~/".formularacer"
DESKTOP=$(xdg-user-dir DESKTOP)
DESKTOP="$DESKTOP/$NAME.desktop"

SWFNAME=FormulaRacer.swf
JPGNAME=game_formularacer.gif
PNGNAME=formularacer.png
SWFURL=http://www.turbonuke.com/flashgames/$SWFNAME
JPGURL=http://www.turbonuke.com/images/$JPGNAME
FLASHGZ=flashplayer_10_sa.tar.gz
FLASH=flashplayer
FLASHURL=http://download.macromedia.com/pub/flashplayer/updaters/10/$FLASHGZ

function error {
    echo "ERROR: $1"
    cd "$CURRDIR"
    rm -rf "$GAMEDIR"
    exit 1
}

#check dependencies
convert --version &> /dev/null
if [ $? -gt 0 ]; then
    error "imagemagick not installed!"
fi
wget --version &> /dev/null
if [ $? -gt 0 ]; then
    error "wget not installed!"
fi

tar --version &> /dev/null
if [ $? -gt 0 ]; then
    error "tar not installed!"
fi

#try to download swf file
CURRDIR=$(pwd)
mkdir "$GAMEDIR"
cd "$GAMEDIR"
wget $SWFURL
#cp $CURRDIR/angryanimals.swf .
if [ $? -gt 0 ]; then
    error "$SWFNAME download error!"
fi

#try to download jpg file
wget $JPGURL
#cp $CURRDIR/angryanimals.jpg .
if [ $? -gt 0 ]; then
    error "$JPGNAME download error!"
fi
convert $JPGNAME $PNGNAME
rm $JPGNAME

#try to download flash player
wget $FLASHURL
#cp $CURRDIR/flashplayer_10_sa.tar.gz .
if [ $? -gt 0 ]; then
    error "$FLASH download error!"
fi
tar -xzf $FLASHGZ
rm $FLASHGZ

#make desktop launcher
echo "#!/usr/bin/env xdg-open" > "$DESKTOP"
echo "[Desktop Entry]" >> "$DESKTOP"
echo "Version=1.0" >> "$DESKTOP"
echo "Type=Application" >> "$DESKTOP"
echo "Terminal=false" >> "$DESKTOP"
echo "Exec=$GAMEDIR/$FLASH $GAMEDIR/$SWFNAME" >> "$DESKTOP"
echo "Name=$NAME" >> "$DESKTOP"
echo "Comment=$NAME (c) http://www.flashninjaclan.com/" >> "$DESKTOP"
echo "Icon=$GAMEDIR/$PNGNAME" >> "$DESKTOP"
chmod 777 "$DESKTOP"

cd "$CURRDIR"
echo "Sucess!"
exit 0

