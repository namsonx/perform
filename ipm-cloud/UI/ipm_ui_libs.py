
from selenium import webdriver
from time import sleep
from ipm_libs import get_number_of_parking_place, get_parking_place_info, get_tenant_id, get_all_vehicle_of_tenant,\
                        get_all_tenant_of_place



def open_page_and_login(serverIp, port='50202', username = 'anand', passwd = 'anand'):
    
    url = 'http://' + serverIp + ':' + port
    #driver = webdriver.Firefox()
    #options = webdriver.ChromeOptions()
    #options.add_argument("--start-maximized")
    driver = webdriver.Chrome()
    #driver.set_window_size(1920, 1080)
    driver.maximize_window()
    
    driver.implicitly_wait(30)
    
    driver.get(url)
    login_user = driver.find_element_by_id('login-username')
    login_user.clear()
    sleep(3)
    login_user.send_keys(username)
    sleep(2)
    login_pw = driver.find_element_by_id('login-password')
    login_pw.clear()
    sleep(3)
    login_pw.send_keys(passwd)
    sleep(2)
    
    driver.find_element_by_id('submit-button').submit()
    sleep(5)
    title = driver.title
    print 'Title list is: ', title
    if title!='DashBoard | IPM 1.0':
        raise ValueError('Login failed')
    return driver

def open_parking_place(serverIp, port='50202'):
    driver = open_page_and_login(serverIp, port)
    driver.find_element_by_css_selector('a[ng-click="showInnerMenu(2)"]').click()
    sleep(2)
    driver.find_element_by_css_selector('a[ui-sref="dashBoard.manageParkingPlace"]').click()
    sleep(2)
    numIntable = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'The number of parking place is: ', numIntable
    numOfPlaces = get_number_of_parking_place(serverIp)
    if numIntable!=numOfPlaces:
        raise ValueError('The number of parking places showing on UI and in database are mis-matched')
    
    return driver
    
def view_parking_place_detail(serverIp, port, placeName):
    
    driver = open_page_and_login(serverIp, port)
    parkingPlace = get_parking_place_info(serverIp, placeName)
    href = '#/dashBoard/createBlockSlots/' + str(parkingPlace.id) + '?placeName=' + placeName + '&parkType=2&autoExit=N'
    print 'href is: ', href
    selector = 'button[href=\"%s\"]' %href
    driver.find_element_by_css_selector(selector).click()
    #driver.find_element_by_css_selector('button[href="#/dashBoard/createBlockSlots/135?placeName=tenant-test&parkType=2&autoExit=N"]').click()
    sleep(2)
    return driver, parkingPlace

def view_tenant_management(serverIp, port, placeName):
    driver, parkingPlace = view_parking_place_detail(serverIp, port, placeName)
    href = '#/dashBoard/manageTenants/' + str(parkingPlace.id) + '?placeName=' + placeName
    print 'href is: ', href
    selector = 'button[href=\"%s\"]' %href
    driver.find_element_by_css_selector(selector).click()
    sleep(3)
    if 'Manage Tenants' in driver.page_source:
        return driver
    else:
        raise ValueError('Cannot open Manage Tenants page')
    
def create_new_tenant_ui(serverIp, port, placeName, name):
    driver = view_tenant_management(serverIp, port, placeName)
    driver.find_element_by_css_selector('button[ng-click="createTenant(\'NEWTENANT\')"]').click()
    sleep(2)
    tenantName = driver.find_element_by_css_selector('input[ng-model="tenantDetails.tenantName"]')
    tenantName.clear()
    sleep(2)
    tenantName.send_keys(name)
    sleep(2)
    driver.find_element_by_css_selector('button[ng-click="submitParkingTenant()"]').click()
    sleep(2)
    
    numOfTenant = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    i=1
    check = 0
    while i<=numOfTenant:
        xpath = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/span/b' %(i, 1)
        tena = driver.find_elements_by_xpath(xpath)
        print 'check is: ', tena[0].text
        if name==tena[0].text:
            check = check+1
            break
        i = i+1
    if check==0:
        raise ValueError('Cannot create new tenant via UI')
    else:
        return driver
    
