from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
import time

numbers = {
    'Lenore': '+16043172568'
}


vancouver = '//*[@id="sm-16097219725622068-10"]/li[1]/a'
north_vancouver = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=78c7ab47bbe04fa59fe0a4889f4cda4c&random=5ff26b8aef25f&iframeid=&mode=p'
surrey = '//*[@id="sm-16097219725622068-10"]/li[3]/a'
poco = '//*[@id="sm-16097219725622068-10"]/li[4]/a'

driver = webdriver.Chrome('D:\Downloads\Chrome Downloads\chromedriver_win32\chromedriver.exe')

driver.get(north_vancouver)

client = Client("ACd9f208c4fad6c91d977d7390e939ecb7", "61924b6ecce8f4cd2697ddcb0f41df0f")

driver.find_element_by_xpath('//*[@id="booking_offering_list_7609fc060ca04696b291d58b7b10fd21"]/fieldset/div/a').click()

# keep refreshing until the add to cart button appears
def clickButton():
    try:
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="start_date_calendar"]/div/table/tbody/tr[2]/td[2]')))
        driver.find_element_by_xpath('//*[@id="start_date_calendar"]/div/table/tbody/tr[2]/td[2]').click()
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH,'//*[@id="offering-page-select-events-table"]/tbody/tr[12]/td[4]/a')))
        driver.find_element_by_xpath('//*[@id="offering-page-select-events-table"]/tbody/tr[12]/td[4]/a').click()
        return True
    except Exception:
        print('Not Available... Retrying')
        time.sleep(600)
        driver.refresh()
        return False
    
while not clickButton():
    clickButton()

# send me a text message
for name, number in numbers.items():
    try:    client.messages.create(to=number, 
                        from_="+12515773195", 
                        body="Yo " + name +  " reservation at the hive is open " + north_vancouver)
    except:
        print('Could not send sms')
        raise
    