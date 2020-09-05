import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import sys

# User must provide a CSV of orders to plot
if (len(sys.argv) != 2):
    sys.exit("Usage: python plot.py FILENAME.csv")

# Open the CSV file
# File format: 7/11/2016,433.01
file = open(sys.argv[1])

# 2 arrays to plot (x,y) 
dates_obj = []
amounts = []
dateMaskCSV = '%Y-%m-%d'
totalSpent = 0

for line in file:
    
    #Convert into Python datetime
    cols = line.split(',')
    datetime_object = datetime.strptime(cols[0], dateMaskCSV)
    dates_obj.append(datetime_object)
    
    # append CUMULATIVE amount spent
    totalSpent += float(cols[1])
    amounts.append(totalSpent)

# Convert datetime into matplot dates
dates_matplot = matplotlib.dates.date2num(dates_obj)

plt.plot_date(dates_matplot,amounts)
plt.show()
