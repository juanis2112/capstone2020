#!/usr/bin/env python3
"""
Webapp that allows browsing, modifying, analysing student data.
"""

# Standard library imports
import base64
from io import BytesIO
from pathlib import Path
import secrets

# Third party imports
from flask import flash, Flask, redirect, render_template, request, url_for
import flask_login
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import psycopg2
import seaborn as sns
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Connection to DataBase
conn = psycopg2.connect(user="postgres",
                        password="Jgrccgv",
                        host="localhost",
                        port="5432",
                        database="Epsilon",)

conn.set_session(autocommit=True)
cur = conn.cursor()
app = Flask(__name__)
app.secret_key = secrets.token_bytes(nbytes=16)

login_manager=flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id
        

@login_manager.user_loader
def load_user(user_id):
    try:
        cur.execute("SELECT usuario FROM personas WHERE usuario=%s", (user_id,))
        return User(user_id)
    except Exception:
        return None     
        
        
    
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


def get_student_grades(user_name, class_name, group):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
            nota4,nota5, round((porcentaje1*nota1+porcentaje2*nota2+
                                porcentaje3*nota3+porcentaje4*nota4+
                                porcentaje5*nota5)/100,2)
            FROM RESUMEN
            WHERE
                prof_usr = %s AND
                nombre_asignatura = %s AND
                grupo = %s AND
                anio = (SELECT max(anio) FROM RESUMEN) AND
                periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio =
                        (SELECT max(anio) FROM RESUMEN))
            ORDER BY(nombre_est)""", (user_name, class_name, group)
                )
    grades = cur.fetchall()
    return grades


def get_student_grades_period(user_name, class_name, year, period, group):
    cur.execute("""SELECT est_usr,nombre_est,ap1_est,ap2_est,nota1,nota2,nota3,
                nota4,nota5,round((porcentaje1*nota1+porcentaje2*nota2+
                                   porcentaje3*nota3+porcentaje4*nota4+
                               porcentaje5*nota5)/100,2)
            FROM RESUMEN
            WHERE
                prof_usr = %s AND
                nombre_asignatura = %s AND
                anio = %s AND
                periodo = %s AND
                grupo = %s
            ORDER BY(nombre_est)""", (user_name, class_name, year, period, group)
                )
    grades = cur.fetchall()
    return grades


def get_name_from_user(user_name):
    cur.execute("""SELECT nombre, apellido_1, apellido_2
                    FROM personas
                    WHERE usuario = %s""", (user_name,))
    name = cur.fetchone()
    return name


def plot_groups(data, groups_data, class_name):
    N = 10
    width = 0.4
    ind = np.arange(N)
    plt.figure(figsize=(10, 6))
    sns.set(font_scale=0.8)
    ax = plt.subplot(111)
    plots = []
    color = ['r', 'b', 'g']
    for idx, data in enumerate(groups_data):
        df = pd.DataFrame(data, columns=['user', 'student', 'last_name1', 'last_name2', 'grade1',
                                         'grade2', 'grade3', 'grade4', 'grade5', 'grade_final'])
        df["grupo_promedio"] = pd.cut(df['grade_final'], bins=[n * 0.5 for n in range(11)])
        conteo_promedio = df['grupo_promedio'].groupby([df['grupo_promedio']]).count()
        y = [i for i in conteo_promedio]
        plots.append(ax.bar(ind+idx*0.4, y, width=0.4, align='center', color=color[idx]))
    ax.set_ylabel('Numero de estudiantes')
    ax.set_title("Nota final estudiantes curso %s" % class_name)
    ax.set_xticks(ind+width)
    ax.set_xticklabels(['(0, 0.5]', '(0.5, 1]', '(1, 1.5]', '(1.5, 2]', '(2, 2.5]', '(2.5, 3]',
                        '(3, 3.5]', '(3.5, 4]', '(4, 4.5]', '(4.5, 5]'])

    plot_legend = [plot[0] for plot in plots]
    name_legend = ['Grupo %s' % str(i+1) for i in range(len(plots))]
    ax.legend(plot_legend, name_legend)
    return ax


def generate_image():
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    image = base64.b64encode(figfile.getvalue()).decode('utf-8')
    return image

def send_email(username,email,codigo):
    sender_email = "EpsilonAppUR@gmail.com"
    receiver_email = email
    password = "macc123*"

    message = MIMEMultipart("alternative")
    message["Subject"] = "Ingreso a la APP Epsilon"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    HTML = """\
                <html>
                <body>
                    <p>Bienvenido a la app Epsilon. Su usuario y contraseña son:<br>
                    User: %s <br>
                    Password: %s <br> 
                    <a href="http://www.realpython.com">Epsilon </a> 
                    para cambiar la contraseña.
                    </p>
                </body>
                </html>
                """%(username,codigo)

    # Turn these into plain/html MIMEText objects
    part2 = MIMEText(HTML, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part2) 

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )


def render_main_windows(user_name):
    cur.execute("SELECT esAdmin,esProfesor FROM personas JOIN empleado ON personas.codigo = empleado.codigo WHERE usuario= %s;", (user_name,))
    aux = cur.fetchone()
    if (None is aux):
        return redirect(url_for('main_student', user_name=user_name))
    else:
        aux = list(aux)
        is_admin, is_teacher = aux

        # Get user type to know what main_window to open
        if is_admin and is_teacher:
            return render_template('admin/admin_teacher.html', user_name= user_name)
        elif is_admin:
            return redirect(url_for('main_admin'))
        else:
            return redirect(url_for('main_teacher', user_name=user_name))
      
        
def upload_file(file, path_to_file, data_insertion_path, **kwargs):    
    csv_file_path = Path(path_to_file).resolve()
    with open(csv_file_path, mode='wb') as csv_file:
        csv_file.write(file.read())
    csv_file_path.chmod(0o777) 
    with open(data_insertion_path, 'r', encoding='utf-8') as insercion_sql:
        sqlFile = insercion_sql.read().format(path=str(csv_file_path), **kwargs)
        cur.execute(sqlFile)      
         

# --- Login Window --------------------------------------------------------------------------------

@app.route("/")
def main_window(): 
    try:
        cur.execute("SELECT * from personas")
         
    except:
        conn.rollback()
        with open('../datos_prueba/creacion_bd_2.sql', 'r') as sqlFile:
                cur.execute(sqlFile.read())      
                     
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username_input = request.form['username']
        password_input = request.form['passwd']
        # Verify username is on the database
        user = load_user(username_input)
        if not user:
            flash('El usuario no se encuentra registrado o la contraseña es incorrecta', 'error')
            return render_template('login.html')
        cur.execute("SELECT contrasena = crypt(%s, contrasena) FROM personas WHERE usuario = %s;", (password_input, username_input))
        passwd = str(cur.fetchone()[0])
        if passwd == 'False':
            flash('El usuario no se encuentra registrado o la contraseña es incorrecta', 'error')
            return render_template('login.html')
        flask_login.login_user(user)
        # Realizar consulta del login para saber si es la primera vez que se ingresa
        first_time = False
        if first_time:
            return render_template('/change_passwd.html', user_name=username_input)
        else:
            return render_main_windows(username_input)        
    else:
        return render_template('login.html')

@app.route("/change_passwd/<string:user_name>", methods=['POST','GET'])
@flask_login.login_required
def change_passwd(user_name):
    password_input = request.form['passwd']
    password_input_conf = request.form['passwd_conf']
    if password_input != password_input_conf:
        flash('Las contraseña no coinciden', 'error')
        return render_template('change_passwd.html')
    else:
        cur.execute("""UPDATE personas set contrasena = crypt(%s,gen_salt('xdes')) 
                    where usuario = %s; """, (password_input_conf,user_name))
        flash('La contraseña fue cambiada', 'error')
        return render_main_windows(user_name)


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))
        

# --- Student Page --------------------------------------------------------------------------------

@app.route("/main_student/<string:user_name>", methods=['POST', 'GET'])
@flask_login.login_required
def main_student(user_name):
    cur.execute("""SELECT
                    nombre_asignatura, nota1,nota2,nota3,nota4,nota5,
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
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
def main_teacher(user_name):
    cur.execute("""SELECT DISTINCT nombre_asignatura, grupo
                    FROM RESUMEN
                    WHERE
                        prof_usr = %s AND
                        anio = (SELECT max(anio) FROM RESUMEN) AND
                        periodo = (SELECT max(periodo) FROM RESUMEN WHERE anio
                                = (SELECT max(anio) FROM RESUMEN))
                    ORDER BY(nombre_asignatura)    """, (user_name,))
    data = cur.fetchall()
    return render_template('/teacher/main_teacher.html', classes=data, user_name=user_name)


@app.route("/class/<string:user_name>/<string:class_name>/grupo:<string:group>", methods=['POST', 'GET'])
@flask_login.login_required
def show_class(user_name, class_name, group):
    data = get_student_grades(user_name, class_name, group)
    return render_template('/teacher/class.html', user_name=user_name,
                           students_class=data, class_name=class_name, group=group)


@app.route("/class_edit/<string:user_name>/<string:class_name>/grupo:<string:group>", methods=['POST', 'GET'])
@flask_login.login_required
def edit_grade(user_name, class_name, group):
    students_class = get_student_grades(user_name, class_name, group)
    return render_template('/teacher/class_edit.html', user_name=user_name,
                           class_name=class_name,
                           students_class=students_class, group=group)


@app.route("/class_update/<string:user_name>/<string:class_name>/grupo:<string:group>", methods=['POST'])
@flask_login.login_required
def update_grade(class_name, user_name, group):
    students_class = get_student_grades(user_name, class_name, group)
    for student in students_class:
        grades = list(student[4:-1])
        for idx, grade in enumerate(grades):
            new_grade = float(request.form['grade%s_%s' % (idx+1, student[0])])
            if float(grade) != new_grade:
                grades[idx] = new_grade
                student_alerts(student[0], class_name, new_grade)
        cur.execute("""UPDATE toma
                        SET -- Las 'nueva nota' se reemplazan por la nueva nota NUMERICA NO STRING
                        	nota1 = %s,
                        	nota2 = %s,
                        	nota3 = %s,
                        	nota4 = %s,
                        	nota5 = %s
                        WHERE	
                        	codigo_asignatura = (select distinct codigo_asignatura from RESUMEN where nombre_asignatura = %s) AND
                        	codigo = (select distinct est_cod from RESUMEN where est_usr = %s) AND 
                        	grupo = (
                        		select distinct grupo
                        		from RESUMEN
                        		where 
                        			prof_usr = %s AND
                        			nombre_asignatura = %s AND
                        			anio = (select max(anio) from RESUMEN) AND
                        			periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))
                        	) AND
                        	anio = (select max(anio) from RESUMEN) AND
                        	periodo = (select max(periodo) from RESUMEN where anio = (select max(anio) from RESUMEN))""",
                    (*grades, class_name, student[0], user_name, class_name))
    return redirect(url_for('show_class', user_name=user_name,
                                class_name=class_name, group=group))

