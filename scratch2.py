from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
import time

driver = webdriver.Chrome('D:\Downloads\Chrome Downloads\chromedriver_win32\chromedriver.exe')

url = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=78c7ab47bbe04fa59fe0a4889f4cda4c&random=5ff26b8aef25f&iframeid=&mode=p'

driver.get(url)

driver.find_element_by_xpath('//*[@id="booking_offering_list_7609fc060ca04696b291d58b7b10fd21"]/fieldset/div/a').click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,'ui-state-default')))
content = driver.find_element_by_css_selector('a.ui-state-default')

#for day in content:
#    print(day.text, day.get_attribute("value"))


attrs = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', content)
print(attrs)