"""Module to automatically test Vizit."""
# import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display

# display = Display(visible=0, size=(800,600))
# display.start()

# selenium.minimizeWindow()
driver = webdriver.Firefox()

driver.get("http://tsethaskew.me/csc/")

inputtxt = driver.find_element_by_name("inputtxt")
inputtxt.send_keys("1,2,3,4,5")
inputtxt.send_keys(Keys.RETURN)
