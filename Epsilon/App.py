#!/usr/bin/env python3
"""
Webapp that allows browsing, modifying, analysing student data.
"""

# Standard library imports
import base64
from io import BytesIO

# Third party imports
from flask import flash, Flask, redirect, render_template, request, url_for
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import seaborn as sns

# Connection to DataBase
conn = psycopg2.connect(user="postgres",
                        password="Jgrccgv",
                        host="localhost",
                        port="5432",
                        database="Epsilon_5")
cur = conn.cursor()
app = Flask(__name__)
app.secret_key = 'mysecretkey'


# --- Login Window --------------------------------------------------------------------------------
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
            cur.execute("select usuario from personas where usuario='"+username_input+"'")
            cur.execute("select contrasena from personas where usuario='"+username_input+"'")
            passwd = str(cur.fetchone()[0])
            if password_input != passwd:
                flash('La contraseña es incorrecta', 'error')
                return render_template('login.html')

            cur.execute("select tipo from personas where usuario='"+username_input+"'")
            usertype_input = str(cur.fetchone()[0])

            # Get user type to know what main_window to open
            if usertype_input == 'administrador':
                return redirect(url_for('main_admin'))
            elif usertype_input == 'profesor':
                return redirect(url_for('main_teacher', user_name=username_input))
            else:
                return redirect(url_for('main_student', user_name=username_input))

        except Exception:
            flash('El usuario no se encuentra registrado', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')


# --- Student Page --------------------------------------------------------------------------------
@app.route("/main_student/<string:user_name>", methods=['POST', 'GET'])
def main_student(user_name):
    cur.execute("""SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5,
                round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+
                       porcentaje4*nota4+porcentaje5*nota5)/100,2)
                    FROM RESUMEN
                    WHERE
                        est_usr = %s AND
                        anio = (select max(anio) from RESUMEN) AND
                        periodo = (select max(periodo) from RESUMEN where anio
                                = (select max(anio) from RESUMEN))
                    ORDER BY(nombre_asignatura)""", (user_name,))
    data = cur.fetchall()
    #Consulta de el numero de alertas
    return render_template('main_student.html', classes=data, user_name=user_name)

@app.route("/student_data/<string:user_name>", methods=['POST', 'GET'])
def personal_data(user_name):
    cur.execute("""SELECT codigo, nombre, apellido_1, apellido_2, 
                correo_institucional, documento_actual from personas 
                WHERE
                    usuario = %s""", (user_name,))
    data = cur.fetchall()[0]
    return render_template('student_data.html', student_data=data, user_name=user_name)

@app.route("/academic_history/<string:user_name>", methods=['POST', 'GET'])
def academic_history(user_name):    
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE est_usr = %s""", (user_name,))
    periods = cur.fetchall()
    return render_template('academic_history.html', user_name=user_name, periods = periods)

@app.route("/period_classes/<string:user_name>/<string:year>/<string:period>", methods=['POST', 'GET'])
def period_classes(user_name, year, period):
    cur.execute("""SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5,
                    round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+
                       porcentaje4*nota4+porcentaje5*nota5)/100,2)
                    FROM RESUMEN
                    WHERE 
                    	est_usr = %s AND
                    	anio = %s AND
                    	periodo = %s
                    ORDER BY(nombre_asignatura);""", (user_name, year, period))
    data = cur.fetchall()
    #Consulta del numero de alertas
    return render_template('period_classes.html', classes=data, user_name=user_name)
    


# - Teacher Page ----------------------------------------------------------------------------------
@app.route("/main_teacher/<string:user_name>", methods=['POST', 'GET'])
def main_teacher(user_name):
    cur.execute("""SELECT DISTINCT nombre_asignatura
                    FROM RESUMEN
                    WHERE
                        prof_usr = %s AND
                        anio = (select max(anio) from RESUMEN) AND
                        periodo = (select max(periodo) from RESUMEN where anio
                                = (select max(anio) from RESUMEN))
                    ORDER BY(nombre_asignatura)    """, (user_name,))
    data = cur.fetchall()
    return render_template('main_teacher.html', classes=data, user_name=user_name)


@app.route("/class/<string:user_name>/<string:class_name>", methods=['POST', 'GET'])
def show_class(user_name, class_name,):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5,round((porcentaje1*nota1+porcentaje2*nota2+
                                   porcentaje3*nota3+porcentaje4*nota4+
                                   porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    prof_usr = %s AND
                    nombre_asignatura = %s AND
                    anio = (select max(anio) from RESUMEN) AND
                    periodo = (select max(periodo) from RESUMEN where anio =
                            (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    data = cur.fetchall()
    return render_template('class.html', user_name=user_name,
                           students_class=data, class_name=class_name)


@app.route("/class_edit/<string:user_name>/<string:class_name>", methods=['POST', 'GET'])
def edit_grade(user_name, class_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2+
                                    porcentaje3*nota3+porcentaje4*nota4+
                                    porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    prof_usr = %s AND
                    nombre_asignatura = %s AND
                    anio = (select max(anio) from RESUMEN) AND
                    periodo = (select max(periodo) from RESUMEN where anio =
                            (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    students_class = cur.fetchall()
    return render_template('class_edit.html', user_name=user_name,
                           class_name=class_name,
                           students_class=students_class)


@app.route("/class_update/<string:user_name>/<string:class_name>", methods=['POST'])
def update_grade(class_name, user_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5,round((porcentaje1*nota1+porcentaje2*nota2+
                                   porcentaje3*nota3+porcentaje4*nota4+
                                   porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    prof_usr = %s AND
                    nombre_asignatura = %s AND
                    anio = (select max(anio) from RESUMEN) AND
                    periodo = (select max(periodo) from RESUMEN where anio =
                            (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    students_class = cur.fetchall()
    for student in students_class:
        grade1 = float(request.form['grade1_'+student[0]])
        grade2 = float(request.form['grade2_'+student[0]])
        grade3 = float(request.form['grade3_'+student[0]])
        grade4 = float(request.form['grade4_'+student[0]])
        grade5 = float(request.form['grade5_'+student[0]])
        
        grades = [grade1, grade2, grade3, grade4, grade5]
        for grade in grades:
             student_alerts(student[0], class_name, grade)          
        
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
                                periodo = (select max(periodo) from RESUMEN
                               where anio = (select max(anio) from RESUMEN))
                                ) AND
                                toma.codigo = (
                                    select distinct est_cod
                                    from RESUMEN
                                    where
                                        est_usr = %s)""",
                    (grade1, grade2, grade3, grade4, grade5, user_name, class_name,
                     student[0], student[0]))
        conn.commit()
            
            
            
            
    return redirect(url_for('show_class', user_name=user_name,
                                class_name=class_name))

