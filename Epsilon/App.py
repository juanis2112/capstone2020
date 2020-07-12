#!/usr/bin/env python3
"""
Webapp that allows browsing, modifying, analysing student data.
"""

# Standard library imports
import base64
from io import BytesIO
from pathlib import Path
import tempfile

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
                        database="Epsilon_13")
cur = conn.cursor()
app = Flask(__name__)
app.secret_key = 'mysecretkey'


# --- Util Functions --------------------------------------------------------------------------------
def count_alerts(user_name):
    cur.execute("""SELECT count(*)
                    FROM alertas
                    WHERE
                        usuario = %s AND
                        visto_estudiante = '0' """, (user_name,))
    count = int(cur.fetchone()[0])
    return count


def count_admin_alerts():
    cur.execute("""SELECT count(*)
                    FROM alertas
                    WHERE
                        visto_admin = '0' """)
    count = int(cur.fetchone()[0])
    return count


def get_student_grades(user_name, class_name):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
            nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2+
                                porcentaje3*nota3+porcentaje4*nota4+
                                porcentaje5*nota5)/100,2)
            FROM RESUMEN
            WHERE
                prof_usr = %s AND
                nombre_asignatura = %s AND
                anio = (SELECT max(anio) FROM RESUMEN) AND
                periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                        (SELECT max(anio) FROM RESUMEN))
            ORDER BY(nombre_est)""", (user_name, class_name)
                )
    grades = cur.fetchall()
    return grades


def get_student_grades_period(user_name, class_name, year, period):
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
    grades = cur.fetchall()
    return grades


def get_name_from_user(user_name):
    cur.execute("""SELECT nombre, apellido_1, apellido_2
                    FROM personas
                    WHERE usuario = %s""", (user_name,))
    name = cur.fetchone()
    return name


def plot_groups(data, groups_data):
    N = 10
    width = 0.4
    ind = np.arange(N)
    plt.figure(figsize=(12, 10))
    sns.set(font_scale=0.8)
    ax = plt.subplot(111)
    plot = []
    color = ['r', 'b', 'g']
    for idx, data in enumerate(groups_data):
        df = pd.DataFrame(data, columns=['user', 'student', 'last_name1', 'last_name2', 'grade1',
                                         'grade2', 'grade3', 'grade4', 'grade5', 'grade_final'])
        df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
        conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
        y = [i for i in conteo_promedio]
        plot.append(ax.bar(ind+idx*0.4, y, width=0.4, align='center', color=color[idx]))
    ax.set_ylabel('Numero de estudiantes')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(['(0, 0.5]', '(0.5, 1]', '(1, 1.5]', '(1.5, 2]', '(2, 2.5]', '(2.5, 3]',
                        '(3, 3.5]', '(3.5, 4]', '(4, 4.5]', '(4.5, 5]'])
    ax.legend((plot[0][0], plot[1][0]), ('grupo1', 'grupo2'))
    return ax


def generate_image():
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    image = base64.b64encode(figfile.getvalue()).decode('utf-8')
    return image


# --- Login Window --------------------------------------------------------------------------------

@app.route("/")
def main_window(): 
    try:
        cur.execute("SELECT * from personas")
        conn.commit()
    except:
        conn.rollback()
        with open('../datos_prueba/creacion_bd.sql', 'r') as sqlFile:
                print(sqlFile)
                cur.execute(sqlFile.read())      
                conn.commit()    
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['passwd']
        # Verify username is on the database
        try:
            cur.execute("SELECT usuario FROM personas WHERE usuario=%s", (username_input,))
            cur.execute("SELECT contrasena FROM personas WHERE usuario=%s", (username_input,))
            passwd = str(cur.fetchone()[0])
            if password_input != passwd:
                flash('La contraseña es incorrecta', 'error')
                return render_template('login.html')

            cur.execute("SELECT tipo FROM personas WHERE usuario=%s", (username_input,))
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
    cur.execute("""SELECT
                    nombre_asignatura,nota1,nota2,nota3,nota4,nota5,
                    round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+
                    porcentaje4*nota4+porcentaje5*nota5)/100,2)
                FROM RESUMEN
                WHERE
                    est_usr = %s AND
                    anio = (SELECT max(anio) FROM RESUMEN) AND
                    periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio
                            = (SELECT max(anio) FROM RESUMEN))
                    ORDER BY(nombre_asignatura)""", (user_name,))
    data = cur.fetchall()
    cur.execute("""SELECT
                    round(sum(creditos_asignatura*round((porcentaje1*nota1+
                    porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+
                    porcentaje5*nota5)/100,2))/sum(creditos_asignatura),2)
                    as promedio_semestral
                FROM RESUMEN
                WHERE
                    est_usr = %s AND
                    anio = (SELECT max(anio) FROM RESUMEN) AND
                    periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                             (SELECT max(anio) FROM RESUMEN));""", (user_name,)
                )
    average = float(cur.fetchone()[0])
    count = count_alerts(user_name)
    return render_template('/student/main_student.html', classes=data, user_name=user_name,
                           promedio=average, count=count)


@app.route("/student_data/<string:user_name>", methods=['POST', 'GET'])
def personal_data(user_name):
    cur.execute("""SELECT codigo, nombre, apellido_1, apellido_2,
                correo_institucional, documento_actual FROM personas
                WHERE
                    usuario = %s""", (user_name,))
    data = cur.fetchall()[0]
    count = count_alerts(user_name)
    return render_template('/student/student_data.html', student_data=data, user_name=user_name,
                           count=count)


@app.route("/academic_history/<string:user_name>", methods=['POST', 'GET'])
def academic_history(user_name):
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE est_usr = %s
                ORDER BY anio DESC, periodo DESC""", (user_name,))
    periods = cur.fetchall()
    count = count_alerts(user_name)
    return render_template('/student/academic_history.html', user_name=user_name, periods = periods,
                           count=count)


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
    count = count_alerts(user_name)
    return render_template('/student/period_classes.html', classes=data, user_name=user_name,
                           count=count, year=year, period=period)



