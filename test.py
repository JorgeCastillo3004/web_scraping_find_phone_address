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

# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)
# driver.get("https://www.fastpeoplesearch.com/")


def launchNavigator():
    global options, driver
    options = webdriver.ChromeOptions()
    optionsConfiguration()
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36")
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
    driver = webdriver.Chrome(options=options)
    # Changing the property of the navigator value for webdriver to undefined     

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")  #Error
    driver.get('https://www.fastpeoplesearch.com/')
    # wait_search_box(max_try = 15)
    # SelectSearch(by_name = True)

launchNavigator()

time.sleep(180)