@app.route("/class_history/<string:user_name>", methods=['POST', 'GET'])
def class_history(user_name):    
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE prof_usr = %s""", (user_name,))
    periods = cur.fetchall()
    return render_template('class_history.html', user_name=user_name, periods = periods)

@app.route("/classes/<string:user_name>/<string:year><string:period>", methods=['POST', 'GET'])
def classes(user_name, year, period):
    cur.execute("""SELECT DISTINCT nombre_asignatura
                    FROM RESUMEN
                    WHERE
                    	prof_usr = %s AND
                    	anio = %s AND
                    	periodo = %s
                    ORDER BY(nombre_asignatura)""", (user_name, year, period))
    data = cur.fetchall()
    #Consulta del numero de alertas
    return render_template('historic_teacher.html', classes=data, user_name=user_name, year=year, period=period)
    
@app.route("/class/<string:user_name>/<string:class_name>/<string:year><string:period>", methods=['POST', 'GET'])
def show__historic_class(user_name, class_name, year, period):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5,round((porcentaje1*nota1+porcentaje2*nota2+
                                   porcentaje3*nota3+porcentaje4*nota4+
                                   porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    prof_usr = %s AND
                    nombre_asignatura = %s AND
                    anio = %s AND
                    periodo = %s
                ORDER BY(nombre_est)""", (user_name, class_name, year, period)
                )
    data = cur.fetchall()
    return render_template('historic_class.html', user_name=user_name,
                           students_class=data, class_name=class_name)


# --- Admin Page ----------------------------------------------------------------------------------
@app.route("/main_admin", methods=['POST', 'GET'])
def main_admin():
     #Consulta de el numero de alertas 
    return render_template('main_admin.html')


