"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
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

#metdo para agregar todos los planetas
@app.route('/planetas', methods=['GET'])
def obtener_planetas():
    list_planetas = Planetas.query.all()
    todos_planetas = [planeta.serialize() for planeta in list_planetas ]
    reponse_body = {
        'msg': 'Planetas encontrados', 
        'planetas':todos_planetas
    }
    return jsonify(reponse_body),200

#obtengo un planeta con su id 
@app.route('/planetas/<int:id>', methods=['GET'])
def planeta_id(id):
    planeta = Planetas.query.get(id)
    if planeta is None: 
        return jsonify({'msg':'Planeta no encontrado'}), 400
    return jsonify(planeta.serialaze()),200

#obtener TODOS los personajes
@app.route('/personajes', methods=['GET'])
def obtener_personajes():
    list_personajes = Personajes.query.all()
    todos_personajes = [personajes.serialize() for personajes in list_personajes]
    response_body = {
        'msg': 'Personajes encontrados', 
        'personajes': todos_personajes
    }
    return jsonify(response_body), 200

#obtener UN personaje según su id:
@app.route('/personajes/<int:id>', methods=['GET'])
def personaje_id(id):
    personaje = Personajes.query.get(id)
    if personaje is None: 
        return jsonify({'msg': 'Personaje no encontrado'}), 400
    return jsonify(personaje.serialaze()),200

#agregar un plenta
@app.route('/planetas', methods=['POST'])
def agregar_planeta():
    data = request.get_json()
    name = data.get('name')
    climate = data.get('climate')

    if not  name or not climate:
        return jsonify({'msg':'Error campos obligatorios'}), 400
    
    if Planetas.query.filter_by(name=name).first():
        return jsonify({'msg': 'El planeta ya existe '}), 400
    
    nuevo_planeta = Planetas( name=name, climate= climate)

    try: 
        db.session.add(nuevo_planeta)
        db.session.commit()
        return jsonify({'msg': 'Planeta agregado con exito '}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500
    

    



    

#agregar un planeta a fav.
@app.route('/favoritos/planetas', methods =['POST'])
def favoritos_planetas():
    data = request.get_json()
    
    planeta_id = data.get("planeta_id")

    if not planeta_id: 
        return jsonify({'msg': 'Planeta id no enviado'}), 400
    
    planeta = Planetas.query.get(planeta_id)
    if not planeta: 
        return jsonify({'msg': 'El planeta no existe'}), 400
    
    nuevo_favorito = Favoritos(planeta_favorito=planeta_id)

    try: 
        db.session.add(nuevo_favorito)
        db.session.commit()
        return jsonify({'msg': 'Planeta agregado con exito '}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 500
    

   





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
