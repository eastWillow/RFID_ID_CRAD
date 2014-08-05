#encoding : utf-8
#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

cursor = db.cursor()

sql = """INSERT INTO basicInformation(UID,FIRSTNAME,LASTNAME,AGE,SEX)
		VALUES(%s,'%s','%s',%s,'%s')""" %('0x5566778899','Andy','Kuo','18','Male')
try:
	cursor.execute(sql)
	db.commit()
	print "succed"
except:
		print "error"
		db.rollback()
db.close()
