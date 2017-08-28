
from selenium import webdriver
from time import sleep
from ipm_libs import get_number_of_parking_place



def open_page_and_login(username, passwd, url='http://192.168.0.229:50202'):
    
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    
    driver.get(url)
    login_user = driver.find_element_by_id('login-username')
    login_user.clear()
    sleep(1)
    login_user.send_keys(username)
    sleep(2)
    login_pw = driver.find_element_by_id('login-password')
    login_pw.clear()
    sleep(1)
    login_pw.send_keys(passwd)
    sleep(2)
    
    driver.find_element_by_id('submit-button').submit()
    sleep(2)
    title = driver.title
    print 'Title list is: ', title
    
    return driver

def open_parking_place(serverIp, driver):
        
    driver.find_element_by_css_selector('a[ng-click="showInnerMenu(2)"]').click()
    sleep(2)
    driver.find_element_by_css_selector('a[ui-sref="dashBoard.manageParkingPlace"]').click()
    sleep(2)
    numIntable = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'The number of parking place is: ', numIntable
    numOfPlaces = get_number_of_parking_place(serverIp)
    if numIntable!=numOfPlaces:
        raise ValueError('The number of parking places showing on UI and in database are mis-matched')

def title_should_be(driver, title):
    print driver.title
    if driver.title==title:
        print 'Title is matched. Test successes'
    else:
        raise ValueError('The title is not matching')