# ---- Admin: Students Page -----------------------------------------------------------------------
@app.route("/students", methods=['POST', 'GET'])
def load_students():
    cur.execute("""select usuario, nombre, apellido_1, apellido_2 from personas
                where tipo='estudiante'""")
    data = cur.fetchall()
    data_complete = []
    for user in data:
        user_info = list(user)
        cur.execute("""select
                     round(sum(creditos_asignatura*round((porcentaje1*nota1+
                      porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+
                      porcentaje5*nota5)/100,2))/sum(creditos_asignatura),2)
                     as promedio_semestral
                from RESUMEN
                where
                     est_usr = %s AND
                     anio = (select max(anio) from RESUMEN) AND
                     periodo = (select max(periodo) from RESUMEN where anio =
                             (select max(anio) from RESUMEN));""", (user[0],)
                    )
        promedio1 = cur.fetchone()
        if (None in promedio1):
            promedio = ''
        else: 
            promedio = float(promedio1[0])
        cur.execute("""select sum(creditos_asignatura) as creditos from resumen
                    group by(nombre_est,est_cod)""")
        credito_suma = float(cur.fetchone()[0])
        user_info.append(credito_suma)
        user_info.append(promedio)
        data_complete.append(user_info)
    return render_template('students.html', students=data_complete)


# ---- Admin: Teachers Page -----------------------------------------------------------------------
@app.route("/teachers", methods=['POST', 'GET'])
def load_teachers():
    cur.execute("""select usuario, nombre, apellido_1, apellido_2 from personas
                where tipo='profesor' or tipo='administrador'""")
    data = cur.fetchall()
    return render_template('teachers.html', teachers=data)

@app.route("/admin_main_teacher/<string:user_name>", methods=['POST', 'GET'])
def admin_main_teacher(user_name):   
    print(user_name)
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE prof_usr = %s""", (user_name,))
    periods = cur.fetchall()
    print(periods)
    return render_template('main_teacher_admin.html', user_name=user_name, periods = periods)

@app.route("/class_admin/<string:user_name>/<string:class_name>", methods=['POST', 'GET'])
def admin_show_class(user_name, class_name,):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2+
                                    porcentaje3*nota3+porcentaje4*nota4+
                                    porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    prof_usr = %s AND
                    nombre_asignatura = %s AND
                    anio = (select max(anio) from RESUMEN) AND
                    periodo = (select max(periodo) from RESUMEN where anio =
                            (select max(anio) from RESUMEN))
                ORDER BY(nombre_est)""", (user_name, class_name)
                )
    data = cur.fetchall()
    return render_template('class_admin.html', user_name=user_name,
                           students_class=data, class_name=class_name)


# ---- Admin: Classes Page ------------------------------------------------------------------------
@app.route("/classes", methods=['POST', 'GET'])
def load_classes():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (select max(anio) from RESUMEN) AND
                periodo = (select max(periodo) from RESUMEN where anio =
                        (select max(anio) from RESUMEN))
            ORDER BY(nombre_asignatura)""")
    data = cur.fetchall()
    return render_template('classes.html', classes=data)


@app.route("/groups/<string:class_name>", methods=['POST', 'GET'])
def load_groups(class_name):
    cur.execute("""SELECT distinct nombre_asignatura,grupo,prof_usr,
                nombre_prof,ap1_prof,ap2_prof
                FROM RESUMEN
                WHERE
                    nombre_asignatura = %s AND
                    anio = (select max(anio) from RESUMEN) AND
                    periodo = (select max(periodo) from RESUMEN where anio =
                            (select max(anio) from RESUMEN))
                ORDER BY(grupo)""", (class_name,))
    data = cur.fetchall()
    return render_template('groups.html', groups=data)


@app.route("/admin_classes_edit/", methods=['POST', 'GET'])
def admin_edit_class():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (select max(anio) from RESUMEN) AND
                periodo = (select max(periodo) from RESUMEN where anio =
                        (select max(anio) from RESUMEN))
            ORDER BY(nombre_asignatura)""")
    classes = cur.fetchall()
    return render_template('admin_classes_edit.html', classes=classes)


