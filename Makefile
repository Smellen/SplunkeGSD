SplunkeApp = SplunkeGSD

default: 
	echo "Please run: \n1. make install \n2.  make test \n3.  make clean"

install:
	find controllers/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 
	find views/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 
	find tests/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 	
	rm -rf ${HOME}/public_html/web2py/applications/${SplunkeApp}
	mkdir -p ${HOME}/public_html/web2py/applications/${SplunkeApp} 
	cp -r * ${HOME}/public_html/web2py/applications/${SplunkeApp}
	python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p 8080

install-web2py:
	echo "Please note this will remove current version of web2py"
	read Confirm
	rm -rf ${HOME}/public_html/web2py
	mkdir -p ${HOME}/public_html
	unzip web2py_src.zip
	mv web2py/ ${HOME}/public_html
	mv ${HOME}/public_html/web2py/handlers/wsgihandler.py ${HOME}/public_html/web2py/wsgihandler.py

run: 	
	python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p 8080
test: 
	clear 
	python ${HOME}/public_html/web2py/applications/${SplunkeApp}/tests/testTeam.py
clean: 	
	clear
	cd 
	rm -r ${HOME}/public_html/web2py/applications/${SplunkeApp}
