import sqlite3
import os
import pandas as pd
# from control import filter_by_file
import json

def createConection():
    dbase = sqlite3.connect("peoplesearch.db")
    return dbase

def closeConection(dbase):
    dbase.close()

def createTablePeople(dbase):
	# dbase.execute('''CREATE TABLE IF NOT EXISTS people (name TEXT, phone TEXT,
	#   				address TEXT, list_phones TEXT, past_address TEXT, status TEXT, filename TEXT, current_row INT)''')

	dbase.execute('''CREATE TABLE IF NOT EXISTS people (search_name TEXT,first_name TEXT, last_name TEXT, search_address TEXT,  search_city TEXT,
	  search_state TEXT, search_zip TEXT, address TEXT, city TEXT,  state TEXT,  zip TEXT, name TEXT, age TEXT,
	   phone TEXT,list_phones TEXT,	past_address TEXT, status TEXT, filename TEXT, current_row INT)''')

def createTableColumns(dbase):
	dbase.execute('''CREATE TABLE IF NOT EXISTS columns (name TEXT, address TEXT,
	  				city_state_zip TEXT)''')

def getPeopleContact(dbase):
	data = dbase.execute("SELECT name, phone, address FROM people")
	result = data.fetchall()    
	return result

def getColumnsNames(dbase):
	data = dbase.execute("SELECT name, address, city_state_zip FROM columns")
	return data.fetchall()

def insertNewRegister(dbase, dictdata, filename_):
	search_name = dictdata['search_name']
	first_name = dictdata['first_name']
	last_name = dictdata['last_name']
	search_address = dictdata['search_address']
	search_city = dictdata['search_city']
	search_state = dictdata['search_state']
	search_zip = str(dictdata['search_zip'])
	address = dictdata['address']
	city = dictdata['city']
	state = dictdata['state']
	zip_ = dictdata['zip']
	name = dictdata['name']
	age = dictdata['age']
	phone = dictdata['phone']
	list_phones = str(dictdata['list_phones'])
	past_address = str(dictdata['past_address'])
	status = dictdata['status']	
	current_row = dictdata['current_row']

	dbase.execute(''' INSERT INTO people (search_name, first_name, last_name, search_address, search_city, search_state, search_zip, address,
		 city, state, zip, name, age, phone, list_phones, past_address, status, filename, current_row) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
		 (search_name, first_name, last_name, search_address, search_city, search_state, search_zip, address, city, state, zip_,
		  name, age, phone, list_phones, past_address, status, filename_, current_row))
	dbase.commit()

def getPreviousRegisters(dbase, filename_):
	data = dbase.execute("SELECT name, phone, address FROM people WHERE filename =='{}'".format(filename_))
	#data = dbase.execute("SELECT * FROM people WHERE filename =='{}'".format(filename_))	
	return data.fetchall()

def getAllInfoPeopleContact(dbase):
	data = dbase.execute("SELECT * FROM people")
	result = data.fetchall()    
	return result

def getPreviousRegisters_all(dbase, filename_):
	previous_registers = dbase.execute("SELECT * FROM people WHERE filename == '{}'".format(filename_))
	return previous_registers.fetchall()

def getLastRow(dbase, filename_):
	select_last_record_sql = "SELECT current_row FROM people WHERE filename =='{}' ORDER BY current_row DESC LIMIT 1".format(filename_)
	last_row = dbase.execute(select_last_record_sql).fetchone()
	if last_row:
		return last_row[0]
	else:
		return 0

def deletePreviosRegister(dbase, filename_):
	delete_query = "DELETE FROM people WHERE filename = '{}'".format(filename_)
	dbase.execute(delete_query)
# if os.path.isfile('peoplesearch.db'):
# 	os.remove('peoplesearch.db')

def show_columns(dbase):
	columns = dbase.execute("PRAGMA table_info(people)").fetchall()
	columns = [column[1] for column in columns]
	return columns

def get_unique_files_names(dbase):
	query = f'SELECT DISTINCT filename FROM people;'
	return dbase.execute(query).fetchall()

dbase = createConection()
createTablePeople(dbase)
createTableColumns(dbase)
columns = show_columns(dbase)
print("columns: ", columns)
# show_columns(dbase)
# current_row = 5
# dictdata = {'name':'George cast', 'primary_phone':'04257366257', 'main_address':'Merida Venezuela',
#   			'list_phones': '', 'past_address':'', 'current_row':current_row, 'status':'found'}
# print("Inser new register")
# insertNewRegister(dbase, dictdata, 'file2.csv')
# show_columns(dbase)

# deletePreviosRegister(dbase, "Address_list.csv")
# last_row = getLastRow(dbase,"Address_list.csv")
# print("last_row", last_row)

# deletePreviosRegister(dbase, ' Address_list.csv ')

# data = getAllInfoPeopleContact(dbase)
# df_data_base = pd.DataFrame(data, columns = columns)
# print("Results from database: ",len(df_data_base))

# df_file = pd.read_csv('files/Address_list.csv')
# df_filtered, df_unfound = filter_by_file(df_data_base, df_file, cond1_e = True, cond2_e = True, cond3_e = True, cond4_e = True, cond5_e = True)

# print("len df_filtered ", len(df_filtered))
# print("Columns df: ", df.columns)
# print("Len df: ", len(df))

# df.to_csv('files/file_fromdatabase1.csv')

# for index, row in df.iterrows():
# 	name = row['address']
# 	print("Address: ",name)

# df.to_csv("test.csv")

uniquefiles = get_unique_files_names(dbase)
print("List of files: ", len(uniquefiles))
for file in uniquefiles:
	print(file)
# results.to_csv("datatest.csv")
# for line in results:
# 	print(line)
# print(last_row, type(last_row))
closeConection(dbase)