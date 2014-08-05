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
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the RFID person information register system"
print "Press Ctrl-C to stop."
print "Please use your Card to Approach the sensor"
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
		print " Your UID is = "
		print "0x%X %X %X %X %X" %(uid[0],uid[1],uid[2],uid[3],uid[4]) 	
		#MySQL Connect
		db = MySQLdb.connect("127.0.0.1","pi","make","RFID")

		cursor = db.cursor()
		sql = """SELECT * FROM basicInformation WHERE UID=0x%x%x%x%x%x """\
				%(uid[0],uid[1],uid[2],uid[3],uid[4])
		cursor.execute(sql)
		results = cursor.fetchall()
		for row in results:
				UID = row[0]
				FIRSTNAME = row[1]
				LASTNAME = row[2]
				SEX = row[3]
				AGE = row[4]
				print "Hi 0x%h Your name is: %s %s.You are %d years old, %s"\
						%(UID,FIRSTNAME,LASTNAME,AGE,SEX)
		
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
		except:
			db.rollback()
		db.close()
		#Welcome Meaasge	
		print "Welcome to the RFID person information register system"
		print "Press Ctrl-C to stop."
		print "Please use your Card to Approach the sensor"
