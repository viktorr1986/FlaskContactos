from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontactos'

mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contactos = data)
    # return 'Fhje'

@app.route('/AddContact', methods=['POST'])
def AddContact():
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        print(Nombre)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contactos (Nombre, Telefono, Email) VALUES (% s, % s, % s)', (Nombre, Telefono, Email))
        mysql.connection.commit()
        flash('Contacto agregado')
        return redirect(url_for('Index'))
    # return 'AddContact'

@app.route('/edit/<id>')
def Edit(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = % s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit.html', contacto = data[0])
    # return 'Editar'

@app.route('/update/<id>', methods = ['POST'])
def Actualizar(id):
    if request.method == 'POST':
        Nombre = request.form['Nombre']
        Telefono = request.form['Telefono']
        Email = request.form['Email']
        cur = mysql.connection.cursor()
        cur.execute(""" UPDATE contactos SET Nombre=% s, Telefono=% s, Email=% s WHERE id =% s """, (Nombre, Telefono, Email, id))
        mysql.connection.commit()
        flash('Contacto actualizado')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def Delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado')
    return redirect(url_for('Index'))
    # return id
    # return 'Elimminar'

if __name__ == '__main__':
    app.run(port=3000, debug=True)
