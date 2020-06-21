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
                        database = "CAPSTONE")
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
        print(username_input)
        # Verify username is on the database
        try: 
            cur.execute("select usuario from personas where usuario='"+username_input+"'")
            cur.execute("select contrasena from personas where usuario='"+username_input+"'")
            passwd =  str(cur.fetchone()[0])
            if password_input != passwd:
                flash("La contraseña es incorrecta")
                return render_template('login.html')
            
            else:   
                cur.execute("select tipo from personas where usuario='"+username_input+"'")
                usertype_input =  str(cur.fetchone()[0])
                
                # Get user type to know what main_window to open
                if usertype_input == 'administrador':
                    return redirect(url_for('main_admin'))
                elif usertype_input == 'profesor':
                    return redirect(url_for('main_teacher',user_name = username_input))
                else:
                    return redirect(url_for('main_student',user_name = username_input))
        
        except: 
            flash("El usuario no se encuentra registrado")
            return render_template('login.html')


#-----------------------------------------------------------------------------#

@app.route("/main_student/<string:user_name>", methods=['POST', 'GET'])
def main_student(user_name):
    #FALTA LA NOTA FINAL
    user_name = str(user_name)
    cur.execute("""SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5 
            FROM semestre,curso_sem,toma,asignaturas,(personas join estudiante on personas.codigo = estudiante.codigo)
            WHERE 
            	semestre.sem_id = toma.sem_id AND
            	semestre.sem_id = curso_sem.sem_id AND
            	anio = (select max(anio) from semestre) AND
            	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre)) AND
            	curso_sem.codigo_asignatura = asignaturas.codigo_asignatura AND
            	estudiante.codigo =( 
            		select estudiante.codigo 
            		from personas,estudiante 
            		where 
            			personas.codigo = estudiante.codigo AND
            			usuario = '%s')""" % user_name)
    data = cur.fetchall()
    return render_template('main_student.html', classes = data, user_name = user_name)       
    
#-----------------------------------------------------------------------------#

@app.route("/main_teacher/<string:user_name>", methods=['POST', 'GET'])
def main_teacher(user_name):
    cur.execute("""SELECT nombre_asignatura
            FROM semestre,curso_sem,dicta,asignaturas,(personas join empleado on personas.codigo = empleado.codigo)
            WHERE 
            	semestre.sem_id = dicta.sem_id AND
            	semestre.sem_id = curso_sem.sem_id AND
            	anio = (select max(anio) from semestre) AND
            	periodo = (select max(periodo) from semestre where anio = (select max(anio) from semestre)) AND
            	curso_sem.codigo_asignatura = asignaturas.codigo_asignatura AND
            	empleado.codigo =( 
            		select empleado.codigo 
            		from personas,empleado 
            		where 
            			personas.codigo = empleado.codigo AND
            			usuario = '%s')""" % user_name)
    data = cur.fetchall()
    return render_template('main_teacher.html', classes = data, user_name = user_name) 

@app.route('/class/<string:class_name>', methods = ['POST', 'GET'])
def show_class(class_name):
    #query para crear tabla que muestra los estudiantes en orden alfabetico inscritos en la materia seleccionada
    #dictada por el profesor seleccionado (nombre de usuario)
    cur.execute(f"select * FROM students WHERE class_name = '{class_name}'")
    data = cur.fetchall()
    final_grade = 3
    return render_template('class.html', students_class = data, class_name=class_name, NotaFinal = final_grade)    
    

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
    df = pd.DataFrame(students_class, columns =['user', 'student', 'class_name', 'grade1', 'grade2', 'grade3', 'grade4','grade5','grade_final'])
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
            grade4 = request.form['grade4_'+student[0]]
            grade5 = request.form['grade5_'+student[0]]
            grade_final = str(round((float(grade1)+float(grade2)+float(grade3)+float(grade4)+float(grade5))/3,2))
            cur.execute("""
                UPDATE students
                SET nota1 = %s,
                    nota2 = %s,
                    nota3 = %s,
                    grade_final = %s
                WHERE username = %s and class_name = %s
            """, (grade1, grade2, grade3, grade_final, student[0], class_name))
            conn.commit()
            return redirect(url_for('show_class', class_name = class_name))

#-----------------------------------------------------------------------------#
@app.route("/main_admin", methods=['POST', 'GET'])
def main_admin():
    return render_template('main_admin.html') 

@app.route("/students", methods=['POST', 'GET'])
def load_students():
    cur.execute("select usuario, nombre, apellido_1, apellido_2 from personas where tipo='estudiante'")
    data = cur.fetchall()
    return render_template('students.html', students = data) 

@app.route("/teachers", methods=['POST', 'GET'])
def load_teachers():
    cur.execute("select usuario, nombre, apellido_1, apellido_2 from personas where tipo='profesor' or tipo='administrador'")
    data = cur.fetchall()
    return render_template('teachers.html', teachers = data) 

@app.route("/classes", methods=['POST', 'GET'])
def load_classes():
    cur.execute("select nombre_asignatura, codigo_asignatura, creditos_asignatura from asignaturas")
    data = cur.fetchall()
    return render_template('classes.html', classes = data) 


## REPORTES

#1 Grafica de barras con definitivas (estudiantes por cada rango de notas)
#2 Grafica de lineas con definitivas (estudiantes por cada rango de notas) para cada grupo
#3 Grafica de lineas con progreso cortes estudiantes 



if __name__ == "__main__":
    app.run(port = 2000, debug = True, use_reloader=False)
    
    
    
    
    
    
    
    
    