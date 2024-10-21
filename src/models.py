from flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname= db.Column(db.String(20), unique=False, nullable=True)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)


    def __repr__(self): 
        return '<User %r>' % self.id

    def serialize(self): #convierte la instancia de modelo en un diccionario p. 
        return {
            "id": self.id,
            "email": self.email,
            "firstname": self.firstname, 
            "lastname": self.lastname, 
            "username": self.username
            
        }
class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    climate = db.Column(db.String(20), nullable= False)


    def __repr__(self): 
        return '<User %r>' % self.id

    def serialize(self): #convierte la instancia de modelo en un diccionario p. 
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate
        }

class Personajes(db.Model):
    id = db.Column(db.Integer,primary_key=True )
    name = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
        
class Favoritos(db.Model):
    id = db.Column(db.Integer,primary_key=True )
    user_id= db.Column(db.Integer, db.ForeignKey('Usuario.id'), nullable=False)
    planeta_favorito = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable = True)
    personajes_favorito = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=True)

    user = db.relationship('Usuario', backref='favoritos')
    planeta = db.relationship('Planetas', backref ='favoritos')
    personaje = db.relationship('Personajes', backref= 'favoritos')


    def __repr__(self):
        return '<User %r>' % self.id
       
    
    def __serialize(self):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "planeta_favorito": None,
            "personaje_favorito":None,
        }

        #en casao de exisitir un planeta favorito:
        if self.planeta : 
            data["planeta_favorito"]={}
            for key in self.planeta.serialize():
                data["planeta_favorito"][key]= self.planeta.serialize()[key]
            
        
        #si existe personaje fav: 
        if self.personaje: 
            data["personaje_favorito"]={}
            for key in self.personaje.serialize():
                data["personaje_favorito"][key]= self.personaje.serialize()[key]
                
        return data
    





    
    