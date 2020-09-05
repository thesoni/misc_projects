import os
import time
import re
import requests
from selenium import webdriver
import sys
import bs4
import random 

#
#   Set the topURL and logFile.txt at the very bottom
#
#
# https://regex101.com/    
#
# <h3 class="auctions-item-title"><a href="https://bringatrailer.com/listing/1977-porsche-911s-29/">Modified 1977 Porsche 911S</a></h3>
# https:\/\/bringatrailer.com\/listing\/1983-porsche-911sc-coupe\/
# Get main BAT results plot page
# Parse each link to a car
# Get each HTML page and parse out dat, miles, year, price.

###########################################################
# HOW TO EXTRACT DATA USING BS4 
#
# <h3 class="FOO1">
#    <a href="http://google.com/">FOO2</a>
# </h3>
#
# link = soup.find('h3', class_='FOO1')
# link = link.find('a')
# link = link.get('href')
#
###########################################################

# Download the HTML page 
def getPage(url):
    response = requests.get(url)
    return response.text
    
# Process the Regex to get all URLs from HTML
# https:\/\/bringatrailer.com\/listing\/1983-porsche-911sc-coupe\/
def getLinks(pattern, text):
    
    links = []
    
    regex = re.compile(pattern)

    # Remove escape chars to make valid URL
    # Add URLs to lsit
    for link in regex.findall(text):
        link = link.replace('\\','')    
        links.append(link)

    #remove duplicates
    links = list(dict.fromkeys(links))
    
    return links

# '<span class="hide-mobile-inline"><span class="data-label">Sold For</span> <span class="data-value">$75,100</span> <span class="data-label">On</span> <span class="data-value">7/8/15</span></span><span class="show-mobile-inline"><span class="data-value">$75,100</span> <span class="data-sep"></span> <span class="data-value">Sold</span></span>'
def parseCarHTML(url):
    
    html = getPage(url)
    soup = bs4.BeautifulSoup(html, features='html.parser')
    
    #get year (directly from URL)
    pattern = '\d\d\d\d'
    regex = re.compile(pattern)
    year = regex.findall(url)
    
    # program crashed on an ad with no year (engine only)
    try:
        year = str(year[0])
        #print('year = ' + year)
    except:
        year = "N/A"
    
    #get price
    spans = soup.find_all('span', class_='data-value')
    price = spans[0].text
    listingDate = spans[1].text
    #print('price = ' + price)
     
    # get title
    # <meta property="og:title" content="1977 Porsche 911S Targa 3.2L"/>
    # Soup4:  Find the tag.  Get the attribute
    metaTag = soup.find('meta', property='og:title')
    title = metaTag.get('content')
    #print('title = ' + title)
    
    # get mileage
    # <li class="listing-essentials-item">123k Miles Shown</li>
    liTags = soup.find_all('li', class_='listing-essentials-item')
    pattern = ('Miles|miles|Mile|mile|Mileage|mileage|TMU|Shown|Kilometers|Indicated')

    # reset mileage outside the loop
    # since the mileage tag is not the LAST tag in the list
    # so it can get reset back to "not given" after being found
    mileage = "Mileage not given"    
    
    for li in liTags:

        info = li.text

        regex = re.compile(pattern) 
        res = regex.search(info)
        if (res):
            #print(info)
            mileage = info

    msg = listingDate + '|' + year + '|' + price + '|' + mileage + '|' + title + '|' + url + '\n'
    #print(msg)
    return msg
    
# <div class="chart" data-stats="......................."
def getChartData(html):
    soup = bs4.BeautifulSoup(html, features='html.parser')
    div = soup.find('div', class_='chart')
    data = div.get('data-stats')
    return data       

def logData(logFile, data):
    f = open(logFile, "a")
    f.write(data)
    f.close()

def loadCars(logfile):
    try:
        file = open(logfile,"r")
        cars = file.read()
    except:
        cars = ""

    return cars


def main():
    topURL = 'https://bringatrailer.com/porsche/impact-bumper-911/'
    pattern = r'https:\\\/\\\/bringatrailer.com\\\/listing\\\/[\w-]+\\\/'
    logFile = '911.txt'

    currentList = loadCars(logFile)
    #print(currentList)                    
    #sys.exit()
    
    html = getPage(topURL)
    data = getChartData(html)
    
    links = getLinks(pattern, data)
    
    #carURL = 'https://bringatrailer.com/listing/1977-porsche-911s-29/'
    #data = parseCarHTML(carURL)
    #sys.exit(data)
    
    # iterate thru all cars
    # pause on each iteration, to avoid getting bot IP blocked.
    carNum = 0
    
    for link in links:
        #print(link)
        if (currentList.find(link) != -1):
            print ("already in DB: " + link)
            continue
        
        data = parseCarHTML(link)
        carNum += 1
        print(str(carNum) + "-->" + data)
        logData(logFile, data)
        pause = random.randint(1,3)
        #time.sleep(pause)
        
main()