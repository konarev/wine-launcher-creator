# Wine launcher Creator install script
# If you want to make a deb package using this script, you should install 'checkinstall'

prefix=/usr/local/
name=wine-launcher-creator
version=$(shell grep "VERSION=" wlcreator.py | grep -o -E "[.0-9]*")

cleanmac = \
	rm -f $(prefix)/bin/wlcreator.py ; \
	rm -f $(prefix)/share/wlcreator/NoInternet.txt ; \
	rm -f $(prefix)/share/wlcreator/Readme.txt ; \
	rm -f $(prefix)/share/wlcreator/gpl.txt ; \
	rm -f $(prefix)/share/wlcreator/wlcaction.xml ; \
	rm -f $(prefix)/share/wlcreator/wlcreatorGnome.desktop ; \
	rm -f $(prefix)/share/wlcreator/wlcreatorKDE.desktop ; \
	rm -f /usr/share/applications/wlcreator.desktop ; \
	rmdir $(prefix)/share/wlcreator/

install:
	mkdir -p $(prefix)/bin/
	mkdir -p $(prefix)/share/wlcreator/
	mkdir -p /usr/share/nautilus-scripts/
	install -m 0755 wlcreator.py $(prefix)/bin/
	install -m 0644 NoInternet.txt $(prefix)/share/wlcreator/
	install -m 0644 Readme.txt $(prefix)/share/wlcreator/
	install -m 0644 gpl.txt $(prefix)/share/wlcreator/
	install -m 0644 wlcaction.xml $(prefix)/share/wlcreator/
	install -m 0644 wlcreatorGnome.desktop $(prefix)/share/wlcreator/
	install -m 0644 wlcreatorKDE.desktop $(prefix)/share/wlcreator/
	install -m 0644 wlcreator.desktop /usr/share/applications/

uninstall:
	${cleanmac}

clean:
	rm -f *.deb
	rm -f *.gz
	rm -f *.tgz
	rm -f *~

archive: clean
	tar --exclude=*.gz -czf $(name)-$(version).tar.gz ../$(name)

deb:
	checkinstall --nodoc --install=no --arch=all --pkgname=$(name) --pkgversion=$(version) --maintainer=zzarko@gmail.com --requires=python,python-qt4,icoutils,xdg-utils --default
	${cleanmac}

.PHONY: install, uninstall, clean, archive, deb