def show_tenant_prices(serverIp, uiport, placeName, tenantName):
    driver = view_tenant_management(serverIp, uiport, placeName)
    numOfTenant = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'numOfTenant is: ', numOfTenant
    i=1
    while i<=numOfTenant:
        xpathName = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/span/b' %(i, 1)
        tena = driver.find_elements_by_xpath(xpathName)
        if tenantName==tena[0].text:
            print 'Started viewing tenant prices'
            xpathPrices = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/a' %(i, 3)
            prices = driver.find_elements_by_xpath(xpathPrices)
            prices[0].click()
            sleep(2)
            text = driver.find_elements_by_xpath('//h3[@class="modal-title"]')[0].text
            if 'Tenant Prices' not in text:
                errMessage = 'Cannot show prices of tenant %s' %tenantName
                raise ValueError(errMessage)
        i = i+1
            
    driver.close()
    
def edit_tenant_name_via_ui(serverIp, uiport, port, placeName, oldName, newName):
    driver = view_tenant_management(serverIp, uiport, placeName)
    numOfTenant = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'numOfTenant is: ', numOfTenant
    i=1
    while i<=numOfTenant:
        xpathName = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/span/b' %(i, 1)
        tena = driver.find_elements_by_xpath(xpathName)
        if oldName==tena[0].text:
            print 'Started viewing tenant prices'
            xpathEdit = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/a' %(i, 5)
            editTenant = driver.find_elements_by_xpath(xpathEdit)
            editTenant[0].click()
            sleep(2)
            text = driver.find_elements_by_xpath('//h3[@class="modal-title ng-binding"]')[0].text
            if 'Edit Tenant Details For:' not in text:
                errMessage = 'Cannot click on Edit button for tenant %s' %oldName
                raise ValueError(errMessage)
            tenantName = driver.find_element_by_css_selector('input[ng-model="tenantDetails.tenantName"]')
            tenantName.clear()
            sleep(2)
            tenantName.send_keys(newName)
            sleep(2)
            driver.find_element_by_css_selector('button[ng-click="submitParkingTenant()"]').click()
            sleep(3)
        i = i+1
    tenantList = get_all_tenant_of_place(serverIp, port, placeName)
    tenantNamesList = []
    for tenant in tenantList:
        tenantNamesList.append(tenant['tenantName'])
        
    print 'List tenant name: ', tenantNamesList
    if (newName in tenantNamesList) and (oldName not in tenantNamesList):
        print 'Edit tenant Name successful'
    else:
        errMessage = 'Cannot update tenant name from %s to %s' %(oldName, newName)
        raise ValueError(errMessage)
    
    driver.close()
            
