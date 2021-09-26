from flaskext.mysql import MySQL
from flask import session
from flask import Flask, jsonify, request, render_template, json, redirect, flash
from flask_cors import CORS



mysql = MySQL()
app = Flask(__name__)
#CORS(app)
app.secret_key = 'why would I tell you my secret key?'

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'library_db'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


# @app.route('/showMessage')
# def showMessage():
#     if cursor.execute("select * from messages"):
#         mesasage = cursor.fetchone()
#         print(mesasage)
#         return render_template('index.html', mesasage)


app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
        _first_name = request.form['FirstName']
        _last_name = request.form['LastName']
        _email = request.form['inputEmail']

        if _first_name and _email and _last_name:

            conn = mysql.connect()
            cursor = conn.cursor()
            if cursor.execute("select * from tbl_user where email=%s", _email):
                cursor.fetchone()
                # win32api.MessageBox(
                #     0, 'Please Login', 'Already registered', 0x00001000)
                flash('Entered details already present in the DataBase.')
                return redirect('/getData')
            else:
                #_hashed_password = generate_password_hash(_password)
                cursor.execute(
                    "INSERT INTO tbl_user(first_name, last_name,email) VALUES (%s, %s, %s)", (_first_name,_last_name, _email))
                conn.commit()
                flash('Entered details stored in the DataBase.')
            # cursor.execute(
            #         "SELECT * FROM tbl_user WHERE user_name =%s", [_first_name])
        if cursor is not None:
            #data = cursor.fetchall()
            cursor.close()
            conn.close()
    
        return render_template('display.html')


@app.route('/getData', methods=['GET','POST'])
def getData():
    
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM tbl_user")
        flash('Fetched details stored in the DataBase.')
            # cursor.execute(
            #         "SELECT * FROM tbl_user WHERE user_name =%s", [_first_name])
        if cursor is not None:
            # data = cursor.fetchall()
            # if len(data) > 0:
            #     session['user'] = data[0][0]
            #     print(data)
            cursor.close()
            conn.close()
    
        return render_template('display.html')
        
            # except Exception as e:
            #     print(str(e))
            #     return json.dumps({'error': str(e)})
            # finally:
                # cursor.close()
                # conn.close()

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0')
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    #session.init_app(app)

    app.debug = True
    app.run()