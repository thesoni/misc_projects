# GREEDY REGEX is default
# NON_GREEDY has "?" at the end of pattern

import re

def testRegEx(text, pattern):
    
    regex = re.compile(pattern)
    
    res = regex.findall(text)
    for r in res:
        print(r)

def searchForWords():
    text = '110k miles'
    pattern = ('miles|mile|mileage|TMU')
    regex = re.compile(pattern) 
    res = regex.search(text)
    print(res)


def main():

    text = 'moocow12moocow2moocow3'
    nongreedy = r'cow[\w]+?'
    greedy = r'cow[\w]+'
    
    testRegEx(text, greedy)
    testRegEx(text, nongreedy)
    
    searchForWords()
    
main()
