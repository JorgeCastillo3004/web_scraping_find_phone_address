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
# dictdata = {
#         "search_name": "William Roboski",
#         "search_address": "Edgewater FL 32141",
#         "name": "William Roboski",
#         "primary_phone": "(321) 663-8417",
#         "list_phones": {
#             "0": "(407) 366-0067",
#             "1": "(407) 366-4294",
#             "2": "(407) 267-2288",
#             "3": "(407) 340-7165",
#             "4": "(407) 758-0498",
#             "5": "(425) 369-9852",
#             "6": "(407) 365-5495"
#         },
#         "main_address": "4689 Bayfield Harbor Ln Edgewater FL 32141",
#         "past_address": {
#             "0": "2311 Guava Dr Edgewater FL 32141",
#             "1": "825 E State Road 434 Winter Springs FL 32708",
#             "2": "429 Terrace Dr Oviedo FL 32765",
#             "3": "405 Hunters Run Edgefield SC 29824",
#             "4": "1425 Spalding Rd Winter Springs FL 32708",
#             "5": "2476 Mills Creek Rd Chuluota FL 32766"
#         },
#         "status": "found"
#     }

# insertNewRegister(dbase, dictdata, 'filename.csv')
# results = getPeopleContactByFile(dbase, '*')

# print("results", results)

# for result in results:
#  	print(result)



closeConection(dbase)