#!/usr/bin/env python
# -*- coding: utf8 -*-

import RPi.GPIO as GPIO
import MFRC522
import signal
import MySQLdb
import datetime
import time
t = time.time()
continue_reading = True
welcome_message = """
\033[32mWelcome to the \033[33mRFID \033[32mperson information register system\033[m \t
\033[32mPress \033[31mCtrl-C\033[m \033[32mto stop\033[m\t
Please use your \033[33mCard\033[m to Approach the sensor
"""
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
print welcome_message
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
			#MySQL Read Item List
			sql = """SELECT * FROM itemList WHERE OWENER_UID=0x%x%x%x%x%x"""%(uid[0],uid[1],uid[2],uid[3],uid[4])
			cursor.execute(sql)
			listCount = cursor.rowcount
			print "You Have %d Item(s)"%(listCount)
			if listCount > 0:
					Display_items = raw_input("Do you Want to Display \033[1;31mALL\033[m Items?(Y/N)")
					if Display_items == 'Y' or Display_items == 'y':
						results = cursor.fetchall()
						for row in results:
								ITEM_ID = row[0]
								OWENER_ID = row[1].encode('hex')
								OWENER_NAME = row[2]
								ITEM_NAME = row[3]
								STORAGE_TIME = row[4]
								EXPIRATION_DATE = row[5]
								print "ID:%d 0x%s Owener:%s ItemName:%s Storage:%s Expiration:%s"\
									%(ITEM_ID, OWENER_ID, OWENER_NAME, ITEM_NAME, STORAGE_TIME, EXPIRATION_DATE)
						#MySQL Delete Item
						Delete_exist_item = raw_input("Do you want to \033[1;31mDELETE\033[m Items?(Y/N)")
						if Delete_exist_item == 'Y' or Delete_exist_item == 'y':
							#Continue Delete
							while Delete_exist_item == 'Y' or Delete_exist_item == 'y':
								Which_to_delete = raw_input("Which ID Do Tou Want to Delete?:")
								sql = """DELETE FROM itemList WHERE `ITEM_ID`=%s"""%(Which_to_delete)
								try:
									cursor.execute(sql)
									db.commit()
									print("SUCCESS DELETE ITEM_ID:%s")%(Which_to_delete)
									Delete_exist_item = raw_input(\
									"Do You Want to \033[1;32mconutinue\033[m to \033[1;31mDELETE\033[m ?(Y/N):")
								except:
									db.rollback()
			#MySQL Add new Items
			Add_new_item_answer = raw_input("Do you want to \033[1;32mADD\033[m New Item?(Y/N)")
			if Add_new_item_answer == 'y' or Add_new_item_answer == 'Y':
				while Add_new_item_answer == 'y' or Add_new_item_answer =='Y':
					ITEM_NAME = raw_input("Please Input Item Name:")
					EXPIRATION_DATE = raw_input("Please Input EXPIRATION_DATE(1000-01-01):")
					sql = """INSERT INTO `itemList` 
							(`OWENER_UID` , `ITEM_NAME`, `EXPIRATION_DATE`, `STORAGE_TIME`,`OWENER_NAME`)
							VALUES (0x%s, '%s', '%s','%s','%s')"""\
							%(UID, ITEM_NAME, EXPIRATION_DATE, \
							datetime.datetime.fromtimestamp(t).strftime('%Y-%m-%d %H:%M:%S'), \
							FIRSTNAME+LASTNAME)
					try:
						cursor.execute(sql)
						db.commit()
						print ("Add New Item SUCCESS")
						Add_new_item_answer = raw_input(\
						"Do You Want to \033[1;32mconutinue\033[m to \033[1;32mADD\033[m ?(Y/N):")
					except:
						db.rollback()
			if not (len(ITEM_NAME) > 0):
				#Delete basic inforamtion
				Delete_answer = raw_input("Do you want to \033[1;31mDELETE\033[m your information ?(Y/N):")
				if Delete_answer == 'Y' or Delete_answer == 'y':
					sql = """DELETE FROM basicInformation WHERE `UID`=0x%s"""%(UID)
					try:
						cursor.execute(sql)
						db.commit()
						print "Delete Done"
					except:
						db.rollback()
						print "Please Delete All of Your Item"
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
		print welcome_message
