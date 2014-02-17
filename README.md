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
Released: 05/02/2014

Implemented: 
- (Feature 17) Master configuration (file) that specifies certain global values unlikely to change from one simulation to the next. This can be a simple configuration file in any human-readable/editable format (json, xml, yaml, ...)

The config file is located at ./application.config


Known Issues: 
- None

Fixed Issues: 
- None

Iteration 1
============
Released: 12/02/2014

Implemented:
- (Feature 9) Process simulator that calculates progress on each task for each module for each simulated day in the game. Taking into account the development method (waterfall or agile; follow-the-sun are taken into account sperately).

A page refresh simulates the end of a day. It will display the current effort and at what stage the module is at or if it has been completed.

Example Output:

[Test Module is 10.0 of 60.8879480518 done. Current Stage: Implementation]

[Test Module is 39.2829866538 of 39.2829866538 done. Current Stage: Complete]

Known Issues:
- (1) web2py Invalid Request when trying to access localhost/SplunkeGSD. Do not remove the welcome application from the applications folder. Without this application web2py admin page can not be reached.

Fixed Issues:
- None
