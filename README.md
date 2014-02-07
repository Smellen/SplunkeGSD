SplunkeGSD
==========

GSD sim game

Once installed, the application can be reached at 
https://localhost/SplunkeGSD

We are using the python web framework "Web2Py" - http://web2py.com/ 

The installation installs this framework during installation. 

Installation Instructions
=========================

To install the application: run make install 
Additional Install Notes: 
- The commands will need to use sudo 
- The application will install in /home/www-data which it creates itself 
- In order to not write over any files that might already be there, select [N]one if asked to replace, this will use the files that are there. 
- If asked about mail server, select No Config

To clean the application: run make clean with the make file out of the directory. 

To test the application : run make test


Download Files
===============

The application is also able to be downloaded using a tar file at each release, these are located in Downloads. 


Release 0
===========
Released: 05/02/14

Implemented: 
- (Feature 17) Master configuration (file) that specifies certain global values unlikely to change from one simulation to the next. This can be a simple configuration file in any human-readable/editable format (json, xml, yaml, ...)

The config file is located at ./application.config


Known Issues: 
- None

Fixed Issues: 
- None


