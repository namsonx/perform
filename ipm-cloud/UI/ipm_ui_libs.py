from selenium import webdriver
from time import sleep



def open_page_and_login(username, passwd, url='http://192.168.0.229:50202'):
    
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    
    driver.get(url)
    login_user = driver.find_element_by_id('login-username')
    login_user.clear()
    login_user.send_keys(username)
    sleep(2)
    login_pw = driver.find_element_by_id('login-password')
    login_pw.clear()
    login_pw.send_keys(passwd)
    sleep(2)
    
    driver.find_element_by_id('submit-button').submit()
    sleep(2)
    title = driver.title
    print 'Title list is: ', title
    
    return driver
    
def title_should_be(driver, title):
    print driver.title
    if driver.title==title:
        print 'Test successes'
    else:
        print 'Test failed'