# - Teacher Page ----------------------------------------------------------------------------------
@app.route("/main_teacher/<string:user_name>", methods=['POST', 'GET'])
def main_teacher(user_name):
    cur.execute("""SELECT DISTINCT nombre_asignatura
                    FROM RESUMEN
                    WHERE
                        prof_usr = %s AND
                        anio = (SELECT max(anio) FROM RESUMEN) AND
                        periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio
                                = (SELECT max(anio) FROM RESUMEN))
                    ORDER BY(nombre_asignatura)    """, (user_name,))
    data = cur.fetchall()
    return render_template('/teacher/main_teacher.html', classes=data, user_name=user_name)


@app.route("/class/<string:user_name>/<string:class_name>", methods=['POST', 'GET'])
def show_class(user_name, class_name,):
    data = get_student_grades(user_name, class_name)
    return render_template('/teacher/class.html', user_name=user_name,
                           students_class=data, class_name=class_name)


@app.route("/class_edit/<string:user_name>/<string:class_name>", methods=['POST', 'GET'])
def edit_grade(user_name, class_name):
    students_class = get_student_grades(user_name, class_name)
    return render_template('/teacher/class_edit.html', user_name=user_name,
                           class_name=class_name,
                           students_class=students_class)


@app.route("/class_update/<string:user_name>/<string:class_name>", methods=['POST'])
def update_grade(class_name, user_name):
    students_class = get_student_grades(user_name, class_name)
    for student in students_class:
        grades = list(student[4:-1])
        for idx, grade in enumerate(grades):
            new_grade = float(request.form['grade%s_%s' % (idx+1, student[0])])
            if float(grade) != new_grade:
                grades[idx] = new_grade
                student_alerts(student[0], class_name, new_grade)
        cur.execute("""UPDATE toma
                    SET
                        nota1 = %s,
                        nota2 = %s,
                        nota3 = %s,
                        nota4 = %s,
                        nota5 = %s
                    WHERE
                        toma.sem_id = (
                            SELECT sem_id
                            FROM RESUMEN
                            WHERE
                                prof_usr = %s AND
                                nombre_asignatura = %s AND
                                RESUMEN.est_usr = %s AND
                                anio = (SELECT max(anio) FROM RESUMEN) AND
                                periodo = (SELECT max(periodo) FROM RESUMEN
                               WHERE anio = (SELECT max(anio) FROM RESUMEN))
                                ) AND
                                toma.codigo = (
                                    SELECT distinct est_cod
                                    FROM RESUMEN
                                    WHERE
                                        est_usr = %s)""",
                    (*grades, user_name, class_name,
                     student[0], student[0]))
        conn.commit()
    return redirect(url_for('show_class', user_name=user_name,
                                class_name=class_name))

