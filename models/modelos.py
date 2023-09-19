from utils.db import db
from sqlalchemy.sql import text

class tipo_usuario(db.Model):
    __tablename__ = "tipo_usuario"
    nombre = db.Column(db.String(100), primary_key=True)
    
    def __init__(self, nombre):
        self.nombre = nombre

class usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    clave = db.Column(db.String(500), nullable=False)
    tipo_usuario = db.Column(db.String(100), db.ForeignKey("tipo_usuario.nombre", ondelete="CASCADE"), default="cliente")
    
    tipo_usuario_relacion = db.relationship("tipo_usuario", passive_deletes=True, backref="tipo_usuario")

    def __init__(self, nombres, apellido, numero, email, clave, tipo_usuario = "cliente"):
        self.nombres        = nombres
        self.apellido       = apellido
        self.numero         = numero
        self.email          = email
        self.clave          = clave
        self.tipo_usuario   = tipo_usuario

class vehiculo(db.Model):
    __tablename__ = "vehiculo"
    id           = db.Column(db.Integer, primary_key=True)
    placa        = db.Column(db.String(100), nullable=False) 
    marca        = db.Column(db.String(100), nullable=False)
    modelo       = db.Column(db.String(100), nullable=False)
    fecha        = db.Column(db.DateTime, nullable=False)
    color        = db.Column(db.String(100), nullable=False)

    def __init__(self, placa, marca, modelo, fecha, color):
        self.placa          =placa
        self.marca          =marca
        self.modelo         =modelo
        self.fecha          =fecha
        self.color          =color 
        

class peticion(db.Model):
    __tablename__ = "peticion"

    id = db.Column(db.Integer, primary_key=True)

    usuario     = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"))
    vehiculo    = db.Column(db.Integer, db.ForeignKey("vehiculo.id", ondelete="CASCADE"))
    info        = db.Column(db.String(500), nullable=False)
    status      = db.Column(db.Boolean, default=0)
    
    usuario_relacion = db.relationship("usuario", passive_deletes=True, backref="cliente")
    vehiculo_relacion = db.relationship("vehiculo", passive_deletes=True, backref="vehiculo")
    
    def __init__(self, usuario, vehiculo, info):
        self.usuario    =usuario
        self.vehiculo   =vehiculo
        self.info       =info



class respuesta(db.Model):
    __tablename__:"respuesta"

    id= db.Column(db.Integer, primary_key=True)

    peticion    = db.Column(db.Integer, db.ForeignKey("peticion.id", ondelete="CASCADE"))
    mecanico    = db.Column(db.Integer, db.ForeignKey("usuario.id", ondelete="CASCADE"))
    info        = db.Column(db.String(500), nullable=False)


    mecanico_relacion = db.relationship("usuario", passive_deletes=True, backref="mecanico")    
    peticion_relacion = db.relationship("peticion", passive_deletes=True, backref="peticion")    

    def __init__(self, peticion, mecanico, info):
        self.peticion   =peticion
        self.mecanico   =mecanico
        self.info       =info   

