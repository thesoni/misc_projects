# The HTML table data with the order amounts looks like:
# <td data-label="Total">$177.81</td>

import sys
import bs4

if (len(sys.argv) != 2):
    sys.exit("Usage: python fcp.py FILENAME.html")

file = open(sys.argv[1])
soup = bs4.BeautifulSoup(file, features='html.parser')
elems = soup.select('td')

numOrders = 0
totalCost = 0

for e in elems:
    attr = e.get('data-label')
    if attr == 'Total':
        amt = e.getText()
        amt = amt.replace('$', '')
        amt = float(amt)
        numOrders += 1
        totalCost += amt

print('You spent ${} over {} orders'.format(totalCost, numOrders))