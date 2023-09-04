# from os import environ
# import re

# from app import app, db
# from server.models import Animal, Enclosure, Zookeeper

# class TestApp:
#     '''Flask application in app.py'''

#     with app.app_context():
#         a_1 = Animal()
#         a_2 = Animal()
#         e = Enclosure()
#         z = Zookeeper()
#         e.animals = [a_1, a_2]
#         z.animals = [a_1, a_2]
#         db.session.add_all([a_1, a_2, e, z])
#         db.session.commit()

#     def test_animal_route(self):
#         '''has a resource available at "/animal/<id>".'''
#         response = app.test_client().get('/animal/1')
#         assert(response.status_code == 200)

#     def test_animal_route_has_attrs(self):
#         '''displays attributes in animal route in <ul> tags called Name, Species.'''
#         name_ul = re.compile(r'\<ul\>[Nn]ame.+')
#         species_ul = re.compile(r'\<ul\>[Ss]pecies.+')
        
#         response = app.test_client().get('/animal/1')

#         assert(len(name_ul.findall(response.data.decode())) == 1)
#         assert(len(species_ul.findall(response.data.decode())) == 1)

#     def test_animal_route_has_many_to_one_attrs(self):
#         '''displays attributes in animal route in <ul> tags called Zookeeper, Enclosure.'''
#         zookeeper_ul = re.compile(r'\<ul\>Zookeeper.+')
#         enclosure_ul = re.compile(r'\<ul\>Enclosure.+')
        
#         response = app.test_client().get('/animal/1')

#         assert(len(zookeeper_ul.findall(response.data.decode())) == 1)
#         assert(len(enclosure_ul.findall(response.data.decode())) == 1)

#     def test_zookeeper_route(self):
#         '''has a resource available at "/zookeeper/<id>".'''
#         response = app.test_client().get('/zookeeper/1')
#         assert(response.status_code == 200)

#     def test_zookeeper_route_has_attrs(self):
#         '''displays attributes in zookeeper route in <ul> tags called Name, Birthday.'''
#         name_ul = re.compile(r'\<ul\>[Nn]ame.+')
#         birthday_ul = re.compile(r'\<ul\>[Bb]irthday.+')
        
#         response = app.test_client().get('/zookeeper/1')

#         assert(len(name_ul.findall(response.data.decode())) == 1)
#         assert(len(birthday_ul.findall(response.data.decode())) == 1)

#     def test_zookeeper_route_has_one_to_many_attr(self):
#         '''displays attributes in zookeeper route in <ul> tags called Animal.'''
#         animal_ul = re.compile(r'\<ul\>Animal.+')
        
#         id = 1
#         response = app.test_client().get(f'/zookeeper/{id}')
#         assert len(animal_ul.findall(response.data.decode()))

#     def test_enclosure_route(self):
#         '''has a resource available at "/enclosure/<id>".'''
#         response = app.test_client().get('/enclosure/1')
#         assert(response.status_code == 200)

#     def test_enclosure_route_has_attrs(self):
#         '''displays attributes in enclosure route in <ul> tags called Environment, Open to Visitors.'''
#         environment_ul = re.compile(r'\<ul\>[Ee]nvironment.+')
#         open_ul = re.compile(r'\<ul\>[Oo]pen\s[Tt]o\s[Vv]isitors.+')
        
#         response = app.test_client().get('/enclosure/1')

#         assert(len(environment_ul.findall(response.data.decode())) == 1)
#         assert(len(open_ul.findall(response.data.decode())) == 1)

#     def test_enclosure_route_has_one_to_many_attr(self):
#         '''displays attributes in enclosure route in <ul> tags called Animal.'''
#         animal_ul = re.compile(r'\<ul\>Animal.+')
        
#         id = 1
#         response = app.test_client().get(f'/enclosure/{id}')
#         assert len(animal_ul.findall(response.data.decode()))



#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Animal, Zookeeper, Enclosure

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.filter(Animal.id == id).first()
    if not animal:
        response_body = '<h1>404 animal not found</h1>'
        response = make_response(response_body, 404)
        return response
   
    response_body = f'''
                <ul>Name:{animal.name}</ul>
                <ul>Species:{animal.species}</ul>  
                <ul>Zookeeper:{animal.zookeeper.name}</ul>
                <ul>Enclosure:{animal.enclosure.environment}</ul>
             '''
    response = make_response(response_body,200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.filter(Zookeeper.id == id).first()
    if not zookeeper:
        response_body = '<h1>404 zookeeper not found</h1>'
        response = make_response(response_body, 404)
        return response
    response_body = f'''
                <ul>Name:{zookeeper.name}</ul>
                <ul>Birthday:{zookeeper.birthday}</ul>
                <ul>Animals:
                            '''
     # Loop through the animals associated with the zookeeper
    for animal in zookeeper.animals:
        response_body += f'<li>{animal.name} - {animal.species}</li>'
    
    response_body += '</ul>'
    response = make_response(response_body,200)
    return response

@app.route('/enclosure/<int:id>')

def enclosure_by_id(id):
    enclosure = Enclosure.query.filter(Enclosure.id == id).first()
    response_body = f'''
            <ul>Environment:{enclosure.environment}</ul>
            <ul>Open To Visitors:{enclosure.open_to_visitors}</ul>
            <ul>Animals:
           '''
    for animal in enclosure.animals:
        response_body += f'<li>{animal.name} - {animal.species}</li>'
    
    response_body += '</ul>'
    response = make_response(response_body,200)
    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)