@app.route("/admin_classes_update", methods=['POST'])
def admin_update_class():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (select max(anio) from RESUMEN) AND
                periodo = (select max(periodo) from RESUMEN where anio =
                        (select max(anio) from RESUMEN))
            ORDER BY(nombre_asignatura)""")
    classes = cur.fetchall()
    for class_name in classes:
        credit = int(request.form['credit_'+class_name[1]])
        per1 = int(request.form['term1_'+class_name[1]])
        per2 = int(request.form['term2_'+class_name[1]])
        per3 = int(request.form['term3_'+class_name[1]])
        per4 = int(request.form['term4_'+class_name[1]])
        per5 = int(request.form['term5_'+class_name[1]])
        cur.execute("""UPDATE asignaturas
                    SET
                        creditos_asignatura = %s,
                    porcentaje1 = %s,
                    porcentaje2 = %s,
                        porcentaje3 = %s,
                        porcentaje4 = %s,
                    porcentaje5 = %s
                    WHERE
                    codigo_asignatura = (SELECT distinct codigo_asignatura
                       from RESUMEN WHERE
                        RESUMEN.anio = (select max(RESUMEN.anio)
                       from RESUMEN) AND
                        RESUMEN.periodo = (select max(RESUMEN.periodo)
                       from RESUMEN where RESUMEN.anio =
                       (select max(RESUMEN.anio) from RESUMEN)) AND
                    RESUMEN.nombre_asignatura = %s)""",
                    (credit, per1, per2, per3, per4, per5, class_name[0]))
        conn.commit()
    return redirect(url_for('load_classes', classes=classes))


# ---- Admin: Reports -----------------------------------------------------------------------------
@app.route("/class_report/<string:class_name>/<string:user_name>", methods=['POST', 'GET'])
def one_group_report(class_name, user_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,
                nota3,nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2
                                          +porcentaje3*nota3+porcentaje4*nota4
                                          +porcentaje5*nota5)/100,2)
                 FROM RESUMEN
                 WHERE
                     prof_usr = %s AND
                     nombre_asignatura = %s AND
                     anio = (select max(anio) from RESUMEN) AND
                     periodo = (select max(periodo) from RESUMEN where anio =
                             (select max(anio) from RESUMEN))
                 ORDER BY(nombre_est)""", (user_name, class_name)
                )
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['user', 'student', 'last_name1',
                                     'last_name2', 'grade1', 'grade2',
                                     'grade3', 'grade4', 'grade5', 'grade_final'])
    df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
    conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
    plt.figure(figsize=(8, 6))
    sns.set(font_scale=1.2)
    ax = conteo_promedio.plot.bar(
        x="Promedio Final", y="Numero Estudiantes",
        rot=50, title="Nota final estudiantes Curso %s" % class_name)
    ax.set(
        ylabel="Numero estudiantes",
        xlabel="Promedio Final",
        )

    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue()).decode('utf-8')
    plt.close()
    return render_template('class_report.html', image=figdata_png)


@app.route("/student_report/<string:user_name>/", methods=['POST', 'GET'])
def student_report(user_name):
    cur.execute("""select
                     round(sum(creditos_asignatura*nota1)/sum(creditos_asignatura),2)
                     as promedio_cohorte1,
                     round(sum(creditos_asignatura*nota2)/sum(creditos_asignatura),2)
                     as promedio_cohorte2,
                     round(sum(creditos_asignatura*nota3)/sum(creditos_asignatura),2)
                     as promedio_cohorte3,
                     round(sum(creditos_asignatura*nota4)/sum(creditos_asignatura),2)
                     as promedio_cohorte4,
                     round(sum(creditos_asignatura*nota5)/sum(creditos_asignatura),2)
                     as promedio_cohorte5,
                     round(sum(creditos_asignatura*round((porcentaje1*nota1+
                        porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+
                        porcentaje5*nota5)/100,2))/sum(creditos_asignatura),2)
                     as promedio_semestral
                from RESUMEN
                where
                     est_usr = %s AND
                     anio = (select max(anio) from RESUMEN) AND
                     periodo = (select max(periodo) from RESUMEN where anio =
                             (select max(anio) from RESUMEN));""", (user_name,)
                )
    data = cur.fetchall()
    x = ['Corte1', 'Corte2', 'Corte3', 'Corte4', 'Corte5', 'Nota final']
    plt.plot(x, data[0], marker='o')
    plt.xlabel('Cortes')
    plt.ylabel('Promedio')
    plt.title('Promedio de notas estudiante')
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    image = base64.b64encode(figfile.getvalue()).decode('utf-8')
    plt.close()
    return render_template('students_report.html', image=image)

