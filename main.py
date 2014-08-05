#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import MySQLdb
continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "\n\033[31mCtrl+C captured, ending read.\033[m"
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "\033[32mWelcome to the \033[33mRFID \033[32mperson information register system\033[m"
print "\033[32mPress \033[31mCtrl-C\033[m \033[32mto stop\033[m"
print "Please use your \033[33mCard\033[m to Approach the sensor"
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "\033[32mCard detected\033[m"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
		print "Card's UID is = \033[33m0x%X %X %X %X %X\033[m" %(uid[0],uid[1],uid[2],uid[3],uid[4]) 	
		print ""
		#MySQL Connect
		db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

		cursor = db.cursor()
		#MySQL SEARECH
		sql = """SELECT * FROM basicInformation WHERE UID=0x%x%x%x%x%x"""\
			%(uid[0],uid[1],uid[2],uid[3],uid[4])

		cursor.execute(sql)

		results = cursor.fetchall()
		if len(results) > 0:
			for row in results:
				UID =  row[0].encode('hex')
				FIRSTNAME = row[1]
				LASTNAME = row[2]
				SEX = row[3]
				AGE = row[4]

			print "UID = \033[33m0x%s\033[m,Your Name=\033[36m%s %s\033[m,\033[32m%s\033[m \033[35m%s\033[m Years Old"%\
						(UID,FIRSTNAME,LASTNAME,SEX,AGE)
			print ""
			#MySQL Delete Data
			Delete_answer = raw_input("Do you want to \033[1;31mDELETE\033[m your information ?(Y/N):")
			if Delete_answer == 'Y' or Delete_answer == 'y':
				sql = """DELETE FROM basicInformation WHERE `UID`=0x%s"""%(UID)
				try:
					cursor.execute(sql)
					db.commit()
					print "Delete Done"
				except:
					db.rollback()
			#MySQL Data UPDATE
			else:
				Change_answer = raw_input("Do you want to \033[1;34mCHANGE\033[m your information ?(Y/N):")
				if Change_answer == 'Y' or Change_answer == 'y':
					print "Please input yuor bsic information"
					info = {'Firstname':'Andy', 'Lastname':'Kuo', 'Age':18, 'Sex':'Male'}
					info['Firstname'] = raw_input ("Firstname : ")
					info['Lastname'] = raw_input ("Lastname : ")
					info['Age'] = input("Age : ")
					info['Sex'] = raw_input("Sex (Male or Female) : ")
					sql = """UPDATE basicInformation SET 
						`FIRSTNAME`='%s', `LASTNAME` = '%s', `SEX` = '%s', `AGE`=%d WHERE `UID`=0x%s""" \
						%(info['Firstname'],info['Lastname'],info['Sex'],info['Age'],UID)
					try:
						cursor.execute(sql)
						db.commit()
						print "Change Done"
					except:
						db.rollback()
		#MySQL Add New Information
		else:
			Add_answer = raw_input("Do you want to \033[1;32mADD\033[m your information ?(Y/N):")
			if Add_answer == 'Y' or Add_answer == 'y':
				db.rollback()
				#Input Data
				print "Please input yuor bsic information"
				info = {'Firstname':'Andy', 'Lastname':'Kuo', 'Age':18, 'Sex':'Male'}
				info['Firstname'] = raw_input ("Firstname : ")
				info['Lastname'] = raw_input ("Lastname : ")
				info['Age'] = input("Age : ")
				info['Sex'] = raw_input("Sex (Male or Female) : ")
				#MySQL Data INSERT
				sql = """INSERT INTO basicInformation(UID,FIRSTNAME,LASTNAME,AGE,SEX)
					VALUES(0x%x%x%x%x%x,'%s','%s',%s,'%s')""" \
					%(uid[0],uid[1],uid[2],uid[3],uid[4],info['Firstname'],info['Lastname'],info['Age'],info['Sex'])
				try:
					cursor.execute(sql)
					db.commit()
					print"Add Done"
				except:
					db.rollback()
		db.close()
		#Welcome Meaasge	
		print ""
		print "\033[32mWelcome to the \033[33mRFID \033[32mperson information register system\033[m"
		print "\033[32mPress \033[31mCtrl-C\033[m \033[32mto stop\033[m"
		print "Please use your \033[33mCard\033[m to Approach the sensor"
