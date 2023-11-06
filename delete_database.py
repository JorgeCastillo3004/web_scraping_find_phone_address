import sqlite3
import os
import pandas as pd
# from control import filter_by_file
import json

if os.path.isfile('peoplesearch.db'):
	os.remove('peoplesearch.db')