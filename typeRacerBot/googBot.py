from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# load browser
driver = webdriver.Chrome(executable_path=r'C:\Users\ssoni\Documents\installs\chromedriver_win32\chromedriver.exe')

# navigate to chosen website
driver.get("http://www.google.com")

# enter text into search box
driver.find_element_by_name('q').send_keys('cat')

# click button
#driver.find_element_by_name('btnK').click()
driver.find_element_by_name('q').send_keys(Keys.ENTER)





