#encoding=utf-8
#!/usr/bin/python
print "Please input yuor bsic information"
info = {'Firstname':'Andy', 'Lastname':'Kuo', 'Age':18, 'Sex':'Male'}
info['Firstname'] = raw_input ("Firstname : ")
info['Lastname'] = raw_input ("Lastname : ")
info['Age'] = input("Age : ")
info['Sex'] = raw_input("Sex (Male or Female) : ")

print info
