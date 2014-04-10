SplunkeApp = SplunkeGSD
port = 8080
@current_dir = $(shell pwd)

default: 
	@echo "Please run: \n1. make install \n2.  make test \n3.  make clean \n4. make install-web2py"

install:
	@clear
	@echo "\nInstalling Application in ~/public_html/web2py/applications/"
	@echo "This will remove any previous version with the same name - ${SplunkeApp}"
	@echo "Please press ENTER to confirm or Ctrl-C to cancel"
	@read Confirm 
	@find controllers/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 
	@find views/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 
	@find tests/ -type f -print0 | xargs -0 sed -i 's:SplunkeGSD:${SplunkeApp}:g' 	
	@rm -rf ${HOME}/public_html/web2py/applications/${SplunkeApp}
	@mkdir -p ${HOME}/public_html/web2py/applications/${SplunkeApp} 
	@cp -r * ${HOME}/public_html/web2py/applications/${SplunkeApp}
	@python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p ${port}

install-web2py:
	@clear
	@echo "Installing web2py at ~/public_html/web2py"
	@echo "Please note this will remove any version of web2py at ~/public_html/web2py/ \nPlease press ENTER to confirm or Ctrl-C to cancel \n\n"
	@read Confirm
	@rm -rf ${HOME}/public_html/web2py
	@mkdir -p ${HOME}/public_html
	@unzip web2py_src.zip
	@mv web2py/ ${HOME}/public_html
	@mv ${HOME}/public_html/web2py/handlers/wsgihandler.py ${HOME}/public_html/web2py/wsgihandler.py

run: 	
	@clear
	@echo "\n***When running, the application is available at http://localhost:8080/${SplunkeApp}\n"
	@python ${HOME}/public_html/web2py/web2py.py -a adminpass -i localhost -p ${port}

test:
	@clear
	@echo ${current_dir} 
	@echo "Running tests...\n\n" 
	@python tests/testTeam.py
	@python tests/testControllerDefault.py
clean: 	
	@clear
	@echo "Removing Application..."
	@echo "Please press ENTER to confirm or Ctrl-C to cancel"
	@read Confirm 
	@cd 
	@rm -r ${HOME}/public_html/web2py/applications/${SplunkeApp}
