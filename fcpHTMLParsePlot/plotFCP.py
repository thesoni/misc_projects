# Does spending on a used car flatten out ? 
# Plot FCP orders, cumulative running total
#
# Import HTML table, parse it
# Plot data with pyplot
#
# The HTML table data with the order amounts looks like:
# <td data-label="Total">$177.81</td>
# <td data-label="Date">Apr 01, 2020</td>

import sys
import bs4
import matplotlib
import matplotlib.pyplot as plt
import datetime as dt

def main(): 

    # User must provide a CSV of orders to plot
    if (len(sys.argv) != 2):
        sys.exit("Usage: python plotFCP.py FILENAME.html")

    # Pass the HTML file to BS4
    file = open(sys.argv[1])
    soup = bs4.BeautifulSoup(file, features='html.parser')
    elems = soup.select('td')

    numOrders = 0
    runningTotal = 0
    
    # 2 arrays to plot (x,y) 
    dates_matplot = []
    amounts = []

    #Parse the tags in the HTML file
    for e in elems:
        attr = e.get('data-label')
        if attr == 'Date':
            date = e.getText()
            
            #Convert date string into Python datetime
            date_time_obj = dt.datetime.strptime(date, '%b %d, %Y')

            # Convert datetime into matplot date format
            date_matplot = matplotlib.dates.date2num(date_time_obj)
            dates_matplot.append(date_matplot)
            
        if attr == 'Total':
            amt = e.getText()
            amt = amt.replace('$', '')
            amt = float(amt)

            # Increment the totals
            numOrders += 1
            runningTotal += amt
            amounts.append(runningTotal)
            
    print('\nYou spent ${} over {} orders'.format(runningTotal, numOrders))
    
    # Reverse the order of the dates
    # FCP data has the most recent orders at the top of the HTML page
    # No need to reverse amounts, since itsa running total
    dates_matplot.reverse()
    
    # Plot the 2 data series
    plt.plot_date(dates_matplot,amounts)
    plt.show()


main()
