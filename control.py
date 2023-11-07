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
#                                   MAIN FUNCTIONS                                       #
#                                                                                       #
#########################################################################################
def validateField(field):
    if not pd.isna(field):
        field = str(field)
    else:
        field = ''
    return field

def load_file(file_name):
    """Function to load last file generated"""
    if os.path.isfile(file_name):
        df_all = pd.read_csv(file_name)
    else:
        df_all = pd.DataFrame()
    return df_all

def wait_search_box(search_by_name, max_try = 15):
    wait_search_box_found = False
    flag_wait = True
    count = 0
    while flag_wait:
        try:
            if search_by_name:
                input_name = driver.find_element(By.ID, 'search-name-name')
            else:
                input_name = driver.find_element(By.ID, 'search-address-1')
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

def build_search_fields(search_by_name, row, dict_columns_names):    
    # regular_columns = ['first_name', 'last_name', 'Address', 'City', 'State', 'Zip']    
    first_box = []
    if search_by_name:        
        for column_name in dict_columns_names['name']:
            first_box.append(validateField(row[column_name].item()))
        
    else:
        for column_name in dict_columns_names['address']:
            first_box.append(validateField(row[column_name].item()))

    first_box = ' '.join(first_box)

    city_str = validateField(row[dict_columns_names['city_state_zip'][0]].item())
    state_str = validateField(row[dict_columns_names['city_state_zip'][1]].item())
    zip_str = validateField(row[dict_columns_names['city_state_zip'][2]].item())
    second_box = city_str +' ' + state_str + ' ' + zip_str
    return first_box, second_box

def sendSearch(name, address, search_by_name):
    wait = WebDriverWait(driver, 10)
    # free_search = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'search-form-button-submit.btn.btn-md.btn-primary')))

    if search_by_name:        
        # input_name = driver.find_element(By.ID, 'search-name-name')
        input_name = wait.until(EC.element_to_be_clickable((By.ID, 'search-name-name')))
        input_address = driver.find_element(By.ID, 'search-name-address')
    else:        
        input_name = wait.until(EC.element_to_be_clickable((By.ID, 'search-address-1')))
        input_address = driver.find_element(By.ID, 'search-address-2')

    input_name.clear()
    for character in name:
        input_name.send_keys(character)
        time.sleep(random.uniform(0.1,0.2))    
    
    input_address.clear()
    for character in address:
        input_address.send_keys(character)
        time.sleep(random.uniform(0.1,0.2))
    input_address.send_keys('\n')

    # time.sleep(random.uniform(0.5,1.2))
    # free_search.click()

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
def split_address(address_second_line):
    # Regular expressions for matching city, state, and zip code
    city_state_zip_pattern = r'(?P<city>.+?)\s*(?P<state>[A-Z]{2})\s+(?P<zipcode>\d{5}(?:-\d{4})?)'
    
    # Try to match the address using the pattern
    match = re.search(city_state_zip_pattern, address_second_line)
    
    if match:
        # Extract address and city/state/zip info
        city = match.group('city')
        state = match.group('state')
        zip_code = match.group('zipcode')
        return city, state, zip_code
    else:
        # If no match is found, return the original address
        print(address_second_line)
        input('check address')
        return None, None, None

def get_address(card_block):
    listdivs = card_block.find_elements(By.CSS_SELECTOR, 'div')
    dict_old_address = {}
    main_address = 'unfound'
    for count, div in enumerate(listdivs):
        if count ==0:            
            main_address = div.text.split('\n')[0]            
            address_second_line = div.text.split('\n')[1]
            city, state, zip_code = split_address(address_second_line)
                
        if count ==1:            
            old_address = div.find_elements(By.CSS_SELECTOR, 'div')
            list_old_address = []
            for i, old_ in enumerate(old_address):                
                dict_old_address[i] = old_.text.replace('\n',' ')
            break   
    return {'address': main_address, 'past_address':dict_old_address,
            'city':city, 'state':state, 'zip':zip_code}

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
    return {'phone':primary_phone, 'list_phones':dict_phones}

