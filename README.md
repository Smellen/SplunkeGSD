SplunkeGSD
==========

GSD sim game

Once installed, the application can be reached at 
https://localhost:8080/SplunkeGSD

We are using the python web framework "Web2Py" - http://web2py.com/ 

The installation installs this framework during installation. 

Installation Instructions
=========================

If you would like to change the application name include SplunkeGSD=appname in the make command
e.g. make SplunkeGSD=appname install

Additional Install Notes: 
- The commands will need to use sudo 
- The application will install in /home/www-data which it creates itself 
- In order to not write over any files that might already be there, select [N]one if asked to replace, this will use the files that are there. 
- If asked about mail server, select No Config

To install web2py: run make install-web2py

To update the application to current version (from tar): run make install

To clean the application: run make clean with the make file out of the directory. 

To test the application : run make test


Download Files
===============

The application is also able to be downloaded using a tar file at each release. 
- Release 0 : pub.mmcgarr.me/team_splunke_release0.tar.gz
- Iteration 1: pub.mmcgarr.me/team_splunke_iteration1.tar.gz
- Iteration 2: pub.mmcgarr.me/team_splunke_iteration2.tar.gz
- Iteration 3:


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



Iteration 2
============
Released: 20/02/2014

Implemented:
- (Feature 6) Map based status display showing which sites are making normal progress, which are behind, which are failing.

New title screen has been added. The options to choose from are Create New Game or Select from Predefined Games. Creating a new game will take the player to the map screen. They will then be able to choose next day to continue progress or restart game which takes them back to title screen.

- (Feature 20) Default game scenarios including pre-specified product and site configuration.
All default game scenarios have been added to SplunkeGSD/scenarios. All files in this location are different scenarios stored in JSON format and users can select which game they want to play.

Known Issues:
- (None)

Fixed Issues:
- Fixed Issue with URL - redirects to the correct URL if you input localhost/SplunkeGSD/default and localhost/SplunkeGSD/


Iteration 3
============
Released: 06/03/2014



Implemented:

Known Issues:

Fixed Issues:


