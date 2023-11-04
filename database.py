import sqlite3
import os
import pandas as pd

def createConection():
    dbase = sqlite3.connect("peoplesearch.db")
    return dbase

def closeConection(dbase):
    dbase.close()

def createTablePeople(dbase):
	# dbase.execute('''CREATE TABLE IF NOT EXISTS people (name TEXT, phone TEXT,
	#   				address TEXT, list_phones TEXT, past_address TEXT, status TEXT, filename TEXT, current_row INT)''')

	dbase.execute('''CREATE TABLE IF NOT EXISTS people (search_name TEXT, search_address TEXT,  search_city TEXT,
	  search_state TEXT, search_zip TEXT, address TEXT, city TEXT,  state TEXT,  zip TEXT, name TEXT, age TEXT,
	   phone TEXT,list_phones TEXT,	past_address TEXT, status TEXT, filename TEXT, current_row INT)''')

def getPeopleContact(dbase):
	data = dbase.execute("SELECT name, phone, address FROM people")
	result = data.fetchall()    
	return result

def insertNewRegister(dbase, dictdata, filename_):
	search_name = dictdata['search_name']
	search_address = dictdata['search_address']
	search_city = dictdata['search_city']
	search_state = dictdata['search_state']
	search_zip = str(dictdata['search_zip'])
	address = dictdata['main_address']
	city = dictdata['city']
	state = dictdata['state']
	zip_ = dictdata['zip']
	name = dictdata['name']
	age = dictdata['age']
	phone = dictdata['primary_phone']
	list_phones = str(dictdata['list_phones'])
	past_address = str(dictdata['past_address'])
	status = dictdata['status']	
	current_row = dictdata['current_row']

	dbase.execute(''' INSERT INTO people (search_name, search_address, search_city, search_state, search_zip, address,
		 city, state, zip, name, age, phone, list_phones, past_address, status, filename, current_row) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
		 (search_name, search_address, search_city, search_state, search_zip, address, city, state, zip_,
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
# columns = show_columns(dbase)
# print("columns: ", columns)
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

results = getPreviousRegisters_all(dbase, 'Address_list.csv')
print(len(results))

uniquefiles = get_unique_files_names(dbase)
print("List of files: ", len(uniquefiles))
for file in uniquefiles:
	print(file)
# results.to_csv("datatest.csv")
# for line in results:
# 	print(line)
# print(last_row, type(last_row))
closeConection(dbase)