#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 16:29:36 2020

@author: juanis
"""

# Third party imports
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Connection to DataBase
conn = psycopg2.connect(user = "postgres",
                        password = "Jgrccgv",
                        host = "localhost",
                        port = "5432",
                        database = "epsilon")
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

@app.route('/class/<string:class_name>', methods = ['POST', 'GET'])
def show_class(class_name):
    #query para crear tabla que muestra los estudiantes en orden alfabetico inscritos en la materia seleccionada
    cur.execute(f"select * FROM students WHERE class_name = '{class_name}'")
    data = cur.fetchall()
    return render_template('class.html', students_class = data, class_name=class_name)    
    

@app.route('/class_edit/<string:class_name>', methods = ['POST','GET'])
def edit_grade(class_name):
    #query para crear tabla que muestra los estudiantes en orden alfabetico inscritos en la materia seleccionada
    cur.execute(f"select * FROM students WHERE class_name = '{class_name}'")
    data = cur.fetchall()
    return render_template('class_edit.html', class_name = class_name, students_class = data)

@app.route('/class_update/<string:class_name>', methods=['POST'])
def update_grade(class_name):
    cur.execute(f"select * FROM students WHERE class_name = '{class_name}'")
    students_class = cur.fetchall()
    
    
    # Mover a administrador 
    df = pd.DataFrame(students_class, columns =['user', 'student', 'class_name', 'grade1', 'grade2', 'grade3', 'grade_final'])
    df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
    conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
    sns.set(font_scale=1.2)
    ax = conteo_promedio.plot.bar(x="Promedio Final", y="Numero Estudiantes", rot=50, title="Promedio estudiantes materia")
    ax.set(
        ylabel="Numero estudiantes",
        xlabel="Promedio Final",
        )
    plt.savefig('Reporte.png')
    
    # ---------------------------------------
   
    if request.method == 'POST':
        for student in students_class:
            grade1 = request.form['grade1_'+student[0]]
            grade2 = request.form['grade2_'+student[0]]
            grade3 = request.form['grade3_'+student[0]]
            grade_final = str(round((float(grade1)+float(grade2)+float(grade3))/3,2))
            cur.execute("""
                UPDATE students
                SET grade1 = %s,
                    grade2 = %s,
                    grade3 = %s,
                    grade_final = %s
                WHERE username = %s and class_name = %s
            """, (grade1, grade2, grade3, grade_final, student[0], class_name))
            conn.commit()
            return redirect(url_for('show_class', class_name = class_name))

#-----------------------------------------------------------------------------#
@app.route("/main_admin", methods=['POST', 'GET'])
def main_admin():
    cur.execute('select * from user_app')
    data = cur.fetchall()
    return render_template('main_student.html', users = data) 


## REPORTES

#1 Grafica de barras con definitivas (estudiantes por cada rango de notas)
#2 Grafica de lineas con definitivas (estudiantes por cada rango de notas) para cada grupo
#3 Grafica de lineas con progreso cortes estudiantes 



if __name__ == "__main__":
    app.run(port = 2000, debug = True)