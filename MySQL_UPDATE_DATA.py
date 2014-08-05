import MySQLdb

db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

cursor = db.cursor()
Change_answer = raw_input("Do you want to change your information ?(Y/N):")
if Change_answer == 'Y' or Change_answer == 'y':
	print "Please input yuor bsic information"
	info = {'Firstname':'Andy', 'Lastname':'Kuo', 'Age':18, 'Sex':'Male'}
	info['Firstname'] = raw_input ("Firstname : ")
	info['Lastname'] = raw_input ("Lastname : ")
	info['Age'] = input("Age : ")
	info['Sex'] = raw_input("Sex (Male or Female) : ")
	#MySQL Data UPDATE
	sql = """UPDATE basicInformation SET `FIRSTNAME`='%s', `LASTNAME` = '%s', `SEX` = '%s', `AGE`=%d WHERE `UID`=0x2693D55434""" \
	%(info['Firstname'],info['Lastname'],info['Sex'],info['Age'])
	try:
		cursor.execute(sql)
		db.commit()
	except:
		print "error"
		db.rollback()
