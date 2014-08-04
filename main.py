#encoding = utf-8
#!/usr/bin/python
import RPi.GPIO as GPIO
import MFRC522
import signal

MIFAREReader = MFRC522.MFRC522()

print "Welcome to the RFID ID CARD SYSTEM"
print "Press Ctrl-c to STOP"

while True:

		(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

		if status == MIFAREReader.MI_OK:
				print "Card detected"
		(status,uid) = MIFAREReader.MFRC522_Anticoll()

		if status == MIFAREReader.MI_OK:
