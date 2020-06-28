<form action="{{url_for('main_student', user_name = user_name)}}" method="POST">
  <!DOCTYPE html>
  <html lang="en">
  <style>

  a:link {
    color: white;
    background-color: transparent;
    text-decoration: none;
  }
  a:visited {
    color: white;
    background-color: transparent;
    text-decoration: none;
  }
  a:hover {
    color: green;
    background-color: transparent;
    text-decoration: underline;
  }
  a:active {
    color: green;
    background-color: transparent;
    text-decoration: underline;
  }
  </style>
  <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>Document</title>
      <link rel="stylesheet" href="{{ url_for('static', filename='styletemplate.css') }}" />
  </head>
  <body>
      <div>
          <div class="header">
              <img class="top-logo" src="{{ url_for('static', filename='template_general/imagenes/campana.png') }}">
              <a href="{{ url_for('main_window') }}">
                <img type="image" src="{{ url_for('static', filename='template_general/imagenes/logoout.jpg') }}" class="top-logo">
              </a>
          </div>
          <div class="row">
              <div class="col-3 menu">
              <ul>
                <a href="{{url_for('load_students')}}">
                      <li>
                        <div class="menu-box">
                          <div >
                            Estudiantes
                          </div>
                        <img src="{{ url_for('static', filename='template_general/imagenes/student.png') }}" width="30px" width="30px" style="background-color:white ;">
                        </div>
                      </li>
                </a>
                <a href="{{url_for('load_teachers')}}">
                      <li>
                        <div class="menu-box">
                          <div >
                            Profesores
                          </div>
                        <img src="{{ url_for('static', filename='template_general/imagenes/profesorbien.png') }}" width="30px" width="30px" style="background-color:white ;">
                        </div>
                      </li>
                </a>
                <a href="{{url_for('load_classes')}}">
                      <li>
                        <div class="menu-box">
                          <div >
                            Materias
                          </div>
                        <img src="{{ url_for('static', filename='template_general/imagenes/materia.png') }}" width="30px" width="30px" style="background-color:white ;">
                        </div>
                      </li>
                </a>
                <a href="{{url_for('main_window')}}">
                      <li>
                        <div class="menu-box">
                          <div >
                            Alertas
                          </div>
                        <img src="{{ url_for('static', filename='template_general/imagenes/campana.png') }}" width="30px" width="30px" style="background-color:white ;">
                        </div>
                      </li>
                </a>
              </ul>
              </div>
        <div class="col-9">
          <a href="{{url_for('admin_main_teacher', user_name = user_name)}}" class="btn">
              <img src="{{ url_for('static', filename='template_general/imagenes/retorno.png') }}" height="13px" width="13px">
          </a>
        <ul>
          <p>
          {% if image != None %}
          <img src="data:image/png;base64,{{ image }}">
          {% endif %}
          </p>
        </ul>
        </div>
      </div>
    </div>
  <script>
  function habilitar(){
      var casillas_notas=document.getElementsByClassName("table-toggle");
      for(var i=0;i<casillas_notas.length;i++){
          casillas_notas[i].readOnly=false;
      }
      document.getElementById("boton-editar").style.backgroundColor="#073D72";
      document.getElementById("boton-editar").setAttribute("onclick","deshabilitar()");
  }

  function deshabilitar(){
      var casillas_notas=document.getElementsByClassName("table-toggle");
      for(var i=0;i<casillas_notas.length;i++){
          casillas_notas[i].readOnly=true;
      }
      document.getElementById("boton-editar").style.backgroundColor="white";
      document.getElementById("boton-editar").setAttribute("onclick","habilitar()");
  }
  </script>
  </body>
  </html>
</form>