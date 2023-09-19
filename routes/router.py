from flask          import Blueprint, render_template, request, redirect, flash
from models.modelos import usuario, vehiculo, peticion
from utils.db       import db
from sqlalchemy.sql import text
from flask_login    import login_user, current_user, logout_user, login_required
from models.User    import User
from datetime       import datetime

import bcrypt
import re


nuberouter = Blueprint('nuberouter', __name__)

@nuberouter.route("/")
def base():
    return redirect("/informacion")

@nuberouter.route("/informacion")
def informacion():
    session = request.cookies.get('session')
    if session: return redirect("/vista_cliente")
    else:       return render_template("informacion.html")

@nuberouter.route("/regis", methods=['POST'])
def regis():
    nombres=request.form['nombres']
    apellido=request.form['apellido']
    numero=request.form['numero']
    email=request.form['email']
    clave=request.form['clave'] 
    
    if len(str(numero)) != 11:
        flash("El telefono debe contener 11 numeros")
        return redirect("/registro")
    
    hashed = bcrypt.hashpw(clave.encode('UTF-8'), bcrypt.gensalt())
    
    new_modelos = usuario(nombres, apellido, numero, email, hashed)
    
    db.session.add(new_modelos)
    db.session.commit()
        
    return redirect("/login")

@nuberouter.route("/registro")
def registro():
    session = request.cookies.get('session')
    if session: return redirect("/vista_cliente")
    else:       return render_template("/registro.html")

@nuberouter.route("/log", methods=['POST'])
def log():
    email=request.form['email']
    clave=request.form['clave'] 
    
    
    sql             = f"SELECT * FROM usuario WHERE email = '{email}';"
    usuario_valido  = db.session.execute(text(sql)) 
    usuario_valido  = list(usuario_valido)
    
    print(usuario_valido)
    print(clave)
    
    if len(usuario_valido):
        
        clave_codificada = clave.encode('UTF-8')
        
        if bcrypt.checkpw(clave_codificada, usuario_valido[0][5].encode('UTF-8')):
            user = User(usuario_valido[0][0], usuario_valido[0][1], usuario_valido[0][2], usuario_valido[0][3], usuario_valido[0][4], usuario_valido[0][5])
            login_user(user)
            if usuario_valido[0][6] == "cliente":
                return redirect("/vista_cliente")
        else:  
            flash("contraseña incorrecta")
            return redirect("/login") 
        
    else: 
        flash("el correo es incorrecto o el usuario no existe") 
        return redirect("/login")
    # return redirect("/formulario_mecanico")
@nuberouter.route("/login")
def login():
    session = request.cookies.get('session')
    if session: return redirect("/vista_cliente")
    else:       return render_template("/login.html")
    
@nuberouter.route("/vista_cliente", methods=['GET'])
def vista_cliente():
    session = request.cookies.get('session')
    print(current_user)
    if session: return render_template("/cliente.html", data=current_user)
    else:       return redirect("/informacion")


@nuberouter.route("/carro", methods=['POST'])
def carro():
    
    placa=request.form['placa'] 
    marca=request.form['marca']
    modelo=request.form['modelo']
    fecha=request.form['fecha']
    color=request.form['color']
    info=request.form['info']
     
    fecha_n=datetime.strptime(fecha, '%Y-%m-%d') 
    
    carro = vehiculo(placa=placa, marca=marca, modelo=modelo, fecha=fecha, color=color)
    db.session.add(carro)
    db.session.commit()
       
    sql             = f"SELECT * FROM vehiculo;"
    vehiculo_valido  = db.session.execute(text(sql)) 
    vehiculo_valido  = list(vehiculo_valido)
    ref = peticion(info=info, vehiculo=vehiculo_valido[-1][0], usuario=current_user['id'])
    db.session.add(ref)
    db.session.commit()
    
    return redirect("/vista_cliente")


@nuberouter.route("/exit")
def exit():
    logout_user()
    return redirect('/informacion')

@nuberouter.route("/respuesta")
def respuesta():
    print(f"current_user: {current_user}")
    sql = f'''
      SELECT respuesta.id, usuario.nombres, usuario.apellido, peticion.info, respuesta.info 
      FROM respuesta 
      INNER JOIN usuario ON usuario.id = respuesta.mecanico
      INNER JOIN peticion ON peticion.id = respuesta.peticion
      WHERE peticion.usuario = {current_user["id"]}
      ORDER BY peticion.id;
    '''
    respuesta = db.session.execute(text(sql))
    respuesta = respuesta.fetchall()
    print(respuesta)
    return render_template("/respuesta.html", data=respuesta)