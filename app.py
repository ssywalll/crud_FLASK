from flask import Flask, render_template, url_for, request, flash, redirect, json
from flask_mysqldb import MySQL
import requests


app = Flask(__name__)
app.secret_key = 'aslkdh'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

@app.route('/')
def mysql_route():
    return render_template('home.html')

@app.route('/mysql')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', users=data)

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        avatar = request.form['avatar']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (email, first_name, last_name, avatar) VALUES (%s, %s, %s, %s)",(email, firstname, lastname, avatar))
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id_data))
    mysql.connection.commit()
    return redirect(url_for('index'))

@app.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        avatar = request.form['avatar']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE users SET email=%s, first_name=%s, last_name=%s, avatar=%s,
        WHERE id=%s   
        """, (email, firstname, lastname, avatar, id_data))
        flash("Data Upated Successfully")
        return redirect(url_for('index'))
    
@app.route('/users/fetch', methods = ['GET'])
def user_fetch():
    req = requests.get("https://reqres.in/api/users?page=1") 
    data = json.loads(req.content)
    return render_template('api.html', data=data['data'])

if __name__ == "__name__":
    app.run(host='localhost', port=5000, debug=True)
