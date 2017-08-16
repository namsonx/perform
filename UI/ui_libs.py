
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

def open_page(page_url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    #driver.maximize_window()
    
    driver.get(page_url)
    
    login_user = driver.find_element_by_id('username')
    login_user.clear()
    login_user.send_keys('Adminuser')
    sleep(2)
    login_pw = driver.find_element_by_id('password')
    login_pw.clear()
    login_pw.send_keys('Admin@123456')
    sleep(2)
    driver.find_element_by_id('loginBtn').click()
    
    
    search_box = driver.find_element_by_id('vehicleNoId')
    search_box.clear()
    search_box.send_keys('KA99MS')
    sleep(2)
    driver.find_element_by_id('btnVehicleNo').click()
    
    lists= driver.find_elements_by_class_name('table dataTable table-striped table-bordered')
    
    for item in lists:
        print 'Test search fucntion: ', item
        
    print 'Number of items in search result is: ', len(lists)
    