@app.route("/class_history/<string:user_name>", methods=['POST', 'GET'])
def class_history(user_name):
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE prof_usr = %s
                ORDER BY anio DESC, periodo DESC""", (user_name,))
    periods = cur.fetchall()
    return render_template('/teacher/class_history.html', user_name=user_name, periods = periods)

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
    return render_template('/teacher/historic_teacher.html', classes=data, user_name=user_name, year=year, period=period)

@app.route("/class/<string:user_name>/<string:class_name>/<string:year><string:period>", methods=['POST', 'GET'])
def show__historic_class(user_name, class_name, year, period):
    data = get_student_grades_period(user_name, class_name, year, period)
    return render_template('/teacher/historic_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, year=year,
                           period=period)


# --- Admin Page ----------------------------------------------------------------------------------
@app.route("/main_admin", methods=['POST', 'GET'])
def main_admin():
    count = count_admin_alerts()
    return render_template('/admin/main_admin.html', count=count)


# ---- Admin: Students Page -----------------------------------------------------------------------
@app.route("/students", methods=['POST', 'GET'])
def load_students():
    cur.execute("""SELECT usuario, nombre, apellido_1, apellido_2 FROM personas
                WHERE tipo='estudiante'""")
    data = cur.fetchall()
    data_complete = []
    cur.execute("""SELECT count(*)
                    FROM alertas
                    WHERE
                        visto_admin = '0' """)
    count = int(cur.fetchone()[0])
    for user in data:
        user_info = list(user)
        cur.execute("""SELECT
                        round(sum(creditos_asignatura*(nota1*porcentaje1+nota2*porcentaje2+nota3*
                        porcentaje3+nota4*porcentaje4+nota5*porcentaje5)/100)/sum(creditos_asignatura),2)
                        FROM RESUMEN
                        WHERE est_usr = %s""", (user[0],))
        promedio1 = cur.fetchone()
        if (None in promedio1):
            promedio = ''
        else:
            promedio = float(promedio1[0])
        cur.execute("""SELECT sum(creditos_asignatura) as creditos FROM resumen
                    WHERE est_usr = %s""", (user[0],))
        credito_suma = float(cur.fetchone()[0])
        user_info.append(credito_suma)
        user_info.append(promedio)
        data_complete.append(user_info)
    return render_template('/admin/admin_students.html', students=data_complete,
                           count=count)

@app.route("/admin_main_student/<string:user_name>", methods=['POST', 'GET'])
def admin_main_student(user_name):
    cur.execute("""SELECT nombre_asignatura,nota1,nota2,nota3,nota4,nota5,
                round((porcentaje1*nota1+porcentaje2*nota2+porcentaje3*nota3+
                       porcentaje4*nota4+porcentaje5*nota5)/100,2)
                    FROM RESUMEN
                    WHERE
                        est_usr = %s AND
                        anio = (SELECT max(anio) FROM RESUMEN) AND
                        periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio
                                = (SELECT max(anio) FROM RESUMEN))
                    ORDER BY(nombre_asignatura)""", (user_name,))
    data = cur.fetchall()
    count = count_admin_alerts()
    student = get_name_from_user(user_name)
    return render_template('/admin/student/main_student.html', classes=data,
                           user_name=user_name, count=count, student=student)

@app.route("/admin_student_data/<string:user_name>", methods=['POST', 'GET'])
def admin_personal_data(user_name):
    cur.execute("""SELECT codigo, nombre, apellido_1, apellido_2,
                correo_institucional, documento_actual FROM personas
                WHERE
                    usuario = %s""", (user_name,))
    data = cur.fetchall()[0]
    count = count_admin_alerts()
    return render_template('/admin/student/student_data.html', student_data=data, user_name=user_name,
                           count=count)

@app.route("/admin_academic_history/<string:user_name>", methods=['POST', 'GET'])
def admin_academic_history(user_name):
    cur.execute("""SELECT
                        distinct cast(anio as varchar),cast(periodo as varchar),
                        round(sum(creditos_asignatura*(nota1*porcentaje1+nota2*
                        porcentaje2+nota3*porcentaje3+nota4*porcentaje4+nota5*
                        porcentaje5)/100)/sum(creditos_asignatura),2),
                        sum(creditos_asignatura)
                    FROM RESUMEN
                    WHERE est_usr = %s
                    GROUP BY(anio,periodo)
                    ORDER BY anio DESC, periodo DESC
                    """, (user_name,))
    periods = cur.fetchall()
    count = count_admin_alerts()
    student = get_name_from_user(user_name)
    return render_template('/admin/student/academic_history.html', user_name=user_name, periods=periods,
                           count=count, student=student)

@app.route("/admin_period_classes/<string:user_name>/<string:year>/<string:period>", methods=['POST', 'GET'])
def admin_period_classes(user_name, year, period):
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
    count = count_admin_alerts()
    return render_template('/admin/student/period_classes.html', classes=data, user_name=user_name,
                           count=count, year=year, period=period)

# ---- Admin: Teachers Page -----------------------------------------------------------------------
@app.route("/teachers", methods=['POST', 'GET'])
def load_teachers():
    cur.execute("""SELECT usuario, nombre, apellido_1, apellido_2 FROM personas
                WHERE tipo='profesor' or tipo='administrador'""")
    data = cur.fetchall()
    count = count_admin_alerts()
    return render_template('admin/admin_teachers.html', teachers=data, count=count)


@app.route("/admin_main_teacher/<string:user_name>", methods=['POST', 'GET'])
def admin_main_teacher(user_name):
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE prof_usr = %s
                ORDER BY anio DESC, periodo DESC""", (user_name,))
    periods = cur.fetchall()
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('/admin/teacher/main_teacher.html', user_name=user_name,
                           periods=periods, teacher=teacher, count=count)

