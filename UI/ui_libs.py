
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def open_page(page_url):
    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.maximize_window()
    
    driver.get(page_url)
    
    search_box = driver.find_element_by_id('vehicleNoId')
    search_box.clear()
    search_box.send_keys('KA99MS')
    search_box.submit()
    
    lists= driver.find_elements_by_class_name('row search table-result')
    
    for item in lists:
        print 'Test search fucntion: ', item
        
    print 'Number of items in search result is: ', len(lists)
    