def add_vehicle_to_tenant_ui(serverIp, uiport, port, placeName, tenantName, vehList):
    driver = view_tenant_management(serverIp, uiport, placeName)
    numOfTenant = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'numOfTenant is: ', numOfTenant
    i=1
    while i<=numOfTenant:
        print 'adding vehicles to tenant'
        xpathName = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/span/b' %(i, 1)
        tena = driver.find_elements_by_xpath(xpathName)
        if tenantName==tena[0].text:
            print 'Started adding to tenent: ', tena[0].text
            xpathAddVeh = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/a' %(i, 4)
            addVeh = driver.find_elements_by_xpath(xpathAddVeh)
            addVeh[0].click()
            sleep(2)
            for veh in vehList:
                driver.find_element_by_css_selector('button[ng-click="createUpdateTenantVehicle(\'NEWVEHICLE\',tenantVehicleDetails)"]').click()
                sleep(2)
                tenantVeh = driver.find_element_by_css_selector('input[ng-model="tenantVehicle.vehicleNumber"]')
                tenantVeh.clear()
                sleep(2)
                tenantVeh.send_keys(veh.vehicleNo)
                sleep(2)
                driver.find_element_by_css_selector('span[class="ui-select-match-text pull-left"]').click()
                vehType = driver.find_element_by_css_selector('input[placeholder="Select Vehicle type"]')
                vehType.clear()
                sleep(2)
                if veh.vehicleType==2:
                    print 'vehicleType is Two Wheeler'
                    typeOfVeh = '//li[@class="ui-select-choices-group"]/div/a/div[text()="Two Wheeler "]'
                    vehicleType = driver.find_elements_by_xpath(typeOfVeh)
                    print len(vehicleType)
                    vehicleType[0].click()
                if veh.vehicleType==3:
                    print 'vehicleType is Three Wheeler'
                    typeOfVeh = '//li[@class="ui-select-choices-group"]/div/a/div[text()="Three Wheeler "]'
                    vehicleType = driver.find_elements_by_xpath(typeOfVeh)
                    print len(vehicleType)
                    vehicleType[0].click()
                if veh.vehicleType==4:
                    print 'vehicleType is Four Wheeler'
                    typeOfVeh = '//li[@class="ui-select-choices-group"]/div/a/div[text()="Four Wheeler"]'
                    vehicleType = driver.find_elements_by_xpath(typeOfVeh)
                    print len(vehicleType)
                    vehicleType[0].click()
                if veh.vehicleType==6:
                    print 'vehicleType is Six Wheeler'
                    typeOfVeh = '//li[@class="ui-select-choices-group"]/div/a/div[text()="Six Wheeler"]'
                    vehicleType = driver.find_elements_by_xpath(typeOfVeh)
                    print len(vehicleType)
                    vehicleType[0].click()
                sleep(2)
                driver.find_element_by_css_selector('button[ng-click="addVehicle()"]').click()
                sleep(2)
        i=i+1
    tenantId = get_tenant_id(serverIp, placeName, tenantName)
    vehsTenant = get_all_vehicle_of_tenant(serverIp, port, tenantId)
    vehNoList = []
    for veh in vehsTenant:
        vehNoList.append(veh['vehicleNumber'])
        
    for veh in vehList:
        if veh.vehicleNo not in vehNoList:
            errMessage = 'Cannot add vehicle No %s with vehicle type %s in to tenant %s' %(veh.vehicleNo, veh.vehicleType, tenantName)
            raise ValueError(errMessage)
    sleep(3)
    driver.close()
    
def delete_veh_in_tenant_ui(serverIp, port, uiport, placeName, tenantName, number):
    tenantId = get_tenant_id(serverIp, placeName, tenantName)
    vehList = get_all_vehicle_of_tenant(serverIp, port, tenantId)
    if number>len(vehList):
        errMessage = 'The number of vehicle going to delete (%s) are greater than total vehicles in tenant (%s)' %(number, len(vehList))
        raise ValueError(errMessage)
    driver = view_tenant_management(serverIp, uiport, placeName)
    numOfTenant = len(driver.find_elements_by_xpath("//table[@class='table table-hover']/tbody/tr"))
    print 'numOfTenant is: ', numOfTenant
    i=1
    while i<=numOfTenant:
        print 'adding vehicles to tenant'
        xpathName = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/span/b' %(i, 1)
        tena = driver.find_elements_by_xpath(xpathName)
        if tenantName==tena[0].text:
            print 'Started adding to tenent: ', tena[0].text
            xpathAddVeh = '//table[@class="table table-hover"]/tbody/tr[%s]/td/div[%s]/a' %(i, 4)
            addVeh = driver.find_elements_by_xpath(xpathAddVeh)
            addVeh[0].click()
            sleep(2)
            count = 1
            while count<=number:
                driver.find_element_by_css_selector('button[ng-click="deleteVehicle(vehicle,$item)"]').click()
                count = count + 1
                sleep(2)
        i = i+1        
     
    driver.close()    
    
def title_should_be(driver, title):
    print driver.title
    if driver.title==title:
        print 'Title is matched. Test successes'
    else:
        raise ValueError('The title is not matching')
    
def close_driver_session(driver):
    driver.close()