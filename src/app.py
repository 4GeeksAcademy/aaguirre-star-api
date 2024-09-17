"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Usuario, Planetas, Personajes, Favoritos
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#metodos para obtener todos los usuarios. 
@app.route('/usuario', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all() #obtengo de la tabla usuario y los almaceno, me devuelve una lista.
    todos_usuario = [usuarios.serialize() for usuario in usuarios ] #uso el metodo ser. q convierte el obj usuario en un dicc. Itero sobre cada obj usuario de la lista usuarios de arriba. 

    response_body = {
        "msg": "Usuarios encontrados", 
        "usuarios": todos_usuario  #agrego la lista de usuarios a la rspuesta
    }

    return jsonify(response_body), 200 # respuesta correcta. 

#metodo para obtener un unico usuario, según su id. 
@app.route('/usuario/<int:id>', methods=['GET'])
def obtener_un_usuario(id):
    usuario = Usuario.query.get(id)
    #verifico si el usuario se encontro, 
    if usuario is None:
        return jsonify({'msg':"Usuario no encontrado"}), 400
    #en caso de encontrar el usuario, convierto el js a dicc
    return jsonify(usuario.serialaze()), 200

#metdo para agregar un usuario
@app.route('/planetas', methods=['GET'])
def obtener_planetas():
    list_planetas = Planetas.query.all()
    todos_planetas = [planeta.serialize() for planeta in list_planetas ]
    reponse_body = {
        'msg': 'Planetas encontrados', 
        'planetas':todos_planetas
    }
    return jsonify(reponse_body),200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