@app.route("/admin_teacher_classes/<string:user_name>/<string:year><string:period>", methods=['POST', 'GET'])
def admin_teacher_classes(user_name, year, period):
    cur.execute("""SELECT DISTINCT nombre_asignatura
                    FROM RESUMEN
                    WHERE
                        prof_usr = %s AND
                        anio = %s AND
                        periodo = %s
                    ORDER BY(nombre_asignatura)""", (user_name, year, period))
    data = cur.fetchall()
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('admin/teacher/historic_teacher.html', classes=data, user_name=user_name,
                           teacher=teacher, year=year, period=period, count=count)


@app.route("/admin_teacher_class/<string:user_name>/<string:class_name>/<string:year><string:period>", methods=['POST', 'GET'])
def admin_show_class(user_name, class_name, year, period):
    data = get_student_grades_period(user_name, class_name, year, period)
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('/admin/teacher/historic_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, teacher=teacher,
                           count=count)


# ---- Admin: Classes Page ------------------------------------------------------------------------
@app.route("/classes", methods=['POST', 'GET'])
def load_classes():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (SELECT max(anio) FROM RESUMEN) AND
                periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                        (SELECT max(anio) FROM RESUMEN))
            ORDER BY(nombre_asignatura)""")
    data = cur.fetchall()
    count = count_admin_alerts()
    return render_template('/admin/admin_classes.html', classes=data, count=count)


@app.route("/groups/<string:class_name>", methods=['POST', 'GET'])
def load_groups(class_name):
    cur.execute("""SELECT distinct nombre_asignatura,grupo,prof_usr,
                nombre_prof,ap1_prof,ap2_prof
                FROM RESUMEN
                WHERE
                    nombre_asignatura = %s AND
                    anio = (SELECT max(anio) FROM RESUMEN) AND
                    periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                            (SELECT max(anio) FROM RESUMEN))
                ORDER BY(grupo)""", (class_name,))
    data = cur.fetchall()
    count = count_admin_alerts()
    return render_template('/admin/admin_groups.html', groups=data, count=count)


@app.route("/admin_show_group_class/<string:user_name>/<string:class_name>/grupo<string:group>/", methods=['POST', 'GET'])
def admin_show_group_class(user_name, class_name, group):
    data = get_student_grades(user_name, class_name)
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('/admin/admin_show_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, teacher=teacher,
                           count=count, group=group)


@app.route("/admin_classes_edit/", methods=['POST', 'GET'])
def admin_edit_class():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (SELECT max(anio) FROM RESUMEN) AND
                periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                        (SELECT max(anio) FROM RESUMEN))
            ORDER BY(nombre_asignatura)""")
    classes = cur.fetchall()
    count = count_admin_alerts()
    return render_template('/admin/admin_classes_edit.html', classes=classes,
                           count=count)