@app.route("/class_history/<string:user_name>", methods=['POST', 'GET'])
@flask_login.login_required
def class_history(user_name):
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM resumen
                WHERE prof_usr = %s
                ORDER BY anio DESC, periodo DESC""", (user_name,))
    periods = cur.fetchall()
    return render_template('/teacher/class_history.html', user_name=user_name, periods = periods)

@app.route("/classes/<string:user_name>/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def classes(user_name, year, period):
    cur.execute("""SELECT DISTINCT nombre_asignatura, grupo
                    FROM RESUMEN
                    WHERE
                        prof_usr = %s AND
                        anio = %s AND
                        periodo = %s
                    ORDER BY(nombre_asignatura)""", (user_name, year, period))
    data = cur.fetchall()
    return render_template('/teacher/historic_teacher.html', classes=data, user_name=user_name, year=year, period=period)

@app.route("/class/<string:user_name>/<string:class_name>/grupo:<string:group>/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def show__historic_class(user_name, class_name, year, period, group):
    data = get_student_grades_period(user_name, class_name, year, period, group)
    return render_template('/teacher/historic_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, year=year,
                           period=period)


# --- Admin Page ----------------------------------------------------------------------------------
@app.route("/main_admin", methods=['POST', 'GET'])
@flask_login.login_required
def main_admin():
    count = count_admin_alerts()
    return render_template('/admin/main_admin.html', count=count)


# ---- Admin: Students Page -----------------------------------------------------------------------
@app.route("/students", methods=['POST', 'GET'])
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
def load_teachers():
    cur.execute("""SELECT usuario, nombre, apellido_1, apellido_2 FROM personas
                WHERE tipo='profesor' or tipo='administrador'""")
    data = cur.fetchall()
    count = count_admin_alerts()
    return render_template('admin/admin_teachers.html', teachers=data, count=count)


@app.route("/admin_main_teacher/<string:user_name>", methods=['POST', 'GET'])
@flask_login.login_required
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

@app.route("/admin_teacher_classes/<string:user_name>/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def admin_teacher_classes(user_name, year, period):
    cur.execute("""SELECT DISTINCT nombre_asignatura, grupo
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


