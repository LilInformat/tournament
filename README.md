# Tournament
Uses Postgresql to create a database for tournament data following swiss pairing format.

Install (Mac OS):
1. Install Bleach (http://bleach.readthedocs.io/en/latest/#installing-bleach)  
2. Install Vagrant and Virtual Box (https://udacity.atlassian.net/wiki/display/BENDH/Vagrant+VM+Installation)  
3. Open terminal, navigate to directory "vagrant" of the code
  
Run (Mac OS):  
1. Open terminal
2. Enter "vagrant up" into terminal  
3. Enter "vagrant ssh" into terminal  
4. Enter "cd /vagrant/tournament" into terminal 
6. Enter "psql" into terminal  
7. Enter "\i tournament.sql" to setup database    
8. Hit "CTRL-D" to exit psql  
9. Enter "python tournament_test.py"  
