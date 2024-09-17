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
    planeta_favorito = db.Column(db.Integer, db.ForeignKey('planetas.id'))
    personajes_favorito = db.Column(db.Integer, db.ForeignKey('personajes.id'))

    def __repr__(self):
        return '<User %r>' % self.id
       
    
    def __serialize(self):
        return {
            "id": self.id,
            "planetas_favorito": self.planeta_favorito, 
            "personajes_favorito": self.personajes_favorito
        }





    
    