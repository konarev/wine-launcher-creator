prefix=/usr/local/
name=wine-launcher-creator
version=1.0.5

cleanmac = \
	rm -f /usr/share/nautilus-scripts/Wine\ Launcher\ Creator ; \
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
	install -m 0755 wlcreator.py $(prefix)/bin/
	ln -s $(prefix)/bin/wlcreator.py /usr/share/nautilus-scripts/Wine\ Launcher\ Creator
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

