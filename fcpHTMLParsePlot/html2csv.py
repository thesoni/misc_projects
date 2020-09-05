# The HTML table data with the order amounts looks like:
# <td data-label="Total">$177.81</td>

import sys
import bs4
import os
import datetime as dt

def reformatDate(d):
    date_time_obj = dt.datetime.strptime(d, '%b %d, %Y')
    return date_time_obj.date()

def main(): 

    if (len(sys.argv) != 2):
        sys.exit("Usage: python orders.py FILENAME.html")

    # Generate the output CSV filename to match the input file
    # fcp.html becomes fcp.csv
    #
    cwd = os.getcwd()
    infilename = os.path.basename(sys.argv[1])
    basefile = infilename.split('.')
    outfile = cwd + '/' + basefile[0] + ".csv"
    csvFile = open(outfile, "w")

    # Pass the HTML file to BS4
    file = open(sys.argv[1])
    soup = bs4.BeautifulSoup(file, features='html.parser')
    elems = soup.select('td')

    numOrders = 0
    totalCost = 0
    
    dates = []
    amts = []
    
    #Parse the tags in the HTML file
    for e in elems:
        attr = e.get('data-label')
        if attr == 'Date':
            date = e.getText()
            date = reformatDate(date)
            dates.append(date)
        if attr == 'Total':
            amt = e.getText()
            amt = amt.replace('$', '')
            amt = float(amt)
            numOrders += 1
            totalCost += amt
            amts.append(amt)
            #data = str(date) + ',' + str(amt) + '\n'
            #csvFile.write(data)

    print('You spent ${} over {} orders'.format(totalCost, numOrders))
    
    # Reverse the order of the rows
    # FCP data has the most recent orders at the top of the HTML page
    dates.reverse()
    amts.reverse()

    # Iterate through the 2 lists, and print the combined record data to a CSV file
    for i in range(len(dates)):
        data = str(dates[i]) + ',' + str(amts[i]) + '\n'
        csvFile.write(data)
    
    csvFile.close()

main()