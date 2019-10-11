import base64
import mysql.connector
import os

text='''
<?php
    $User_name= $_POST['User_Id'];
	$img = $_POST['image'];
	$image_parts = explode(";base64,", $img);
	$base64_image= $image_parts[1];
    $con = mysqli_connect('localhost','root','','xpotify_db');
   
   if(!$con)
   {
       die("database not connected");
   }
   $query= "INSERT INTO USERS (User_Name,User_pic) VALUES  ('$User_name','$base64_image')";

   $add_res = mysqli_query($con, $query) or die(mysqli_error($con));

?>
'''
print(text)
mydb=mysql.connector.connect(host='localhost',user='root',passwd='',database='xpotify_db')
cursor=mydb.cursor()
cursor.execute("SELECT User_pic from USERS")

myresult = cursor.fetchall()

for num in range(0,len(myresult)):
	text=myresult[num][0].encode('utf-8')
	imgdata = base64.b64decode(text)
	filename = '../html/images/test.jpeg'  # I assume you have a way of picking unique filenames
	with open(filename, 'wb') as f:
		f.write(imgdata)

os.system("chmod 777 ../html/images/test.jpeg");
