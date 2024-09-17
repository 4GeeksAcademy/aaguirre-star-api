from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    lastname= db.Column(db.String(20), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)


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
class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self): 
        return '<User %r>' % self.id

    def serialize(self): #convierte la instancia de modelo en un diccionario p. 
        return {
            "id": self.id,
            "name": self.name,
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
        
class Favorito (db.Model):
    id = db.Column(db.Integer,primary_key=True )



    
    