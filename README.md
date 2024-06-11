# Update TLEs

This code is used to update TLEs automatically and write them to a file, keeping only the last 5. Unfortunately, it's not 100% automated as you would need to stop the program to then use the file with TLEs on it. 

constantTLEUpdate.py is the program that is constantly getting TLEs and writing them to a file (keeping the last 5). This is the same as tleUpdate.py, but with a loop in order to be able to get the past 5 changed TLEs.

tle_history.txt is the file that contains the output of constantTLEUpdate.py.

tle_test.txt is a single TLE; the output of tleUpdate.py

tleUpdate.py takes in the NORAD ID of a satellite, goes to the n2yo.com equivalent, webscrapes that, and gets the TLEs (writes to tle_test.txt).