@app.route("/admin_teacher_class/<string:user_name>/<string:class_name>/grupo:<string:group>/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def admin_show_class(user_name, class_name, year, period, group):
    data = get_student_grades_period(user_name, class_name, year, period, group)
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('/admin/teacher/historic_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, teacher=teacher,
                           count=count, year=year, period=period)


# ---- Admin: Classes Page ------------------------------------------------------------------------
@app.route("/history_classes", methods=['POST', 'GET'])
@flask_login.login_required
def historic_class():
    cur.execute("""SELECT distinct cast(anio as varchar), cast(periodo as varchar)
                FROM semestre
                ORDER BY anio DESC, periodo DESC;""")
    data = cur.fetchall()
    print(data)
    count = count_admin_alerts()
    return render_template('/admin/historic_classes.html', periods=data, count=count)

@app.route("/classes/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def load_classes(year,period):
    cur.execute("""SELECT distinct nombre_asignatura,codigo_asignatura,
                creditos_asignatura, porcentaje1,
                porcentaje2,porcentaje3,porcentaje4,porcentaje5
            FROM RESUMEN
            WHERE
                anio = %s AND
                periodo = %s
            ORDER BY(nombre_asignatura)""",(year,period))
    data = cur.fetchall()
    count = count_admin_alerts()
    return render_template('/admin/admin_classes.html', classes=data, count=count)


@app.route("/groups/<string:class_name>", methods=['POST', 'GET'])
@flask_login.login_required
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
@flask_login.login_required
def admin_show_group_class(user_name, class_name, group):
    data = get_student_grades(user_name, class_name, group)
    teacher = get_name_from_user(user_name)
    count = count_admin_alerts()
    return render_template('/admin/admin_show_class.html', user_name=user_name,
                           students_class=data, class_name=class_name, teacher=teacher,
                           count=count, group=group)


@app.route("/admin_classes_edit/", methods=['POST', 'GET'])
@flask_login.login_required
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
@flask_login.login_required
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
         
    return redirect(url_for('load_classes', classes=classes))


@app.route("/admin_functions/",methods=['POST', 'GET'])
@flask_login.login_required
def admin_functions():
    count = count_admin_alerts()
    return render_template('admin/admin_functions.html', count=count)
    

@app.route("/admin_functions/import_data_from_file/<string:data_type>/",methods=['POST', 'GET'])
@flask_login.login_required
def import_data_from_file(data_type):
    
    count = count_admin_alerts()
    return render_template('admin/import_data_from_file.html', count=count, data_type=data_type)

@app.route("/admin_functions/import_data_from_file/<string:data_type>/<string:year>/<string:period>",methods=['POST', 'GET'])
@flask_login.login_required
def import_data_from_file_year(data_type, year, period):
    
    count = count_admin_alerts()
    return render_template('admin/import_data_from_file.html', count=count, data_type=data_type, year=year, period=period)


@app.route('/upload_teachers', methods=['POST'])
@flask_login.login_required
def upload_teachers():
    file = request.files['inputfile']
    upload_file(file, '../datos_prueba/temp_data_teachers.csv', '../datos_prueba/insercion_empleados.sql')
    cur.execute("""select usuario,correo_institucional,codigo from personas where tipo = 'profesor' """)
    users = cur.fetchall()
    # for user in users:
    #     send_email(user[0],user[1],user[2])
    count = count_admin_alerts()
    return render_template('admin/import_success.html', count=count)

@app.route('/upload_students', methods=['POST'])
@flask_login.login_required
def upload_students():
    period = request.form['period']
    year = request.form['year']
    file = request.files['inputfile']
    upload_file(file, '../datos_prueba/temp_data_students.csv', '../datos_prueba/insercion_estudiantes.sql', period=period, year=year)
    cur.execute("""select usuario,correo_institucional,codigo from personas where tipo = 'estudiante' """)
    users = cur.fetchall()
    # for user in users:
    #     send_email(user[0],user[1],user[2])
    count = count_admin_alerts()
    return redirect(url_for('import_data_from_file_year', data_type='classes', year=year, period=period))

@app.route("/upload_classes/<string:year>/<string:period>", methods=['POST'])
@flask_login.login_required
def upload_classes(year, period):
    file = request.files['inputfile']
    upload_file(file, '../datos_prueba/temp_data_classes.csv', '../datos_prueba/insercion_cursos_periodos.sql',period=period, year=year)
    count = count_admin_alerts()
    return render_template('admin/import_success.html', count=count)


# ---- Admin: Reports -----------------------------------------------------------------------------
@app.route("/class_report/<string:user_name>/<string:class_name>/grupo:<string:group>/<string:year>/<string:period>", methods=['POST', 'GET'])
@flask_login.login_required
def one_group_report(user_name, class_name,  year, period, group):
    data = get_student_grades_period(user_name, class_name, year, period, group)
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


@app.route("/student_report/<string:user_name>/<string:year>/<string:period>/", methods=['POST', 'GET'])
@flask_login.login_required
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
@flask_login.login_required
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
@flask_login.login_required
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
    plot_groups(data, groups_data, class_name)
    image = generate_image()
    plt.close()
    count = count_admin_alerts()
    return render_template('/admin/groups_report.html', image=image, count=count)


@flask_login.login_required
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
            alert_type ='ALTA'
        cur.execute("""insert into alertas (usuario, texto, tipo, fecha, periodo,
                    anio, nombre_asignatura, visto_estudiante, visto_admin)
                    values (%s,%s,%s, CURRENT_TIMESTAMP,
                            '1', '2020', %s, '0', '0')""", (student, alert_student, alert_type, class_name))
         


# ---- Admin: Alert -----------------------------------------------------------------------------
@app.route("/student_alerts/<string:user_name>/", methods=['POST', 'GET'])
@flask_login.login_required
def show_alerts(user_name):
    cur.execute("""SELECT * FROM alertas
                    WHERE usuario=%s AND
                    visto_estudiante = '0' AND
                    oculto_estudiante = '0'
                    ORDER BY fecha DESC""", (user_name,))
    unread_alerts = cur.fetchall()
    cur.execute("""SELECT * FROM alertas
                    WHERE usuario=%s AND
                    visto_estudiante = '1' AND
                    oculto_estudiante = '0'
                    ORDER BY fecha DESC;""", (user_name,))
    read_alerts = cur.fetchall()
    cur.execute("""UPDATE alertas
                    set visto_estudiante = '1'
                    WHERE usuario=%s AND
                    oculto_estudiante = '0'""", (user_name,))
    return render_template('/student/student_alert.html', unread_alerts=unread_alerts,
                           read_alerts=read_alerts, user_name=user_name, count='0')


@app.route("/admin_alerts/", methods=['POST', 'GET'])
@flask_login.login_required
def show_admin_alerts():
    cur.execute("""SELECT
                    nombre,apellido_1,apellido_2,texto,alertas.tipo
                    as alerta,fecha,periodo,anio,nombre_asignatura, alertas.usuario
                    FROM alertas join personas
                    on alertas.usuario = personas.usuario
                    WHERE
                    visto_admin = '0' AND
                    oculto_admin = '0'
                    ORDER BY fecha DESC""")
    unread_alerts = cur.fetchall()
    cur.execute("""SELECT
                    nombre,apellido_1,apellido_2,texto,alertas.tipo
                    as alerta,fecha,periodo,anio,nombre_asignatura, alertas.usuario
                    FROM alertas join personas
                    on alertas.usuario = personas.usuario
                    WHERE
                    visto_admin = '1' AND
                    oculto_admin = '0'
                    ORDER BY fecha DESC;""")
    read_alerts = cur.fetchall()
    cur.execute("""UPDATE alertas
                    set visto_admin = '1'
                    WHERE oculto_admin = '0'""")
    return render_template('/admin/admin_alert.html', unread_alerts=unread_alerts,
                           read_alerts=read_alerts, count='0')

@app.route("/delete_alerts/<string:user_name>/<string:date>//<string:user_type>/", methods=['POST', 'GET'])
@flask_login.login_required
def delete_alerts(user_name, date, user_type):
    if user_type=='admin':
        print("Hola")
        cur.execute(""" UPDATE alertas SET oculto_admin = '1' WHERE usuario = %s AND fecha = %s
        """, (user_name, date))
        return redirect(url_for('show_admin_alerts'))
    else:
        cur.execute(""" UPDATE alertas SET oculto_estudiante = '1' WHERE usuario = %s AND fecha = %s
        """, (user_name, date))
        return redirect(url_for('show_alerts', user_name = user_name))


if __name__ == "__main__":
    app.run(port=2000, debug=True, use_reloader=False)