def get_block_results(df_all, current_row, row, dict_parameters, enable_filter = False):

    global first_field, second_field, dbase

    # card_blocks = driver.find_elements(By.CLASS_NAME, 'card-block')
    card_blocks = driver.find_elements(By.XPATH, '//div[@class="card-block"][.//h3[text()="Current Home Address:"]]')
    dict_register = {}
    if dict_parameters['search_by_name']:
        dict_register['search_name'] = first_field
        dict_register['search_address'] = ''
    else:
        dict_register['search_name'] = ''
        dict_register['search_address'] = first_field
    
    dict_register['first_name'] = row.first_name.item()
    dict_register['last_name'] = row.last_name.item()
    dict_register['search_city'] = row.City.item()
    dict_register['search_state'] = row.State.item()
    dict_register['search_zip'] = row.Zip.item()
    dict_register['current_row'] = current_row
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
        dict_register['filename'] = dict_parameters['selected_file'].split('/')[-1]
        for i in dict_register.keys():
            dict_partial_info[i] = [str(dict_register[i])]        

        # Condition to only take with the same last name
        if enable_filter:            
            if dict_register['last_name'] in dict_register['name'].split():
                insertNewRegister(dbase, dict_register, dict_parameters['selected_file'].split('/')[-1])
                df = pd.DataFrame.from_dict(dict_partial_info)        
                df_all = pd.concat([df_all, df])
        else:            
            insertNewRegister(dbase, dict_register, dict_parameters['selected_file'].split('/')[-1])
            df = pd.DataFrame.from_dict(dict_partial_info)
            df_all = pd.concat([df_all, df])            
    
    return df_all

def nextPage(max_try = 2):
    flag_click_next = True
    count = 0
    while flag_click_next:
        try:
            button_next = driver.find_element(By.XPATH, '//a[@class="btn" and contains(text(),"Next Page")]')
            button_next.click()
            flag_continue = True
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

def launchNavigator(load_profile = False, search_by_name = True):
    global options1,options2, driver    
    optionsConfiguration(flag_load_profile = load_profile)
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
    wait_search_box(search_by_name, max_try = 15)

    SelectSearch(by_name = search_by_name)

def closeDriver():
    driver.quit()

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

def validate_file_colums(selected_file, search_by_name):
    regular_columns = ['first_name', 'last_name', 'City', 'State', 'Zip', 'Address']
    # regular_columns = ['first_name', 'last_name', 'address', 'city', 'state', 'zip']
    df = pd.read_csv(selected_file)
    list_files_columns = df.columns
    list_missed = []
    
    if search_by_name:
        regular_columns = regular_columns[0:5]
    else:
        regular_columns = regular_columns[2:]

    for column_name in regular_columns:
        if not column_name in list_files_columns:
            list_missed.append(column_name)
    return list_missed

def filter_by_file(df_data_base, df_file, cond1_e = True, cond2_e = True, cond3_e = True, cond4_e = True, cond5_e = True):    
    dict_columns_names = load_check_point('check_points/columns_names.json')
    list_index_unfound = []
    df_filtered = pd.DataFrame()
    for row_number in range(0, len(df_file)):
            # Cond1 address
        print("-", end= '')
        if cond1_e:            
            cond1 = df_data_base.address == df_file.iloc[row_number][dict_columns_names['address'][0]]
        else:            
            cond1 = df_data_base.address == df_data_base.address
            
        if cond2_e:
            last_name = dict_columns_names['name'][1]
            cond2 = df_data_base.apply(lambda row: df_file.iloc[row_number][last_name].lower() in row['name'].lower().split(), axis=1)
        else:
            cond2 = df_data_base.name == df_data_base.name
            
        if cond3_e:
            cond3 = df_data_base.city == df_file.iloc[row_number][dict_columns_names['city_state_zip'][0]]
        else:
            cond3 = df_data_base.city == df_data_base.city
        # Match State
        if cond4_e:
            cond4 = df_data_base.state == df_file.iloc[row_number][dict_columns_names['city_state_zip'][1]]
        else:
            cond4 = df_data_base.state == df_data_base.state
        # Match zip code
        if cond5_e:
            cond5 = df_data_base.zip == df_file.iloc[row_number][dict_columns_names['city_state_zip'][2]]
        else:
            cond5 = df_data_base.zip == df_data_base.zip

        df_row = df_data_base[cond1 & cond2 & cond3][0:1]
        if len(df_row)==0:
            list_index_unfound.append(row_number)
        else:
            df_filtered = pd.concat([df_filtered, df_row])
            
    df_unfound = df_file.iloc[list_index_unfound]    
    df_unfound = df_unfound.drop_duplicates().reset_index(drop=True)    
    df_filtered = df_filtered.drop_duplicates().reset_index(drop=True)

    return df_filtered, df_unfound


