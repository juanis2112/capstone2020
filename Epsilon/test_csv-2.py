def logging(usuario,action,sobre_que = None,sobre_quien = None,asignatura = None,grupo = None,cuando = None,notas_antes = None,notas_despues = None):
    
    f = lambda word: "'"+word+"'"

    date = str(time.strftime('%Y-%m-%d %H:%M:%S'))
    print(date)

    if action == "INICIO" :
        text = "El usuario " + usuario + "ha iniciado sesion."
        # Insercion en login
    elif action == "SALIDA":
        text = "El usuario " + usuario + "ha cerrado sesion."
        # Insercion en login
    elif action == 'CONSULTA':
        text = "El usuario " + usuario + " realizo una consulta en " + sobre_que + (" acerca de  " + sobre_quien  if sobre_quien != None else "") +(" grupo "+grupo if grupo!=None else "")+ (" en el periodo " + cuando if cuando != None else "")
        # Insercion en login.
    elif action == 'EDICION':
        text = "El usuario " + usuario + " realizo una edicion sobre " + sobre_que + ( " a " + sobre_quien if sobre_quien != None else "" ) +(" en "+asignatura+" grupo "+grupo if grupo!=None else "")+ ("en el periodo " + cuando if cuando != None else "")+(" se cambiaron las notas "+("".join([str(n)+',' if n!=None else "" for n in notas_antes]))+" por las notas "+("".join([str(n)+',' if n!=None else "" for n in notas_despues])) if sobre_que=="NOTAS" else "")
    elif action == 'IMPORTAR' :
        text = "El usuario "+ usuario + " importo un archivo sobre "+ sobre_que + ", acerca de "+(sobre_quien if sobre_quien!=None else "")+(" grupo "+grupo if grupo!=None else "")+" para el periodo "+cuando
    elif action == 'EXPORTAR' :
        text = "El usuario "+usuario+" exporto un archivo sobre "+sobre_que+", acerca de "+(sobre_quien if sobre_quien!=None else "")+("en "+asignatura+" grupo "+grupo if grupo!=None else "")+" para el periodo "+cuando
    elif action == 'ALERTA':
        text == "El usuario "+usuario+ "genero una alerta sobre "+sobre_que+" acerca de "+sobre_quien+(" en "+asignatura+" grupo "+grupo if grupo!=None else "")+" para el periodo "+cuando
    else:
        text = "El usuario "+usuario+" hizo halgo"

    cur.execute("INSERT INTO loggin VALUES(%s,%s,%s)" %(f(usuario),f(date),f(text)))
