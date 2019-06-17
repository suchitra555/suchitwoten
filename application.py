from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
application = app = Flask(__name__)
import os
import time
import random
import redis
import pyodbc

myHostname = "azureassignment3.redis.cache.windows.net"
myPassword = "xw5S6heXPfqGZL4PfzatH+d7nnCawcY5dSMNTyWC+qQ="
server = 'mysqlserversuchitra.database.windows.net'
database = 'assignment3'
username = 'azureuser'
password = 'Geetha1963@'
driver= '{ODBC Driver 17 for SQL Server}'

r = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
#conn = sqlite3.connect('database.db')
# print("Opened database successfully")
#conn.execute('drop table earthquake')
#conn.execute('CREATE TABLE Earthquake (time text,latitude real,longitude real,depth real,mag real,magType text,nst real,gap real,dmin real,rms real,net text,id text,updated text,place text,type text,horizontalError real,depthError real,magError real,magNst real,status text,locationSource text,magSource text)')
# print("Table created successfully")
# conn.close()
<<<<<<< HEAD

=======
>>>>>>> fivethirty/master
port = int(os.getenv('PORT', 5000))
@app.route('/')
def home():
   return render_template('home.html')

# @app.route('/enternew')
# def upload_csv():
#    return render_template('upload.html')
#
# @app.route('/addrec',methods = ['POST', 'GET'])
# def addrec():
#    if request.method == 'POST':
#        con = sql.connect("database.db")
#        csv = request.files['myfile']
#        file = pd.read_csv(csv)
#        file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)
#        con.close()
#        return render_template("result.html",msg = "Record inserted successfully")

@app.route('/list')
def list():
   con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
   cur = con.cursor()
   cur.execute("select * from all_month")
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",rows = rows)

@app.route('/records')
def records():
   return render_template('records.html')

@app.route('/options' , methods = ['POST', 'GET'])
def options():
   con = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
   mc = redis.StrictRedis(host=myHostname, port=6380,password=myPassword,ssl=True)
   start_time = time.time()
   num =int(request.form['num'])
   rows = []
   c = []
   for i in range(num):
       val = round(random.uniform(2,5),1)
       print(val)
       cur = con.cursor()
       a = 'select * from all_month WHERE mag = '+str(val)
       #cur.execute("select * from all_month WHERE mag = ?" ,(val,))
       #get = cur.fetchall();
       #rows.append(get)
       print(rows)
       v = str(val)
       if r.get(a):
           print ('Cached')
           c.append('Cached')
       else:
           print('Not Cached')
           c.append('Not Cached')
           cur.execute("select * from all_month WHERE mag = ?" ,(val,))
           get = cur.fetchall()
           r.set(a,str(get))
   con.close()
   end_time = time.time()
   elapsed_time = end_time - start_time
   r.flushdb();
   return render_template("list1.html",rows = [c],times=elapsed_time)

@app.route('/restricted')
def restricted():
   return render_template('rest.html')

@app.route('/options2' , methods = ['POST', 'GET'])
def options2():
   con = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
   start_time = time.time()
   num =int(request.form['num'])
   loc = (request.form['loc'])
   rows = []
   for i in range(num):
       cur = con.cursor()
       b = "select * from all_month WHERE place LIKE %"+loc+"%"
       #cur.execute("select * from all_month WHERE place LIKE ?", ('%'+loc+'%',))
       #get = cur.fetchall()
       #rows.append(get)
       if r.get(b):
           rows.append(r.get(b))
           print ('Cached')
       else:
           print('Not Cached')
           cur.execute("select * from all_month WHERE place LIKE ?", ('%'+loc+'%',))
           get = cur.fetchall();
           rows.append(get)
           r.set(b,str(get))
   end_time = time.time()
   elapsed_time = end_time - start_time
   r.flushdb()
   return render_template("list2.html",row=rows,etime=elapsed_time)



if __name__ == '__main__':
<<<<<<< HEAD
   app.run(host='0.0.0.0',port=port)
=======
   app.run('0.0.0.0',port=port)
  
>>>>>>> fivethirty/master