@app.route("/admin_classes_update", methods=['POST'])
def admin_update_class():
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = (SELECT max(anio) FROM RESUMEN) AND
                periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                        (SELECT max(anio) FROM RESUMEN))
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
                       FROM RESUMEN WHERE
                        RESUMEN.anio = (SELECT max(RESUMEN.anio)
                       FROM RESUMEN) AND
                        RESUMEN.periodo = (SELECT max(RESUMEN.periodo)
                       FROM RESUMEN WHERE RESUMEN.anio =
                       (SELECT max(RESUMEN.anio) FROM RESUMEN)) AND
                    RESUMEN.nombre_asignatura = %s)""",
                    (credit, per1, per2, per3, per4, per5, class_name[0]))
        conn.commit()
    return redirect(url_for('load_classes', classes=classes))


@app.route("/admin_functions/",methods=['POST', 'GET'])
def admin_functions():
    count = count_admin_alerts()
    return render_template('admin/admin_functions.html', count=count)
    
@app.route("/admin_functions/import_students",methods=['POST', 'GET'])
def import_students():
    count = count_admin_alerts()
    return render_template('admin/import_students.html', count=count)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['inputfile']
    
    csv_file_path = Path('../datos_prueba/temp_data.csv').resolve()
    with open(csv_file_path, mode='wb') as csv_file:
        csv_file.write(file.read())
    csv_file_path.chmod(0o777) 
    
    with open('../datos_prueba/insercion_datos.sql', 'r', encoding='utf-8') as insercion_sql:
        sqlFile = insercion_sql.read().format(str(csv_file_path), '1', '2018')
        cur.execute(sqlFile)      
        conn.commit()
    count = count_admin_alerts()
    return render_template('admin/import_success.html', count=count)
    

# ---- Admin: Reports -----------------------------------------------------------------------------
@app.route("/class_report/<string:user_name>/<string:class_name>/<string:year><string:period>/", methods=['POST', 'GET'])
def one_group_report(user_name, class_name,  year, period):
    data = get_student_grades_period(user_name, class_name, year, period)
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
    image = generate_image()
    plt.close()
    count = count_admin_alerts()
    return render_template('admin/class_report.html', image=image, count=count)


@app.route("/student_report/<string:user_name>/<string:year><string:period>/", methods=['POST', 'GET'])
def student_report(user_name, year, period):
    cur.execute("""SELECT
                     round(sum(creditos_asignatura*nota1)/sum(creditos_asignatura),1)
                     as promedio_cohorte1,
                     round(sum(creditos_asignatura*nota2)/sum(creditos_asignatura),1)
                     as promedio_cohorte2,
                     round(sum(creditos_asignatura*nota3)/sum(creditos_asignatura),1)
                     as promedio_cohorte3,
                     round(sum(creditos_asignatura*nota4)/sum(creditos_asignatura),1)
                     as promedio_cohorte4,
                     round(sum(creditos_asignatura*nota5)/sum(creditos_asignatura),1)
                     as promedio_cohorte5,
                     round(sum(creditos_asignatura*round((porcentaje1*nota1+
                        porcentaje2*nota2+porcentaje3*nota3+porcentaje4*nota4+
                        porcentaje5*nota5)/100,2))/sum(creditos_asignatura),1)
                     as promedio_semestral
                FROM RESUMEN
                WHERE
                     est_usr = %s AND
                     anio = %s AND
                     periodo = %s;""", (user_name, year, period)
                )
    data = cur.fetchall()
    x = ['Corte1', 'Corte2', 'Corte3', 'Corte4', 'Corte5', 'Nota final']
    plt.plot(x, data[0], marker='o')
    plt.xlabel('Cortes')
    plt.ylabel('Promedio')
    data = get_name_from_user(user_name)
    student = (str(data[0])+' '+str(data[1])+' '+str(data[2]))
    plt.title('Promedio de notas estudiante %s periodo %s-%s' % (student, year, period))
    image = generate_image()
    plt.close()
    count = count_admin_alerts()
    return render_template('/admin/student/students_report.html', image=image, count=count)


@app.route("/student_historic_report/<string:user_name>/", methods=['POST', 'GET'])
def student_historic_report(user_name):
    cur.execute("""SELECT
                    distinct cast(anio as varchar),cast(periodo as varchar),
                    round(sum(creditos_asignatura*(nota1*porcentaje1+nota2*
                        porcentaje2+nota3*porcentaje3+nota4*porcentaje4+nota5*
                        porcentaje5)/100)/sum(creditos_asignatura),1)
                FROM RESUMEN
                WHERE est_usr = %s
                GROUP BY(anio,periodo)""", (user_name,))
    data = cur.fetchall()
    x = []
    y = []
    for period in data:
        x.append(str(period[0])+'-'+str(period[1]))
    for period in data:
        y.append(period[2])
    plt.plot(x, y, marker='o')
    plt.xlabel('Cortes')
    plt.ylabel('Promedio')
    data = get_name_from_user(user_name)
    student = (str(data[0])+' '+str(data[1])+' '+str(data[2]))
    plt.title('Promedio de notas estudiante %s' % student)
    historic_report = generate_image()
    plt.close()
    count = count_admin_alerts()
    return render_template('/admin/student/students_report.html',
                           image=historic_report, count=count)

@app.route("/groups_report/<string:class_name>/", methods=['POST', 'GET'])
def groups_report(class_name):
    cur.execute("""SELECT distinct nombre_asignatura,grupo
                FROM RESUMEN
                WHERE
                    nombre_asignatura = %s AND
                    anio = (SELECT max(anio) FROM RESUMEN) AND
                    periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio = (SELECT max(anio) FROM RESUMEN))
                ORDER BY(grupo)""", (class_name,))
    data = cur.fetchall()
    groups_data = []
    for group in data:
        cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                            nota4,nota5,round((porcentaje1*nota1+porcentaje2*nota2+
                            porcentaje3*nota3+porcentaje4*nota4+porcentaje5*nota5)/100,2)
                     FROM RESUMEN
                     WHERE
                        nombre_asignatura = %s AND
                        grupo = %s AND
                        anio = (SELECT max(anio) FROM RESUMEN) AND
                        periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio = (SELECT max(anio) FROM RESUMEN))
                     ORDER BY(nombre_est)""", (class_name, group[1])
                    )
        groups_data.append(cur.fetchall())
    plot_groups(data, groups_data)
    image = generate_image()
    plt.close()
    count = count_admin_alerts()
    return render_template('/admin/groups_report.html', image=image, count=count)


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
            alert_student = "Tiene una alerta de nota muy baja en la materia "+class_name
            alert_admin= "El Estudiante "+ student +  " tiene una alerta de nota muy baja, en la materia " +  class_name
            alert_type ='ALTA'
        cur.execute("""insert into alertas (usuario, texto, tipo, fecha, periodo,
                    anio, nombre_asignatura, visto_estudiante)
                    values (%s,%s,%s, CURRENT_TIMESTAMP,
                            '1', '2020', %s, '0' )""", (student, alert_student, alert_type, class_name))
        conn.commit()


