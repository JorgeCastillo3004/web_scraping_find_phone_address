from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import chromedriver_autoinstaller

import pandas as pd
import random
import json
import time
import re
import os
from datetime import date
################## IMPORT MODULES ##################
from database import *
import linecache
import sys
from database import *
#########################################################################################
#                                   BLOCK DEPURATE CODE                                 #
######################################################################################### 
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print ('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

#########################################################################################
#                                                                                       #
#                SECTION FOR SAVE AND LOAD CHECK POINTS                                 #
#                                                                                       #
#########################################################################################
def saveCheckPoint(filename, dictionary):
    json_object = json.dumps(dictionary, indent=4)
    with open(filename, "w") as outfile:
        outfile.write(json_object)

def load_check_point(filename):
    # Opening JSON file
    if os.path.isfile(filename):
        with open(filename, 'r') as openfile:        
            json_object = json.load(openfile)
    else:
        json_object = {}
    return json_object

def search_check_points(filepath, check_point_filename = 'check_points/last_row.json'):
    file_name = filepath.split('/')[-1]
    previous_run_flag = False
    if not os.path.isfile(check_point_filename):
        last_row_dict = {}
        row_number = 0      
    else:
        last_row_dict = load_check_point(check_point_filename)
        try:
            last_row = last_row_dict[file_name]['last_row']
            row_number = last_row + 1
            previous_run_flag = True
        except:
            previous_run_flag = False
            row_number = 0
    return previous_run_flag, last_row_dict, row_number

#########################################################################################
#                                                                                       #
#                                   MAIN FUNCTINS                                       #
#                                                                                       #
#########################################################################################

def load_file(file_name):
    """Function to load last file generated"""
    if os.path.isfile(file_name):
        df_all = pd.read_csv(file_name)
    else:
        df_all = pd.DataFrame()
    return df_all

def wait_search_box(max_try = 15):
    wait_search_box_found = False
    flag_wait = True
    count = 0
    while flag_wait:
        try:
            input_name = driver.find_element(By.ID, 'search-name-name')
            flag_wait = False
            time.sleep(random.uniform(0.5, 3))
            wait_search_box_found = True
        except:
            time.sleep(random.uniform(0.3, 0.8))
            count +=1
            print("-W-SBX-", end='')
            if count ==  max_try:
                flag_wait = False                
    
    return wait_search_box_found

def wait_results(max_try = 15):
    flag_wait = True
    count = 0
    while flag_wait:
        try:
            card_blocks = driver.find_elements(By.CLASS_NAME, 'card-block')
            flag_wait = False
            time.sleep(random.uniform(0.3, 1))
        except:
            time.sleep(random.uniform(0.3, 0.8))
            count +=1
            print('-wr-', end='')
            if count ==  max_try:
                flag_wait = False
                print("Sent alert of connection or CAPTCHA")

def SelectSearch(by_name = True, max_try = 15):
    flag_wait = True
    count = 0
    while flag_wait:
        try:
            if by_name:
                class_search = 'search-nav-link-name'
            else:
                class_search = 'search-nav-link-address'

            searchbyaddress = driver.find_element(By.ID,class_search)
            searchbyaddress.click()
            flag_wait = False
        except:
            count +=1
            time.sleep(1)
            if count == max_try:
                flag_wait = False                

def sendSearch(name, address):
    wait = WebDriverWait(driver, 10)
    free_search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-form-button-submit.btn.btn-md.btn-primary')))
    input_name = driver.find_element(By.ID, 'search-name-name')
    input_name.clear()
    for character in name:
        input_name.send_keys(character)
        time.sleep(random.uniform(0.1,0.2))


    input_address = driver.find_element(By.ID, 'search-name-address')
    input_address.clear()
    for character in address:
        input_address.send_keys(character)
        time.sleep(random.uniform(0.1,0.2))

    # free_search  = driver.find_element(By.CLASS_NAME, 'search-form-button-submit.btn.btn-md.btn-primary')

    time.sleep(random.uniform(0.5,1.2))
    free_search.click()

def imitateBehavior(max_tries = 10):
    randcount = random.randint(2, max_tries)

    for count in range (0, randcount):
        rand_option = random.randint(0,1)
        if rand_option ==0:
            webdriver.ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        else: 
            webdriver.ActionChains(driver).send_keys(Keys.PAGE_UP).perform()
        time.sleep(random.uniform(0.2, 0.2))

def backWaitSearchBox(max_try= 5):
    wait_search_box_found = False

    while not wait_search_box_found:

        wait_search_box_found = wait_search_box(max_try = max_try)
        if wait_search_box_found:
            print("Continue search: ")
        else:
            driver.back()
            wait_search_box_found = wait_search_box(max_try = max_try)
#########################################################################################
#                                   BLOCK GET DATA                                      #
######################################################################################### 
def get_address(card_block):
    listdivs = card_block.find_elements(By.CSS_SELECTOR, 'div')
    dict_old_address = {}
    main_address = 'unfound'
    for count, div in enumerate(listdivs):
        if count ==0:            
            main_address = div.text.replace('\n',' ')
        if count ==1:            
            old_address = div.find_elements(By.CSS_SELECTOR, 'div')
            list_old_address = []
            for i, old_ in enumerate(old_address):
                # list_old_address.append(old_.text.replace('\n',' ')) 
                dict_old_address[i] = old_.text.replace('\n',' ')
            break   
    return {'main_address': main_address, 'past_address':dict_old_address}

def get_name_age(card_block):    
    HTML = card_block.get_attribute('outerHTML')
    name, age = 'unfound','unfound'
    if 'Full Name:' in HTML:
        name = re.findall(r'<h3>Full Name:</h3>(.+)<br',HTML)[0]
        name = ' '.join(name.split())
    else:
        name_address_list = card_block.find_element(By.CLASS_NAME, 'card-title')
        name = name_address_list.find_element(By.CLASS_NAME, 'larger').text
    if 'Age:' in HTML:
        age = re.findall(r'<h3>Age:</h3>(.+)<br',HTML)[0]
        age = ' '.join(age.split())
    return name, age    

def get_phone_numbers(card_block):
    phones_numbers = card_block.find_elements(By.CLASS_NAME, 'nowrap')
    count = 0    
    primary_phone = 'unfound'
    dict_phones = {}
    for phone_number in phones_numbers:
        HTML = phone_number.get_attribute('outerHTML')
        if 'phone number' in HTML:
            if count == 0:
                primary_phone = phone_number.text
            else:
                dict_phones[count -1] = phone_number.text
            count +=1
    return {'primary_phone':primary_phone, 'list_phones':dict_phones}

def get_block_results(df_all, selected_file):

    global all_info, name_search, address_search, dbase

    card_blocks = driver.find_elements(By.CLASS_NAME, 'card-block')
    dict_register = {}
    dict_register['search_name'] = name_search
    dict_register['search_address'] = address_search
    dict_partial_info = {}

    if len(card_blocks)== 0:
        print("Unfound registers")

    for card_block in card_blocks:
        name, age = get_name_age(card_block)        
        dict_register['name'] = name
        dict_register['age'] = age

        dict_phones = get_phone_numbers(card_block)
        dict_register.update(dict_phones)

        dict_address = get_address(card_block)
        dict_register.update(dict_address)

        dict_register['status'] = 'found'
        # = ['name','primary_phone','list_phones','main_address','past_address','status']
        for i in dict_register.keys():
            dict_partial_info[i] = [str(dict_register[i])]
        
        insertNewRegister(dbase, dict_register, selected_file.split('/')[-1])

        df = pd.DataFrame.from_dict(dict_partial_info)        
        df_all = pd.concat([df_all, df])       
    
    return df_all

def nextPage(max_try = 2):
    flag_click_next = True
    count = 0
    while flag_click_next:
        try:
            flag_continue = True
            nextbuttons = driver.find_element(By.CLASS_NAME,'pagination-links')
            paginations = nextbuttons.find_elements(by.CLASS_NAME, 'btn')

            for button in paginations:
                if "NEXT PAGE" in button.tex:
                    button.click()
                    break
                if len(paginations)==1 and 'PREVIOUS PAGE' in button.text:
                     flag_continue = False
            flag_click_next = False
        except:
            count +=1
            if count == max_try:
                flag_click_next = False
                flag_continue = False
            time.sleep(1)
    return flag_continue

def detectCatpcha(max_try = 2):
    CatpchaDetected = False
    try_find_captcha = True
    count = 1
    while try_find_captcha:
        try:
            catpcha = driver.find_element(By.ID, 'challenge-stage')
            HTML = catpcha.get_attribute('outerHTML')
            
            if 'cloudflare.com'in HTML:                
                try_find_captcha = False
                CatpchaDetected = True
        except:
            time.sleep(0.3)
            count +=1
            if count == max_try:
                try_find_captcha = False
    return CatpchaDetected

def closeDriver():
    driver.quit()
######################################################################################### 
def optionsConfiguration(flag_load_profile = False):
    global options1, options2
    options1 = webdriver.ChromeOptions()
    # Adding argument to disable the AutomationControlled flag 
    options1.add_argument("--disable-blink-features=AutomationControlled") 

    # Exclude the collection of enable-automation switches 
    options1.add_experimental_option("excludeSwitches", ["enable-automation"]) 

    # Turn-off userAutomationExtension 
    options1.add_experimental_option("useAutomationExtension", False)  

    options2 = webdriver.ChromeOptions()
    # Adding argument to disable the AutomationControlled flag 
    options2.add_argument("--disable-blink-features=AutomationControlled") 

    # Exclude the collection of enable-automation switches 
    options2.add_experimental_option("excludeSwitches", ["enable-automation"]) 

    # Turn-off userAutomationExtension 
    options2.add_experimental_option("useAutomationExtension", False)    

    # Define default profiles folder
    # options.add_argument(r"user-data-dir=/Users/mitsonkyjecrois/Library/Application Support/Google/Chrome/Profile 1")
    if flag_load_profile:
        # # Define profile folder, profile number
        options.add_argument(r"user-data-dir=/Users/mitsonkyjecrois/Library/Application Support/Google/Chrome/Profile 1")
        # options1.add_argument(r"user-data-dir=/home/jorge/.config/google-chrome/")
        # Define profile folder, profile number
        # options1.add_argument(r"profile-directory=Profile 10")        # launch chrome navigator


def launchNavigator():
    global options1,options2, driver    
    optionsConfiguration(flag_load_profile = True)
    # options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    # options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    try:
        driver = webdriver.Chrome(options=options1)
    except:
        try:
           driver.close() 
        except:
            print("There aren't pending navigators to close ")
        driver = webdriver.Chrome(options=options2)
    # Changing the property of the navigator value for webdriver to undefined     

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  #Error
    driver.get('https://www.fastpeoplesearch.com/')
    wait_search_box(max_try = 15)

    SelectSearch(by_name = True)

def validateField(field):
    if not pd.isna(field):
        field = str(field)
    else:
        field = ''
    return field

def buildNameAddress(row, first_name_, last_name_, city_, state_, zip_):
    
    first_name_str = validateField(row[first_name_].item())
    last_name_str = validateField(row[last_name_].item())
    name = first_name_str +' ' + last_name_str

    city_str = validateField(row[city_].item())
    state_str = validateField(row[state_].item())
    zip_str = validateField(row[zip_].item())
    address = city_str +' ' + state_str + ' ' + zip_str
    return name, address

def go_back(max_try = 3):
    try_back = True
    count = 0
    while try_back:
        try: 
            driver.back()
            print("--Back--")
            try_back = False
        except:
            time.sleep(0.3)
            count +=1
            if count == max_try:
                try_back = False
                driver.get('https://www.fastpeoplesearch.com/')
#########################################################################################
#                    CHROME OPTIONS CONFIGURATION                                       #
######################################################################################### 
# options = webdriver.ChromeOptions()
# options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")

# optionsConfiguration()
# options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})

#########################################################################################
#                               DRIVER START                                            #
#########################################################################################
# driver = webdriver.Chrome(options=options)

# driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  #Error

# #########################################################################################
#                             MAIN                                                        #
# #########################################################################################
list_colums = ['search_name','search_address','name','age','primary_phone'
                       ,'main_address', 'list_phones','past_address', 'status', ]


def validate_file_colums(selected_file, regular_columns = ['Owner 1 First Name', 'Owner 1 Last Name', 'City', 'State', 'Zip']):
    df = pd.read_csv(selected_file)
    list_files_columns = df.columns
    list_missed = []
    
    for column_name in regular_columns:
        if not column_name in list_files_columns:
            list_missed.append(column_name)
    return list_missed

def processControl(t, _stop, selected_file, output_file, CatpchaDetected):
    global df, df_all, list_colums, last_row, dict_issues, all_info, last_row_dict
    global name_search, address_search, flag_click_next, dbase, row, count_except
    nsteps = 9
    print('-',end='')
    if t == 0:
        # print("T inicial: ", t)
        CatpchaDetected = False        
        df = pd.read_csv(selected_file)        

        # INITIALIZATION LOAD CHECK POINTS AND PREVIOUS FILES.
        previous_run_flag, last_row_dict, last_row = search_check_points(selected_file, check_point_filename = 'check_points/last_row.json')        
        dict_issues = load_check_point('check_points/issues_row.json')       
        if previous_run_flag:
            df_all = pd.read_csv(output_file)
        else:
            df_all = pd.DataFrame()

        # DataBase connection
        dbase = createConection()        
        t +=1
        count_except = 0     
    current_row = (t-1)//nsteps + last_row
    print("t:", t, "Step: ", (t-1)%nsteps," Row: ", current_row + 1 ,'/',len(df))
    if t!=0:
        CatpchaDetected = detectCatpcha(max_try = 2)                
        # while current_row <= len(df):
        if not CatpchaDetected:
            if (t-1)%nsteps == 0:            
                row = df.iloc[[current_row]]
            try:            
                if (t-1)%nsteps == 1:
                    name_search, address_search = buildNameAddress(row, 'Owner 1 First Name', 'Owner 1 Last Name', 'City', 'State', 'Zip')
                    # flag_click_next = True
                if (t-1)%nsteps == 2:  
                    sendSearch(name_search, address_search)
                if (t-1)%nsteps == 3:                    
                    CatpchaDetected = detectCatpcha(max_try = 2)
                    if CatpchaDetected:
                        _stop = True
                if (t-1)%nsteps == 4:
                    wait_results(max_try = 2)                
                if (t-1)%nsteps >= 5 and (t-1)%nsteps <= 8:
                    # if flag_click_next:
                    if (t-1)%nsteps == 5:                           
                        imitateBehavior(max_tries = 10)
                    if (t-1)%nsteps == 6:
                        df_all = get_block_results(df_all, selected_file)
                        df_all[list_colums].to_csv(output_file,index= True)                        
                    if (t-1)%nsteps == 7:                            
                        flag_click_next = nextPage(max_try = 2)# Regresar al paso 4                            
                        if flag_click_next:
                            print("More pages found: ")
                            t = t - 4
                            print("Go back step: 4")
                if (t-1)%nsteps == 8:
                    last_row_dict[selected_file.split('/')[-1]] = {'last_row':current_row}                    
                    saveCheckPoint('check_points/last_row.json', last_row_dict)

                    go_back(max_try = 3)
                    search_box_found  = wait_search_box(max_try = 4)
                    while not search_box_found:
                        driver.get('https://www.fastpeoplesearch.com/')
                        search_box_found  = wait_search_box(max_try = 4)                    
                    if current_row + 1 == len(df):
                        print("Stop last row")
                        _stop = True
                        t = -1
                count_except = 0
            except Exception as e:
                print("Current t: ", t)                
                t = t - 1
                CatpchaDetected = detectCatpcha()
                if CatpchaDetected:
                    _stop = True
                
                if not CatpchaDetected:                    
                    dict_issues[current_row] = {'name':name_search, 'address':address_search}
                    saveCheckPoint('check_points/issues_row.json', dict_issues)
                    driver.get('https://www.fastpeoplesearch.com/')
                    time.sleep(3)
                    
                count_except += 1
                if count_except == 3:
                    t = t - (t-1)%nsteps
                    driver.get('https://www.fastpeoplesearch.com/')
                    wait_search_box(max_try = 4)
                if count_except == 5:
                    t = t - (t-1)%nsteps + nsteps # pass to next row
                print("t: ", t ,"Restart step: ", (t-1)%nsteps)
            # print("Current Step: ", (t-1)%nsteps, end= '-')
        # if not CatpchaDetected:
            t +=1            
    return t, _stop, CatpchaDetected, current_row