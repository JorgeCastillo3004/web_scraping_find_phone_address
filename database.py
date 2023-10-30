import sqlite3
import os
import pandas as pd

def createConection():
    dbase = sqlite3.connect("peoplesearch.db")
    return dbase

def closeConection(dbase):
    dbase.close()

def createTablePeople(dbase):
	dbase.execute('''CREATE TABLE IF NOT EXISTS people (name TEXT, phone TEXT,
	  				address TEXT, list_phones TEXT, past_address TEXT, status TEXT, filename TEXT, current_row INT)''')

def getPeopleContact(dbase):
	data = dbase.execute("SELECT name, phone, address FROM people")
	result = data.fetchall()    
	return result

def insertNewRegister(dbase, dictdata, filename_):
	name = dictdata['name']
	phone = dictdata['primary_phone']	
	address = dictdata['main_address']		
	list_phones = str(dictdata['list_phones'])
	past_address = str(dictdata['past_address'])
	status = dictdata['status']
	current_row = dictdata['current_row']

	dbase.execute(''' INSERT INTO people (name, phone, address, list_phones, past_address, status,filename, current_row) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
	 (name, phone, address, list_phones, past_address, status, filename_, current_row))
	dbase.commit()

def getPreviousRegisters(dbase, filename_):
	data = dbase.execute("SELECT name, phone, address FROM people WHERE filename =='{}'".format(filename_))
	#data = dbase.execute("SELECT * FROM people WHERE filename =='{}'".format(filename_))	
	return data.fetchall()
	
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

# if os.path.isfile('peoplesearch.db'):
# 	os.remove('peoplesearch.db')
	
dbase = createConection()
createTablePeople(dbase)


# current_row = 5
# dictdata = {'name':'George cast', 'primary_phone':'04257366257', 'main_address':'Merida Venezuela',
#  			'list_phones': '', 'past_address':'', 'current_row':current_row, 'status':'found'}

# insertNewRegister(dbase, dictdata, 'file2.csv')

# results = getPreviousRegisters_all(dbase, 'Address_list.csv')

# print("results")
# print(len(results))
# print(type(results))

# print('\n')
# for line in results:
# 	print('#', line, '#')
	# for cell in line:
	# 	print(cell)
# print(results)

# last_row = getLastRow(dbase, 'file2.csv')

# print(last_row, type(last_row))



closeConection(dbase)