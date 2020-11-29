# 1) pip install selenium
# 2) Download ChromeDriver from https://chromedriver.chromium.org/
# 3) Put above folder PATH into the main() code at very bottom
#
#  Update:  They changed the XPath.  Right click->Inspect->Copy->XPath
#           
#

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def typeGame(driver):
    URL = 'https://play.typeracer.com/'
    driver.get(URL)
    time.sleep(5)
    
    # Click start game
    #driver.find_element_by_xpath('//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a').click()
    driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[1]/div[2]/table/tbody/tr[2]/td[2]/div/div[1]/div/div[1]/div/a').click()
    
    time.sleep(5)
    
    # Get the msg to be typed
    #msg = driver.find_element_by_xpath('//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]').text
    Xp = '//*[@id="gwt-uid-17"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span['
    msg2 = ''
    spans = []
    
    # Try to process 5 spans, at most.  
    # They change the number of spans to thwart bots!
    # Try block will crash
    # Append each span into a list
    # I can't concat in real time, since one will be missing a space at the end
    for i in range(1,5):
        try:
            currXP = Xp + str(i) + ']'
            elem = driver.find_element_by_xpath(currXP)
            spans.append(elem.text)
        except:
            maxSpan = i
            break

    print(spans)
    
    # Assemble the message, and add the missing space 
    # If there are 3 spans, maxSpan crashed the try() at 4
    # and it needs a space after span 2, hence 4-2
    for l in range(1,maxSpan):
        msg2 += spans[l-1]    
        if (l == maxSpan-2):
            msg2 += ' '
            
    print('Full2:' + msg2)
    
    # Wait for the "Here" message to signify the race has started
    element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'arrowPopupText')))
    
    # Type each letter in the message 
    for letter in msg2:
        driver.find_element_by_class_name('txtInput').send_keys(letter)
        #time.sleep(.03)
     
    
def main():
    #driver = webdriver.Chrome()
    driver = webdriver.Chrome(executable_path=r"C:\Users\sidds.DESKTOP-N255TP6\Documents\install\chromedriver_win32\chromedriver.exe")
    driver.maximize_window()
    
    typeGame(driver)
    
main()