def processControl(t, dict_parameters):    
    global df, df_all, last_row
    global all_info, last_row_dict, dict_issues ## delete
    global first_field, second_field, flag_click_next, dbase, row, count_except, dict_columns_names
    
    _stop = False
    CatpchaDetected = False
    dbase = dict_parameters['dbase']
    last_row = dict_parameters['last_row']
    nsteps = 9
    print('-',end='')
    if t == 0:
        # print("T inicial: ", t)
        CatpchaDetected = False        
        df = pd.read_csv(dict_parameters['selected_file'])
        df_all = dict_parameters['previous_registers']        
        dict_columns_names = load_check_point('check_points/columns_names.json')
        # DataBase connection
        # dbase = createConection()  # self.dict_parameter['dbase']
        t +=1
        count_except = 0
        
        SelectSearch(by_name = dict_parameters['search_by_name'] , max_try = 15) # Select type of search

    current_row = (t-1)//nsteps + last_row
    print("t:", t, "Step: ", (t-1)%nsteps," Row: ", current_row + 1 ,'/',len(df))
    if t!=0:
        CatpchaDetected = detectCatpcha(max_try = 2)                
        # while current_row <= len(df):
        if not CatpchaDetected:
            if (t-1)%nsteps == 0:            
                row = df.iloc[[current_row]]
            # try:
            if (t-1)%nsteps == 1:
                first_field, second_field = build_search_fields(dict_parameters['search_by_name'], row, dict_columns_names)                
                # flag_click_next = True
            if (t-1)%nsteps == 2:  
                sendSearch(first_field, second_field, dict_parameters['search_by_name'])
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
                    df_all = get_block_results(df_all, current_row, row, dict_parameters, enable_filter = False)
                if (t-1)%nsteps == 7:
                    webdriver.ActionChains(driver).send_keys(Keys.END).perform()
                    flag_click_next = nextPage(max_try = 2)# Regresar al paso 4                            
                    if flag_click_next:
                        print("#"*50)
                        print("More pages found: ")
                        t = t - 4
                        print("Go back step: 4")
            if (t-1)%nsteps == 8:
                if len(df_all) != 0:
                    list_colums = ['search_name','search_address','first_name','last_name', 'search_city', 'search_state', 'search_zip',
                    'address','city', 'state', 'zip','name','age','phone',
                    'list_phones','past_address', 'status']
                    print("df len: ", len(df_all))
                    # paht_out = dict_parameters['export_file_name']
                    # dict_parameters['export_file_name'] = dict_parameters['export_file_name'] if dict_parameters['export_file_name'].endswith('.csv') else dict_parameters['export_file_name'] + '.csv'
                    # df_all[list_colums].to_csv(dict_parameters['export_file_name'], index= True)

                # go_back(max_try = 3)
                driver.get('https://www.fastpeoplesearch.com/')
                SelectSearch(by_name = dict_parameters['search_by_name'] , max_try = 15)
                search_box_found  = wait_search_box(dict_parameters['search_by_name'], max_try = 4)
                while not search_box_found:
                    driver.get('https://www.fastpeoplesearch.com/')
                    search_box_found  = wait_search_box(dict_parameters['search_by_name'], max_try = 4)                    
                if current_row + 1 == len(df):
                    print("Stop last row")
                    _stop = True
                    t = -1
            count_except = 0
            # except Exception as e:
            #     print("Current t: ", t)                
            #     t = t - 1
            #     CatpchaDetected = detectCatpcha()
            #     if CatpchaDetected:
            #         _stop = True
                
            #     if not CatpchaDetected:                    
            #         print("Close aids")
            #         # try: close aids
            #         # dict_issues[current_row] = {'name':first_field, 'address':second_field}
            #         # saveCheckPoint('check_points/issues_row.json', dict_issues)
            #         # driver.get('https://www.fastpeoplesearch.com/')
            #         # time.sleep(3)
                    
            #     count_except += 1
            #     if count_except == 3:
            #         t = t - (t-1)%nsteps
            #         driver.get('https://www.fastpeoplesearch.com/')
            #         SelectSearch(by_name = dict_parameters['search_by_name'] , max_try = 15)
            #         wait_search_box(dict_parameters['search_by_name'], max_try = 4)
            #         count_except = 0
            #     if count_except == 5:
            #         t = t - (t-1)%nsteps + nsteps # pass to next row
            #     print("t: ", t ,"Restart step: ", (t-1)%nsteps)

            t +=1            
    return t, _stop, CatpchaDetected, current_row

