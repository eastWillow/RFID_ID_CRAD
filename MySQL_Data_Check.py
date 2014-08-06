#encoding :utf-8
#!/usr/bin/python

import MySQLdb

db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

cursor = db.cursor()

sql = """SELECT * FROM basicInformation WHERE UID=0x2693d55434"""

cursor.execute(sql)

results = cursor.fetchall()

for row in results:
		UID =  row[0].encode('hex')
		FIRSTNAME = row[1]
		LASTNAME = row[2]
		SEX = row[3]
		AGE = row[4]

		print "UID = 0x%s,Your Name=%s %s,%s %s"%\
				(UID,FIRSTNAME,LASTNAME,SEX,AGE)
db.close()