# ---- Admin: Alert -----------------------------------------------------------------------------
@app.route("/student_alerts/<string:user_name>/", methods=['POST', 'GET'])
def show_alerts(user_name):
    cur.execute("""SELECT * FROM alertas
                    WHERE usuario=%s AND
                    visto_admin  = '0'
                    ORDER BY fecha DESC""", (user_name,))
    unread_alerts = cur.fetchall()
    cur.execute("""SELECT * FROM alertas
                    WHERE usuario=%s AND
                    visto_admin = '1'
                    ORDER BY fecha DESC;""", (user_name,))
    read_alerts = cur.fetchall()
    return render_template('/student/student_alert.html', unread_alerts=unread_alerts,
                           read_alerts=read_alerts, user_name=user_name)


@app.route("/student_alerts/", methods=['POST', 'GET'])
def show_admin_alerts():
    cur.execute("""SELECT
                    nombre,apellido_1,apellido_2,texto,alertas.tipo
                    as alerta,fecha,periodo,anio,nombre_asignatura
                    FROM alertas join personas
                    on alertas.usuario = personas.usuario""")
    alerts = cur.fetchall()
    conn.commit()
    return render_template('/admin/admin_alert.html', alerts=alerts)


if __name__ == "__main__":
    app.run(port=2000, debug=True, use_reloader=False)
