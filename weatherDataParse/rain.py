# Notes:
#
#   Determine the number of days it rained this past winter
#   Read precipitation and min. temp for each date/row
#
#   The column header lines were throwing an error.
#   It was not the regex pattern!   First line was crashing
#
#   Get the correct Sys.argv[1] position  (print em)
#   Anaconda:  Run -> Configuration per file -> Command Line Options -> 10605.txt
#
#   Dont just search for (\d\d) for temps, since it can be single digit
#   Used (\d{1,2}) which is greedy
#
#
# File format:
#
#STATION           STATION_NAME                                       DATE     PRCP     TAVG     TMAX     TMIN     WT01     WT04
#----------------- -------------------------------------------------- -------- -------- -------- -------- -------- -------- --------
#GHCND:USW00094745                       WESTCHESTER CO AIRPORT NY US 20200101 0.00     -9999    38       30       -9999    -9999
#GHCND:USW00094745                       WESTCHESTER CO AIRPORT NY US 20200102 0.00     -9999    48       28       -9999    -9999

import os       #file system stuff
import sys      #exit cmd
import re       #regex lin

if (len(sys.argv) != 2):
    sys.exit("Usage: python rain.py FILENAME.txt")

rain = 0

filename = os.getcwd() + '/' + sys.argv[1]
file = open(filename)

for line in file:

    #set the regEx
    rainRegEx = re.compile(r'.*US \d{8} (\d.\d\d)(\s)+-9999(\s)+(\d{1,2})+(\s)+(\d{1,2})+.*')

    #apply the regEx to the current line
    mo = rainRegEx.search(line)

    #extract the desired data column
    try:
        prcp = float(mo.group(1))
        min = float(mo.group(6))
        print('prcp={} & min={}'.format(prcp,min))
        
        if (min > 35 and prcp > 0):
            rain += 1
            print('Rain!')
    except:
        pass
        #print('Bad data:' + line)

print ('It rained on {} days\n'.format(rain))


############  STUB code
        #print ('min = {}, prcp = {}'.format(min, prcp))

        #for i in range(1,7):
        #    print('{} is {}'.format(i,mo.group(i)))
