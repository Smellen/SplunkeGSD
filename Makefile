SplunkeGSD=SplunkeGSD 

default: 
	echo "Please run: \n1. make install \n2.  make test \n3.  make clean"

install: 
	sudo rm -rf ${HOME}/public_html/web2py/applications/${SplunkeGSD}
	sudo mkdir ${HOME}/public_html/web2py/applications/${SplunkeGSD} 
	sudo cp -r * ${HOME}/public_html/web2py/applications/${SplunkeGSD}
	#sudo chown -R www-data:www-data ${HOME}/public_html/web2py/applications/${SplunkeGSD}/
	sudo python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p 8080

install-web2py:
	unzip web2py_src.zip
	sudo mv web2py/ ${HOME}/public_html
	sudo mv ${HOME}/public_html/web2py/handlers/wsgihandler.py ${HOME}/public_html/web2py/wsgihandler.py
	#sudo chown -R www-data:www-data ${HOME}/public_html/web2py

run: 	
	sudo python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p 8080
test: 
	clear 
	python ${HOME}/public_html/web2py/applications/${SplunkeGSD}/tests/testTeam.py
clean: 	
	clear
	cd 
	sudo rm -r ${HOME}/public_html/web2py/applications/${SplunkeGSD}
