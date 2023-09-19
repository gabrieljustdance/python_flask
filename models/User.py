from flask_login    import UserMixin
from sqlalchemy.sql import text
from utils.db       import db

class User(UserMixin):
    def __init__(self, id, nombre, apellido, numero, email, tipo):
        self.id     = id
        self.nombre = nombre
        self.apellido = apellido
        self.numero = numero
        self.email  = email
        self.tipo   = tipo
        
    @classmethod
    def get(self, user_id):
        sql            = f"SELECT * FROM usuario WHERE id = '{user_id}';"
        usuario_valido  = db.session.execute(text(sql)) 
        usuario_valido  = list(usuario_valido)
        print(usuario_valido)
        
        usuario_caja = {
            'id':usuario_valido[0][0],
            'nombre':usuario_valido[0][1],
            'apellido':usuario_valido[0][2],
            'numero':usuario_valido[0][3],
            'email':usuario_valido[0][4],
            'type':usuario_valido[0][5]
        }
        return usuario_caja