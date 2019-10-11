import base64
import mysql.connector


mydb=mysql.connector.connect(host='localhost',user='root',passwd='',database='xpotify_db')
cursor=mydb.cursor()
cursor.execute("SELECT User_pic from USERS")

myresult = cursor.fetchall()

for num in range(0,len(myresult)):
	text=myresult[num][0].encode('utf-8')
	imgdata = base64.b64decode(text)
	filename = 'test.jpeg'  # I assume you have a way of picking unique filenames
	with open(filename, 'wb') as f:
		f.write(imgdata)
