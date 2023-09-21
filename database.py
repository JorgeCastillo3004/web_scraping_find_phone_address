import sqlite3

def createConection():
    dbase = sqlite3.connect("peoplesearch.db")
    return dbase

def closeConection(dbase):
    dbase.close()

def createTablePeople(dbase):
	dbase.execute('''CREATE TABLE IF NOT EXISTS people (name TEXT, phone TEXT,
	  				address TEXT, list_phones TEXT, past_address TEXT, status TEXT, filename TEXT)''')

def getPeopleContact(dbase):
	data = dbase.execute("SELECT name, phone, address FROM people")
	result = data.fetchall()    
	return result

def getPeopleContactByFile(dbase, filename_):
	data = dbase.execute("SELECT name, phone, address FROM people WHERE filename =='{}'".format(filename_))	
	result = data.fetchall()    
	return result

def insertNewRegister(dbase, dictdata, filename_):
	name = dictdata['name']
	phone = dictdata['primary_phone']	
	address = dictdata['main_address']		
	list_phones = str(dictdata['list_phones'])
	past_address = str(dictdata['past_address'])
	status = dictdata['status']
	

	dbase.execute(''' INSERT INTO people (name, phone, address, list_phones, past_address, status,filename) VALUES (?, ?, ?, ?, ?, ?, ?)''',
	 (name, phone, address, list_phones, past_address, status, filename_))
	dbase.commit()

dbase = createConection()
createTablePeople(dbase)
closeConection(dbase)