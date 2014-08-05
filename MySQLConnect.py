#encoding : utf-8
#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

cursor = db.cursor()

sql = "INSERT INTO BASICINFORMATION (FIRSTNAME, LASTNAME, AGE, SEX \
		UID0, UID1, UID2, UID3, UID4) \
		VALUES \
		('%s', '%s', '%d', '%s', '%x', '%x', '%x', '%x', '%x')" % \
		('Andy', 'Kuo', 18, 'Male', 0x5a, 0x6a, 0x6c, 0xbf, 0x12)
try:
	cursor.execute(sql)
	db.commit()
	print "succed"
except:
		print "error"
		db.rollback()
db.close()
