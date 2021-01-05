from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twilio.rest import Client
import time

numbers = {
    #'Lenore': '+16043172568',
    'Nima': '+17787727966'
}

time_inp = input('input time in the following format "7 AM to 9 AM": ')
date_row = input('input the row of the date (1,2,3...): ')
date_col = input('input the column of the date (1,2,3...): ')
location = input('input the location (van, nv, surrey, poco): ')
wait_time = int(input('how long to wait in between each check (in seconds): '))
twilio_auth_token = input('input twilio auth token: ')

## initialize twilio client
client = Client("ACd9f208c4fad6c91d977d7390e939ecb7", twilio_auth_token)

## set path for chrome driver
driver = webdriver.Chrome('D:\Downloads\Chrome Downloads\chromedriver_win32\chromedriver.exe')

if location == 'nv':
    url = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=78c7ab47bbe04fa59fe0a4889f4cda4c&random=5ff26b8aef25f&iframeid=&mode=p'
elif location == 'van':
    url = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=2224a8b95d0e4ca7bf20012ec34b8f3e&random=5ff3a9ca735be&iframeid=&mode=p'
elif location == 'poco':
    url = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=f58be9a9b7c34483a967a1de9dfd4e1e&random=5f985a0916f1c&iframeid=&mode=p'
else:
    url = 'https://app.rockgympro.com/b/widget/?a=list&&widget_guid=69837a02c2bf47e88cf423cf066997e1&random=5ff3a9f3686af&iframeid=&mode=p'

driver.get(url)

## clicks on the Information and Booking button
driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/div[1]/fieldset/div/a').click()

def find_availability():
    
    ## Initialize the result of this function to be false
    result = False
    
    ## this will pick the date in the calendar based on row tr[2] and column tr[2] respectively
    ## TODO: find a better way to choose and click the date in the table
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="start_date_calendar"]/div/table/tbody/tr[' + date_row + ']/td[' + date_col + ']')))
    driver.find_element_by_xpath('//*[@id="start_date_calendar"]/div/table/tbody/tr[' + date_row + ']/td[' + date_col + ']').click()

    ## wait until the new date page loads before grabbing the availability data
    time.sleep(10)

    content = driver.find_element_by_id('offering-page-select-events-table')
    lines = iter(content.text.splitlines())
    
    for line in zip(lines, lines):
        line_text = " ".join(line)

        if time_inp in line_text and 'Available Select' in line_text:
            ## If input date string is found and it is Available then return true
            result = True
        else:
            continue
    
    return result

## keep trying the find_availability function until it returns True
while not find_availability():
    print('Checking availability...')
    find_availability()
    time.sleep(wait_time)
    driver.refresh()
    
# send me a text message
for name, number in numbers.items():
    try:    
        client.messages.create(to=number, 
                        from_="+12515773195", 
                        body="Yo " + name + "your" + time_inp " reservation at the hive" +  location + "is open " + url)
        print('sms sent successfully')
    except:
        print('could not send sms')
        raise
