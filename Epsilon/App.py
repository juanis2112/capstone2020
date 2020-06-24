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
from io import BytesIO
import base64

# Connection to DataBase
conn = psycopg2.connect(user = "postgres",
                        password = "test",
                        host = "localhost",
                        port = "5432",
                        database = "capstone")
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
        
        except Exception: 
            flash("El usuario no se encuentra registrado")
            return render_template('login.html')


#-----------------------------------------------------------------------------#

@app.route("/main_student/<string:user_name>", methods=['POST', 'GET'])
def main_student(user_name):
    #FALTA LA NOTA FINAL
    cur.execute("""SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5
                    FROM RESUMEN
                    WHERE 
                    	est_usr = %s AND
                    	anio = (select max(anio) from RESUMEN) AND
                    	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                    ORDER BY(nombre_asignatura)""" , (user_name,))
    data = cur.fetchall()
    return render_template('main_student.html', classes = data, user_name = user_name)       
    
#-----------------------------------------------------------------------------#

@app.route("/main_teacher/<string:user_name>", methods=['POST', 'GET'])
def main_teacher(user_name):
    cur.execute("""SELECT DISTINCT nombre_asignatura
                    FROM RESUMEN
                    WHERE
                    	prof_usr = %s AND
                    	anio = (select max(anio) from RESUMEN) AND
                    	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                    ORDER BY(nombre_asignatura)	""", (user_name,))
    data = cur.fetchall()
    return render_template('main_teacher.html', classes = data, user_name = user_name) 

@app.route("/class/<string:user_name>/<string:class_name>", methods = ['POST', 'GET'])
def show_class(user_name, class_name,):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,nota4,nota5
                FROM RESUMEN 
                WHERE
                	prof_usr = %s AND
                	nombre_asignatura = %s AND
                	anio = (select max(anio) from RESUMEN) AND
                	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""" , (user_name, class_name)
                )
    data = cur.fetchall()
    final_grade = 3
    return render_template('class.html', user_name = user_name, students_class = data, class_name=class_name, final_grade = final_grade)    
    

@app.route("/class_edit/<string:user_name>/<string:class_name>", methods = ['POST','GET'])
def edit_grade(user_name, class_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,nota4,nota5
                FROM RESUMEN 
                WHERE
                	prof_usr = %s AND
                	nombre_asignatura = %s AND
                	anio = (select max(anio) from RESUMEN) AND
                	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    students_class = cur.fetchall()
    return render_template('class_edit.html', user_name = user_name, class_name = class_name, students_class = students_class)

@app.route("/class_update/<string:user_name>/<string:class_name>", methods=['POST'])
def update_grade(class_name, user_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,nota4,nota5
                FROM RESUMEN 
                WHERE
                	prof_usr = %s AND
                	nombre_asignatura = %s AND
                	anio = (select max(anio) from RESUMEN) AND
                	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    students_class = cur.fetchall()
    if request.method == 'POST':
        for student in students_class:
            grade1 = float(request.form['grade1_'+student[0]])
            grade2 = float(request.form['grade2_'+student[0]])
            grade3 = float(request.form['grade3_'+student[0]])
            grade4 = float(request.form['grade4_'+student[0]])
            grade5 = float(request.form['grade5_'+student[0]])
            grade_final = str(round((float(grade1)+float(grade2)+float(grade3)+float(grade4)+float(grade5))/3,2))
            cur.execute("""UPDATE toma
                        SET 
                        	nota1 = %s,
                        	nota2 = %s,
                        	nota3 = %s,
                        	nota4 = %s,
                        	nota5 = %s
                        WHERE	
                        	toma.sem_id = (
                        		select sem_id
                        		from RESUMEN
                        		where 
                        			prof_usr = %s AND 
                        			nombre_asignatura = %s AND 
                        			RESUMEN.est_usr = %s AND 
                        			anio = (select max(anio) from RESUMEN) AND
                        			periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                                	) AND 
                                	toma.codigo = (
                                		select distinct est_cod
                                		from RESUMEN
                                		where
                                			est_usr = %s)""", 
                (grade1, grade2, grade3, grade4, grade5, user_name, class_name, student[0], student[0]))
            conn.commit()
        return redirect(url_for('show_class', user_name = user_name, class_name = class_name, final_grade = grade_final))

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
    cur.execute("""SELECT distinct prof_usr, nombre_asignatura,codigo_asignatura,creditos_asignatura,grupo,porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5,nombre_prof, ap1_prof
            FROM RESUMEN
            WHERE
            	anio = (select max(anio) from RESUMEN) AND
            	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
            ORDER BY(nombre_asignatura)""")
    data = cur.fetchall()
    return render_template('classes.html', classes = data) 

@app.route("/class_report/<string:class_name>/<string:user_name>", methods=['POST', 'GET'])
def show_class_admin(class_name, user_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,nota4,nota5
                 FROM RESUMEN 
                 WHERE
                 	prof_usr = %s AND
                 	nombre_asignatura = %s AND
                 	anio = (select max(anio) from RESUMEN) AND
                 	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                 ORDER BY(nombre_est)""" , (user_name, class_name)
                 )
    data = cur.fetchall()
    df = pd.DataFrame(data, columns =['user', 'student','last_name1', 'last_name2', 'grade1', 'grade2', 'grade3', 'grade4','grade5'])
    df['grade_final'] = (df['grade1'] + df['grade2'] + df['grade3'] + df['grade4'] + df['grade5']) /5
    df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
    conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
    sns.set(font_scale=1.2)
    ax = conteo_promedio.plot.bar(x="Promedio Final", y="Numero Estudiantes", rot=50, title="Promedio estudiantes materia")
    ax.set(
        ylabel="Numero estudiantes",
        xlabel="Promedio Final",
        )
    
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
    return render_template('class_report.html', image=figdata_png) 
    
    


## REPORTES

#1 Grafica de barras con definitivas (estudiantes por cada rango de notas)
#2 Grafica de lineas con definitivas (estudiantes por cada rango de notas) para cada grupo
#3 Grafica de lineas con progreso cortes estudiantes 



if __name__ == "__main__":
    app.run(port = 2000, debug = True, use_reloader=False)
    
    
    
    
    
    
    
    
    