@app.route("/groups_report/<string:class_name>/", methods=['POST', 'GET'])
def groups_report(class_name):
    cur.execute("""SELECT distinct nombre_asignatura,grupo
                FROM RESUMEN 
                WHERE 
                	nombre_asignatura = %s AND
                	anio = (select max(anio) from RESUMEN) AND
                	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                ORDER BY(grupo)""", (class_name,))
    data = cur.fetchall()
    groups_data =[]
    for group in data:
        cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+porcentaje5*nota5)/100,2)
                     FROM RESUMEN 
                     WHERE
                     	nombre_asignatura = %s AND
                        grupo = %s AND
                     	anio = (select max(anio) from RESUMEN) AND
                     	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                     ORDER BY(nombre_est)""" , (class_name, group[1])
                     )                    
        groups_data.append(cur.fetchall())  
    N = 10
    width = 0.4
    ind = np.arange(N)
    plt.figure(figsize=(12,10))
    sns.set(font_scale=0.8)
    ax = plt.subplot(111)
    plot = []
    color = ['r','b','g']
    for idx, data in enumerate(groups_data):
        df = pd.DataFrame(data, columns =['user', 'student','last_name1', 'last_name2', 'grade1', 'grade2', 'grade3', 'grade4','grade5', 'grade_final'])
        df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
        conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
        #x = [i.left for i in conteo_promedio.index]
        y = [i for i in conteo_promedio]
        plot.append(ax.bar(ind+idx*0.4, y, width=0.4, align='center', color=color[idx]))
    ax.set_ylabel('Numero de estudiantes')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(['(0, 0.5]', '(0.5, 1]', '(1, 1.5]', '(1.5, 2]', '(2, 2.5]', '(2.5, 3]', '(3, 3.5]', '(3.5, 4]', '(4, 4.5]', '(4.5, 5]'])
    ax.legend( (plot[0][0], plot[1][0]), ('grupo1', 'grupo2') )    
    #plt.savefig("Ejemplo1.png")
    plt.tight_layout
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    image = base64.b64encode(figfile.getvalue()).decode('utf-8')
    plt.close()
    return render_template('groups_report.html', image=image) 


def student_alerts(student, class_name, grade):
    #Consulta de la nota final (grade_final)
    if grade < 2: #row[corte] es la nota de la materia del estudiante ne esa asignatura
        #Consulta que mete el string a la base de datos    
        if grade >= 1:
            alert_student = "Tiene una alerta de nota baja en la materia"+class_name
            alert_admin= "El Estudiante "+ student +  " tiene una alerta de nota baja, en la materia " +  class_name
            alert_type = 'MEDIA'
        if grade < 1:
            #Consulta que mete el string a la base de datos    
            alert_student = "Tiene una alerta de nota muy baja en la materia"+class_name
            alert_admin= "El Estudiante "+ student +  " tiene una alerta de nota muy baja, en la materia " +  class_name
            alert_type ='ALTA'
        cur.execute("""insert into alarmas (usuario, texto, tipo, fecha, periodo, 
                    anio, nombre_asignatura) 
                    values (%s,%s,%s, CURRENT_TIMESTAMP, 
                            '1', '2020', %s )""", (student, alert_student, alert_type, class_name))
        conn.commit()

@app.route("/student_alerts/<string:user_name>/", methods=['POST', 'GET'])
def show_alerts(user_name):
    cur.execute("""SELECT * from alarmas
                    where usuario=%s""",(user_name,))
    alerts = cur.fetchall()
    #Consulta que guarda en una variable las alertas del estudiante student
    return render_template('student_alert.html', alerts=alerts) 

@app.route("/student_alerts/", methods=['POST', 'GET'])
def show_admin_alerts():
    cur.execute("""SELECT * from alarmas""")
    alerts = cur.fetchall()
    return render_template('admin_alert.html', alerts=alerts) 


if __name__ == "__main__":
    app.run(port=2000, debug=True, use_reloader=False)
