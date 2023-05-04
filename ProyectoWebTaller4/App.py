from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = 'CrRK'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '14271058lG.'
app.config['MYSQL_DB'] = 'Clinica'
mysql = MySQL(app)

@app.route('/')
def index_():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/indexli.html')
def indexli():
    return render_template('indexli.html')

@app.route('/especialidades.html')
def especialidades():
    return render_template('especialidades.html')

@app.route('/servicios.html')
def servicios():
    return render_template('servicios.html')

@app.route('/quienessomos.html')
def quienessomos():
    return render_template('quienessomos.html')

@app.route('/contactanos.html')
def contactanos():
    return render_template('contactanos.html')

@app.route('/citas.html')
def citas():
    return render_template('citas.html')

@app.route('/registrarcita.html')
def registrarcita():
    return render_template('registrarcita.html')

@app.route('/registrarpaciente.html')
def registrarpaciente():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM pacientes')
    myresult = cursor.fetchall()
    #-Convertimos los datos a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObject.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('registrarpaciente.html', data=insertObject)

@app.route('/rp', methods=['POST'])
def regpac():
    nombre = request.form['nombre']
    ap_paterno = request.form['ap_paterno']
    ap_materno = request.form['ap_materno']
    fecha_nacimiento = request.form['f_nac']
    edad = request.form['edad']
    genero = request.form['genero']
    estado_civil = request.form['est_civil']
    tratamiento = request.form['tratamiento']
    num_familiares = request.form['Num_fam']
    nacionalidad = request.form['nacionalidad']
    estado = request.form['Estado']
    municipio = request.form['Municipio']
    direccion = request.form['direccion']
    codigo_postal = request.form['zip']
    telefono = request.form['telefono']
    
    msg = ''
    if nombre and ap_paterno and ap_materno and fecha_nacimiento and edad and estado_civil and tratamiento and num_familiares and nacionalidad and estado and municipio and direccion and codigo_postal and telefono:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "INSERT INTO pacientes (nombre,ap_paterno,ap_materno,fecha_nacimiento,edad,genero,estado_civil,tratamiento,num_familiares,nacionalidad,estado,municipio,direccion,codigo_postal,telefono) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s )"
        data = (nombre,ap_paterno,ap_materno,fecha_nacimiento,edad,genero,estado_civil,tratamiento,num_familiares,nacionalidad,estado,municipio,direccion,codigo_postal,telefono)
        cursor.execute(sql,data)
        mysql.connection.commit()
    else:
        msg = 'Campos vacios, por favor revise de nuevo.'
    return render_template('/registrarpaciente.html', msg = msg)

@app.route('/delete/<string:folio>', methods=['POST'])
def delete(folio):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "DELETE FROM pacientes WHERE folio=%s"
    data = (folio)
    cursor.execute(sql,data)
    mysql.connection.commit()
    return render_template('/registrarpaciente.html')

@app.route('/edit/<string:folio>', methods=['POST'])
def edit(folio):
    nombre = request.form['nombre']
    ap_paterno = request.form['ap_paterno']
    ap_materno = request.form['ap_materno']
    fecha_nacimiento = request.form['f_nac']
    edad = request.form['edad']
    genero = request.form['genero']
    estado_civil = request.form['est_civil']
    tratamiento = request.form['tratamiento']
    num_familiares = request.form['Num_fam']
    nacionalidad = request.form['nacionalidad']
    estado = request.form['Estado']
    municipio = request.form['Municipio']
    direccion = request.form['direccion']
    codigo_postal = request.form['zip']
    telefono = request.form['telefono']

    msg = ''
    if nombre and ap_paterno and ap_materno and fecha_nacimiento and edad and estado_civil and tratamiento and num_familiares and nacionalidad and estado and municipio and direccion and codigo_postal and telefono:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = "UPDATE pacientes SET nombre=%s,ap_paterno=%s,ap_materno=%s,fecha_nacimiento=%s,edad=%s,genero=%s,estado_civil=%s,tratamiento=%s,num_familiares=%s,nacionalidad=%s,estado=%s,municipio=%s,direccion=%s,codigo_postal=%s,telefono=%s WHERE folio=%s"
        data = (nombre,ap_paterno,ap_materno,fecha_nacimiento,edad,genero,estado_civil,tratamiento,num_familiares,nacionalidad,estado,municipio,direccion,codigo_postal,telefono,folio)
        cursor.execute(sql,data)
        mysql.connection.commit()
    else:
        msg = 'Campos vacios, por favor revise de nuevo.'
    return render_template('/registrarpaciente.html', msg = msg)


    
@app.route('/login.html', methods=['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['idUser']
            session['username'] = user['username']
            msg = 'Inicio de sesion exitoso'
            return render_template('/indexli.html', msg = msg)
        else:
            msg = 'Nombre de usuario y/o contraseña incorrectos'
    return render_template('/login.html', msg = msg)

@app.route('/signup.html', methods=['GET','POST'])
def signup():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'mail' in request.form :
        username = request.form['username']
        password = request.form['password']
        mail = request.form['mail']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Users WHERE username = % s', (username, ))
        user = cursor.fetchone()
        if user:
            msg = 'Cuenta existente'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', mail):
            msg = 'Direccion de correo invalida'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Usuario debe contener solo numeros y caracteres'
        elif not username or not password or not mail:
            msg = 'El campo de usuario o contraseña se encuentran vacios.'
        else:
            cursor.execute('INSERT INTO Users (username, password, mail) VALUES (%s, %s, %s)', (username, password, mail))
            mysql.connection.commit()
            msg = 'Se ha registrado exitosamente'
    elif request.method == 'POST':
        msg = 'Por favor llene todos los campos del formulario.'
    return render_template('/signup.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('idUser', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/recuperarpass.html')
def recuperarpass():
    return render_template('recuperarpass.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 4000, debug = True)