#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:29:36 2020

@author: juanis
"""

# Third party imports
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

# Connection to DataBase
conn = psycopg2.connect(user = "postgres",
                        password = "Jgrccgv",
                        host = "localhost",
                        port = "5432",
                        database = "users_app")
cur = conn.cursor()
app = Flask(__name__)

# For starting a session
app.secret_key = 'mysecretkey' #(???)


# Main Window
@app.route("/")
def main_window():
    return render_template('login.html')
    

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['passwd']
        
        # Verify username is on the database
        try: 
            cur.execute("select username from user_app where username='"+username_input+"'")
            cur.execute("select passwd from user_app where username='"+username_input+"'")
            passwd =  str(cur.fetchone()[0])
            if password_input != passwd:
                flash("La contraseña es incorrecta")
                return render_template('login.html')
            
            else:   
                cur.execute("select user_type from user_app where username='"+username_input+"'")
                usertype_input =  str(cur.fetchone()[0])
                
                # Get user type to know what main_window to open
                if usertype_input == 'admin':
                    return redirect(url_for('main_admin'))
                elif usertype_input == 'teacher':
                    return redirect(url_for('main_teacher'))
                else: #usertype_input == 'student'
                    return redirect(url_for('main_student'))
        
        except: 
            flash("El usuario no se encuentra registrado")
            return render_template('login.html')


#-----------------------------------------------------------------------------#

@app.route("/main_student", methods=['POST', 'GET'])
def main_student():
    #query para crear tabla que muestra las materias del estudiante que hizo log in
    #con las notas de sus respectivos cortes y la nota final
    
    cur.execute('select * from students') 
    data = cur.fetchall()
    return render_template('main_student.html', classes = data)       
    
#-----------------------------------------------------------------------------#

@app.route("/main_teacher", methods=['POST', 'GET'])
def main_teacher():
    #query para crear tabla que muestra las materias que el profesor esta dictando
    cur.execute('select * from students')
    data = cur.fetchall()
    return render_template('main_teacher.html', classes = data) 

@app.route('/class/<string:class_name>', methods = ['POST','GET'])
def show_class(class_name):
    #query para crear tabla que muestra los estudiantes inscritos en la materia seleccionada
    cur.execute(f"select * FROM students WHERE class_name = '{class_name}'")
    data = cur.fetchall()
    return render_template('class.html', students = data, class_name=class_name)    
    
   
#-----------------------------------------------------------------------------#

@app.route("/main_admin", methods=['POST', 'GET'])
def main_admin():
    cur.execute('select * from user_app')
    data = cur.fetchall()
    return render_template('main_student.html', users = data) 





if __name__ == "__main__":
    app.run(port = 3000, debug = True)