import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv 

#Cargar las variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Alumno(db.Model):
    __tablename__ = 'alumnos'
    no_control = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    ap_paterno = db.Column(db.String)
    ap_materno = db.Column(db.String)
    semestre = db.Column(db.Integer)

#endpoint para obtener todos los alumnos
@app.route('/alumnos', methods=['GET'])
def get_alumnos():
    alumnos = Alumno.query.all()
    lista_alumnos = []
    for alumno in alumnos:
        lista_alumnos.append({
            'no_control ': alumno.no_control,
            'nombre ': alumno.nombre,
            'ap_paterno ': alumno.ap_paterno,
            'ap_materno ': alumno.ap_materno,
            'semestre ': alumno.semestre
        })
    return jsonify(lista_alumnos)

#endpoint para agregar un nuevo alumno
@app.route('/alumnos', methods=['POST'])
def insert_alumno():
    data = request.get_json()
    nuevo_alumno = Alumno(
        no_control = data['no_control'],
        nombre = data['nombre'],
        ap_paterno = data['ap_paterno'],
        ap_materno = data['ap_materno'],
        semestre = data['semestre'],
    )
    db.session.add(nuevo_alumno)
    db.session.commit()
    return jsonify ({'msg':'Alumno agregado correctamente'})

#endpoint para obtener un alumno por el no_control
@app.route('/alumnos/<no_control>', methods=['GET'])
def get_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify ({'msg':'Alumno no encontrado'})
    return jsonify({
        'no_control': alumno.no_control,
        'nombre': alumno.nombre,
        'ap_paterno': alumno.ap_paterno,
        'ap_materno': alumno.ap_materno,
        'semestre': alumno.semestre,
    })

#endpoint para eliminar un alumno
@app.route('/alumnos/<no_control>', methods=['DELETE'])
def delete_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify ({'msg':'Alumno no encontrado'})
    db.session.delete(alumno)
    db.session.commit()
    return jsonify ({ 'msg':'Alumno eliminado correctamente'})

#endpoint para actualizar un alumno
@app.route('/alumnos/<no_control>', methods=['PATCH'])
def update_alumno(no_control):
    alumno = Alumno.query.get(no_control)
    if alumno is None:
        return jsonify ({'msg':'Alumno no encontrado'})
    data = request.get_json()

    if "nombre" in data:
        alumno.nombre = data['nombre']
    if "ap_paterno" in data:
        alumno.ap_paterno = data['ap_paterno']
    if "ap_materno" in data:
        alumno.ap_materno = data['ap_materno']    
    if "semestre" in data:
        alumno.semestre = data['semestre']
    
    db.session.commit()
    return jsonify ({ 'msg':'Alumno actualizado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)