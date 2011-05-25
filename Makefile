prefix=/usr/local/
name=wine-launcher-creator
version=1.0.3

cleanmac = \
	rm -f /usr/share/nautilus-scripts/Wine\ Launcher\ Creator ; \
	rm -f $(prefix)/bin/wlcreator.py ; \
	rm -f $(prefix)/bin/installwlcaction ; \
	rm -f $(prefix)/bin/installwlcscript ; \
	rm -f $(prefix)/share/wlcreator/NoInternet.txt ; \
	rm -f $(prefix)/share/wlcreator/Readme.txt ; \
	rm -f $(prefix)/share/wlcreator/gpl.txt ; \
	rm -f $(prefix)/share/wlcreator/wlcaction.xml ; \
	rmdir $(prefix)/share/wlcreator/

install:
	mkdir -p $(prefix)/bin/
	mkdir -p $(prefix)/share/wlcreator/
	install -m 0755 wlcreator.py $(prefix)/bin/
	install -m 0755 installwlcaction $(prefix)/bin/
	install -m 0755 installwlcscript $(prefix)/bin/
	ln -s $(prefix)/bin/wlcreator.py /usr/share/nautilus-scripts/Wine\ Launcher\ Creator
	install -m 0644 NoInternet.txt $(prefix)/share/wlcreator/
	install -m 0644 Readme.txt $(prefix)/share/wlcreator/
	install -m 0644 gpl.txt $(prefix)/share/wlcreator/
	install -m 0644 wlcaction.xml $(prefix)/share/wlcreator/

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
	checkinstall --nodoc --install=no --pkgname=$(name) --pkgversion=$(version) --maintainer=zzarko@gmail.com --requires=python,python-qt4,icoutils,imagemagick,xdg-utils --default
	${cleanmac}

.PHONY: install, uninstall, clean, archive, deb

