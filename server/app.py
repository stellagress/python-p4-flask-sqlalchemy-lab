# #!/usr/bin/env python3

# from flask import Flask, make_response
# from flask_migrate import Migrate

# from models import db, Zookeeper, Enclosure, Animal

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/')
# def home():
#     return '<h1>Zoo app</h1>'

# @app.route('/animal/<int:id>')
# def animal_by_id(id):
#     # animal = Animal.query.filter(Animal.id == id).first()
#     # return f'<ul><li>Name: {animal.Name}</li><li>Species: {animal.Species}</li></ul>'
#     return ''


# @app.route('/zookeeper/<int:id>')
# def zookeeper_by_id(id):
#     return ''

# @app.route('/enclosure/<int:id>')
# def enclosure_by_id(id):
#     return ''


# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


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


