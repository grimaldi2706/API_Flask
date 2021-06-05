#pip install flask, flask-sqlalchemy, flask-marshmallow, marshmallow-sqlalchemy, pymysql
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/bd_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nombres = db.Column(db.String(70),)
    Apellidos = db.Column(db.String(70),)
    identificacion = db.Column(db.Integer, unique=True)
    usuario = db.Column(db.String(50),unique=True)
    contrasena = db.Column(db.String(50),unique=True)
    #https://dev.to/kaelscion/authentication-hashing-in-sqlalchemy-1bem

    def __init__(self, Nombres,Apellidos,identificacion,usuario,contrasena):
        self.Nombres = Nombres
        self.Apellidos = Apellidos
        self.identificacion = identificacion
        self.usuario = usuario
        self.contrasena = contrasena

db.create_all()

class UsuarioSchema(ma.Schema):
    class Meta:
        fields = ('id','Nombres', 'Apellidos', 'identificacion', 'usuario','contrasena')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

@app.route('/user', methods = ['POST'])
def crear_usuario():
    Nombres = request.json['Nombres']
    Apellidos = request.json['Apellidos']
    identificacion = request.json['identificacion']
    usuario = request.json['usuario']
    contrasena = request.json['contrasena']

    nuevo_usuario = Usuarios(Nombres,Apellidos,identificacion,usuario,contrasena)

    db.session.add(nuevo_usuario)
    db.session.commit()

    return usuario_schema.jsonify(nuevo_usuario)

@app.route('/user', methods=['GET'])
def ver_usuarios():
    todos_usuarios = Usuarios.query.all()
    result = usuarios_schema.dump(todos_usuarios)
    return jsonify(result)

@app.route("/user/<int:id>", methods=['GET'])
def ver_usuario(id):
    _usuario = Usuarios.query.filter(Usuarios.identificacion == id).first()
    return usuario_schema.jsonify(_usuario)

@app.route('/user/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    _usuario = Usuarios.query.filter(Usuarios.identificacion == id).first()
    Nombres = request.json['Nombres']
    Apellidos = request.json['Apellidos']
    usuario = request.json['usuario']
    contrasena = request.json['contrasena']

    _usuario.Nombres = Nombres
    _usuario.Apellidos = Apellidos
    _usuario.usuario = usuario
    _usuario.contrasena = contrasena

    db.session.commit()

    return usuario_schema.jsonify(_usuario)

@app.route('/user/<id>', methods=['DELETE'])
def eliminar_usuario(id):
  _usuario = Usuarios.query.filter(Usuarios.identificacion == id).first()
  db.session.delete(_usuario)
  db.session.commit()
  return usuario_schema.jsonify(_usuario)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'API by Grimaldi'})


if __name__ == "__main__":
    app.run(debug=True, port=80)