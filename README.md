SplunkeGSD
==========

GSD sim game

Once installed, the application can be reached at 
http://localhost:8080/SplunkeGSD

We are using the python web framework "Web2Py" - http://web2py.com/ 


Installation Instructions
=========================

First-Time Install
------------------
These instructions will install web2py in $HOME/public_html/web2py, place the application in the correct folders and run web2py (which can be seen at http://localhost:8080/SplunkeGSD or http://localhost:port/appname )

1. run 'make install-web2py'  
2. run 'make install' (if the app name or port want to be changed from default, please see below)
If you would like to change the application name include SplunkeApp=appname in the make command
e.g. 'make SplunkeApp=appname install'

The same is for changing the port, it will automatically run on port 8080, include port=port_number in the make command 
e.g. 'make port=9090 install'

Web2Py Already Installed in $HOME/public_html/web2py without Application OR To Install the Application from TAR
------------------------------------------------------------------------------------------------------------
These installation instructions will REMOVE any version of the application with the same name and pull the application files from the tar folder. 

1. run 'make install' (if the app name or port want to be changed from default, please see below)
If you would like to change the application name include SplunkeApp=appname in the make command
e.g. 'make SplunkeApp=appname install'

The same is for changing the port, it will automatically run on port 8080, include port=port_number in the make command 
e.g. 'make port=9090 install'

The application will be visable at http://localhost:8080/SplunkeGSD or http://localhost:port/appname

To run application once configured
------------------------------------
These running instructions will run web2py with the current application settings. 

1. run 'make run'
If you would like to change the port, it will automatically run on port 8080, include port=port_number in the make command 
e.g. 'make port=9090 run' 

The application will be visable at http://localhost:8080/SplunkeGSD or http://localhost:port/appname

To Clean the Application
-------------------------
These instructions will remove the application from web2py. 
1. run 'make clean' 
Please note that this must be run with the make script outside the application directory. 

To Test the Application
--------------------------
These instructions will test the application using the definded tests. 
1. run 'make test' 
Files and functions not testing in these tests are included in NOT_TESTED.csv


Features
========
1. (Feature 0 README) README file containing instructions to build, install, test, and run the product. Each feature should be documented, in order shown in the backlog, with sufficient instructions to quickly see it working from the running application.
The README.md file can be found in the root folder of the project. 
  
2. (Feature 17 Master Config) Master configuration (file) that specifies certain global values. 
This application.config file is located in the root folder of the project.
This file contains the following configuration settings:
	- Map Dimensions
	- Each city's coordinates on the map
	- Developer Cost per day per city
	- Daily development period (Ideal working hours per day)
	- Geographic distance factor between cities
	- Graphical distance interventions
	- Temporal distance (How many similar working hours)
	- Temporal distance interventions
	- Cultural distance
	- Cultural distance interventions
	- Problem (Probability for a problem to occur)
	- Percentage Delay for problem in each stage of development
	- Cost of interventions


3. (Feature 9 Process Simulator) Process simulator that calculates progress on each task for each module for each simulated day in the game.
	- To see the process simulator running:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list
		- Click 'Next Day' 
		- See Day increment and total cost increase

4. (Feature 6 Status Display) Map-based status display showing which sites are making normal progress, which are behind, which are failing.
	- To see the status display running:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list
		- Click 'Next Day' 
		- The status of each site is displayed by the coloured dot at each site location. 
	- Sites can be one of three colours
		- Green: On Schedule
		- Orange: Behind Schedule
		- Red: Failure

5. (Feature 20 Default Scenarios) Default game scenarios including pre-specified product and site configuration. 
	- All default scenarios are stored in JSON format located in  ./scenarios. 
	- To change any game scenario edit a JSON file. 
	- To create a new game scenario add a new JSON file to the ./scenarios directory.
	- To see a default scenario running:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list

6. (Feature 14 End of Game Report) End of game report comparing estimates to actual performance; report can be saved.
Upon completion of any game the report will be displayed.
	- To see the end of game report:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list
		- Repeat clicking 'Next Day' until the end of game report appears
	- The end of game report will display:
		- Each modules actual effort and estimated effort
		- Total actual effort and total estimated effort for all modules
		- Actual cost and estimated cost of development
		- Actual revenue and estimated revenue
		- Actual days and estimated days to complete development
		- Amount over budget (Cost - Budget)
		- Difference in 6 monthly revenue
		- Total money made in 6 months
		- Ability to save end of game report

7. (Feature 5 Nominal Calculator) The "nominal schedule" is just the sum of all the efforts estimated for each module, divided by a default developer-period effort value. 
	- To see the nominal schedule calculator running:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list
		- On day 0 it will display estimated days for total development and the estimated days for each module

8. (Feature 3 Game Score Calculator) Calculate game score as a function of budget and revenue.
	- To see the game score calculator running:
		- Click 'Select Pre-defined Game' from the home menu
		- Select any game from list
		- Repeat clicking 'Next Day' until the end of game report appears
		- On the end of game report a value will be shown in the 'Total money made in 6 months' section
	
9. (Feature 8 Module Completion calculator) Module-task completion calculator that determines how much effort each task for each module actually takes, based on random 25% variation.
	- This is calculated at the beginning of the game 
	- The variation can be seen in the difference between the actual and estimated effort required to finish a module displayed in the end of game report
	- To see the game score calculator running:
		- Click 'Select Pre-defined Game' from the home menu
		- Repeat clicking 'Next Day' until end of game report appears
	
10. (Feature 11 Problem Simulator) Problem simulator that occasionally selects a site or module to experience a problem, with probability determined by game parameters.
	- The probability parameter is set in the application.config file under the [Problems] section as 'probability' 
	- The probability value is in the range 0 to 1
	- The default value is set at '0.85'
	- To see the problem simulator running:
		- Click 'Select Pre-defined Game' from the home menu
		- Repeat clicking 'Next Day' until end of game report appears
		- If a problem occurs it will be displayed to the terminal and the location in which it occured 

11. (Feature 7 Inquiry Interface) Interface to submit inquiries to a site about their progress.
	- To see the inquiry interface running:
		- Click 'Select Pre-defined Game' from the home menu
		- Click 'Next Day' 
		- On the map hover over any team location
		- Select any inquiry from the location context menu 
		- Relevant information for particular inquiry is displayed

12. (Feature 16 Intervention Interface) Intervention interface that allows the player to spend resources on interventions to correct or prevent problems.
	- To see the intervention interface running:
		- Click 'Select Pre-defined Game' from the home menu
		- Click 'Next Day' 
		- On the map hover over any team location
		- Select any intervention from the location context menu 
		- Once an intervention is selected it cannot be selected again
		- Relevant information for particular intervention is displayed

13. (Feature 15 Culture Influenced Reporting) Culture-influenced reporting that causes a site's status to be displayed according to the site's culture.
	- To see the culture influenced reporting is running:
		- Click 'Select Pre-defined Game' from the home menu
		- Click 'Next Day' until a site in Asia becomes orange
		- On the map hover over any team location
		- From the site context menu select 'Send Email' and press 'Inquire' 
		- The site will report back that it is on schedule


Note: Home Problem Probablity is in (and can be changed in) the config file [Problems] -> home_prob
		

Download Files
===============

The application is also able to be downloaded using a tar file at each release. 
- Release 0 : http://pub.mmcgarr.me/team_splunke_release0.tar.gz
- Iteration 1: http://pub.mmcgarr.me/team_splunke_iteration1.tar.gz
- Iteration 2: http://pub.mmcgarr.me/team_splunke_iteration2.tar.gz
- Iteration 3: http://pub.mmcgarr.me/team_splunke_iteration3.tar.gz
- Release 1: http://pub.mmcgarr.me/team_splunke_release1.tar.gz
- Iteration 5: http://pub.mmcgarr.me/team_splunke_iteration5.tar.gz
- Iteration 6: http://pub.mmcgarr.me/team_splunke_iteration6.tar.gz
- Iteration 7: http://pub.mmcgarr.me/team_splunke_iteration7.tar.gz
- Release 2: http://pub.mmcgarr.me/team_splunke_release2.tar.gz


Release 0
===========
Released: 05/02/2014

Implemented: 
- (Feature 17) Master configuration (file) that specifies certain global values unlikely to change from one simulation to the next.

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
- (Feature 20) Default game scenarios updated. They now contain three new saves. They are located in /scenarios.

- (Feature 14) End of game report. The end of game report comparing estimates to actual performance; report can be saved.

Known Issues:
- Default Follow the Sun scenario does not implement a FTS model.

Fixed Issues:
- web2py can now be installed in user space.
- Installation script has been updated.
- URL redirection.


Release 1
==========
Released: 13/03/2014

Implemented:
- (Feature 5) Nominal Schedule Calculator calculates how long until the end of a module. The nominal schedule is done by getting the sum of all the efforts estimated for each module, divided by a default developer period effort value.

- (Feature 3) Game score calculator calculates the game score as a function of the budget and revenue.

- (Feature 14) Added to the end of game report to now contain information on the revenue and budget.

- application.config now contains a default parameter for the developer period effort value. 

- Json files edited to now contain the development type eg Agile or Waterfall.

- Able to save end of game reports which are saved in appname/saved_game_reports/ with a timestamp

Known Issues:
- None

Fixed Issues:
- None

Iteration 5
===========
Released: 20/03/2014

Implemented:
- (Testing) Added tests for methods in controllers/default.py

- (Formatting) Changed game layout to be more consistant and clear.


Known Issues:
- None

Fixed Issues:
- None


Iteration 6
===========
Released: 27/03/2014

Implemented:
- (Feature 8) Module Completion. Module task completetion calculator that determines how much effort each task for each module actually takes, based on 25% variation.

- (Feature 11) Problem Simulator. A simulator that occasionally selects a site or module to experience a problem, with a probability determined by game parameters. The probability that a site will have a problem is set in application.config.

- (Layout) On Day 0 for each game a new box containing information about each team will appear. It will display where each team is located and their team size. It will also display the module names, time estimated for the task to be complete and estimated days left.

Known Issues:
- None

Fixed Issues:
- (Revenue not returning correct value) End of game report now returns the correct revenue value.


Iteration 7
===========
Released: 03/04/2014

Implemented:
- (Testing) Controllers/default.py has now been fully tested. Test coverage is now at 100%.

- (Hovering on Map) Hovering over a site on the map displays Location, Team Size, Module Estimate. The display disappears when the users on the map. 

Known Issues:
- None

Fixed Issues:
- (Problem Simultator) For some games if there were too many problems it would cause the game to seemingly never end.

- (Last day of game was not being counted) The last day was left out due to a rounding error. This issue is fixed and the game finishes on the correct day.


Release 2
==========
Released: 10/04/2014

Implemented:
- (Feature 7) Inquiry Interface. Interface to submit inquiries to a site about their progress.

- (Feature 16) Interventation interface. Intervention interface that allows the player to spend resources on interventions to correct or prevent problems

- (Feature 15) Culture-Influence. Culture-influenced reporting that causes a site's status to be displayed according to the site's culture.

- (Formatting) Changed layout on the map display. Interventions and query alerts displayed to the user.

- (Testing) Added more tests for new functions. Eg New query and intervention functions.
Known Issues:
- None

Fixed Issues:
- None

