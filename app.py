from flask              import Flask, render_template
from routes.router      import nuberouter
from utils.db           import db
from flask_login        import LoginManager  
from models.User        import User

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/tcarros_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

def pagina_no_encontrada(error):
    return render_template("pagina_no_encontrada.html")

app.register_error_handler(404, pagina_no_encontrada)

login_manager = LoginManager()

login_manager.init_app(app)

db.init_app(app=app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app.register_blueprint(nuberouter)
      
    
## pip install mysqlclient    
## pip install Flask-SQLAlchemy
## pip install mysql-connector-python
## pip install PyMySQL
## pip install Flask-Bootstrap
## pip install bcrypt