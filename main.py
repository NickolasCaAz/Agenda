from person import Person
import json
from flask import Flask, jsonify,request
from playhouse.shortcuts import model_to_dict, dict_to_model
from flask_restful import Api, Resource, reqparse
from flask_restful_swagger_2 import Api as SwaggerApi, swagger, Resource as SwaggerResource
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

@app.route('/')
def homepage():
    return """
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registro Agenda</title>
    </head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@200&display=swap');

    *{
        padding: 0;
        margin: 0;
        box-sizing: border-box;
        font-family: 'inter';
    }
        body{
            width: 100%;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #0c0ce94d;


    }
        .container{
            width: 80%;
            height: 80vh;
            display: flex;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, .212);
        }
        .form-image{
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: wheat;
            padding: 1rem;

        }
        .form-image img{
            width: 31rem;
        }

        .form{
            width: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            background-color: #fff;
            padding: 3rem;
        }
        .form-header{
            margin-bottom: 3rem;
            display: flex;
            justify-content: space-between;
        }
        .login-bt{
            display: flex;
            align-items: center;
        }
        .login-bt button{
            border: none;
            background-color: #6c63ff;
            padding: 0.4rem 1rem;
            border-radius: 5px;
            cursor: pointer;
        }
        .login-bt button:hover{
            background-color: #6c63fff1 ;

        }
        .login-bt button a{
            text-decoration: none;
            font-weight: 500;
            color: #fff;
        }
        .form-header h1::after{
            content: '';
            display: block;
            width: 5rem;
            height: 0.3rem;
            background-color: #6c63ff;
            margin: 0 auto;
            position: absolute;
            border-radius: 10px;
        }

        .input-group{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            padding: 1rem 0;

        }
        .input-box{
            display: flex;
            flex-direction: column;
            margin-bottom: 1.1rem;
        }

        .input-box input{
            margin: 0.6rem 0;
            padding: 0.8rem 1.2rem;
            border: none;
            border-radius: 1;
            box-shadow: 1px 1px 6px #0000001c;
        }
        .input-box input:hover{
            background-color: #eeeeee75;
        }

        .input-box input:focus-visible{
            outline: 1pc solid #6c63ff;
        }

        .input-box label{
            font-size: 0.75rem;
            font-weight: 600;
            color: #000000c0;
        }
        .input-box input::placeholder{
            color: #000000be;
        }


    </style>
    <body>
        <div class="container">
            <div class="form-image">
                <img src="D:/projetos/python/minhaagenda/html/img/undraw_sign_up_n6im.svg">

            </div>
            <div class="form">
                <form action="http://localhost:5000/v1/person" method="POST">
                    <div class="form-header">
                        <div class="title">
                            <h1>Cadastro</h1>
                        </div>
                        <div class="login-bt">
                            <button type="submit"><a>Entrar</a></button>
                        </div>
                    
                    </div>
                    <div class="input-group">
                            <div class="input-box">
                                <label for="name">Nome</label>
                                <input id="name" type="text" name="name" placeholder="Insira seu nome..." required>
                            </div>
                        

                            <div class="input-box">
                                    <label for="number">Número de telefone</label>
                                    <input id="number" type="text" name="number" placeholder="Número para contato..." required>
                            </div>
                            
                            <div class="input-box">
                                <label for="email">E-mail</label>
                                <input id="email" type="text" name="email" placeholder="E-mail para contato..." required>
                            </div>
                
                    </div>    
                </form>
            </div>
        </div>
    </body>
    <!-- ... (your existing HTML code) ... -->

    <script>
        const form = document.querySelector('form');
        form.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                number: formData.get('number'),
                email: formData.get('email')
            };
            
            try {
                const response = await fetch('http://localhost:5000/v1/person', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                if (response.status === 201) {
                    // Success, do something here
                } else {
                    // Handle error here
                }
            } catch (error) {
                // Handle error here
            }
        });
    </script>

    </html>
    """

@app.route('/v1/person', methods = ["GET"])
def getAllPerson():
    pessoas = Person.select()
    lista_pessoas = [model_to_dict(pessoa) for pessoa in pessoas]
    return jsonify(lista_pessoas)


@app.route('/v1/person/<codigo>', methods = ["GET"])
def getPerson(codigo):
    pessoas = Person.get(Person.id==codigo)
    if pessoas:
        return jsonify(model_to_dict(pessoas))
    else:
        return jsonify({'error': 'Pessoa não encontrada'}), 404



@app.route('/v1/person', methods = ["POST"])
def creatPerson():
    request_data = request.get_json()
    # type(request_data)
    pessoa = Person()
    pessoa = dict_to_model(Person, request_data)
    # print (pessoa.number)
    pessoa.save()
    return request_data,201

@app.route('/v1/person/<codigo>', methods=["PUT"])
def updatePerson(codigo):
    request_data = request.get_json()
    pessoa = Person.get_or_none(Person.id == codigo)
    if pessoa:
        pessoa.update(**request_data).where(Person.id == codigo).execute()
        return jsonify({'message': 'Pessoa atualizada com sucesso'}), 200
    else:
        return jsonify({'error': 'Pessoa não encontrada'}), 404


@app.route('/v1/person/<codigo>', methods=["DELETE"])
def deletePerson(codigo):
    pessoa = Person.get_or_none(Person.id == codigo)
    if pessoa:
        pessoa.delete_instance()
        return jsonify({'message': 'Pessoa deletada com sucesso'}), 200
    else:
        return jsonify({'error': 'Pessoa não encontrada'}), 404

@app.route("/spec")
def spec():
    return jsonify(swagger(app))


class PersonResource(SwaggerResource):
    @swagger.doc({
        'tags': ['Person'],
        'description': 'Get all persons',
        'responses': {
            '200': {
                'description': 'List of persons',
                'schema': {
                    'type': 'array',
                    'items': {
                        '$ref': '#/definitions/PersonModel'
                    }
                }
            }
        }
    })
    def get(self):
        # Your implementation to get all persons
        pass

    @swagger.doc({
        'tags': ['Person'],
        'description': 'Create a new person',
        'parameters': [
            {
                'name': 'body',
                'in': 'body',
                'required': True,
                'description': 'Person object',
                'schema': {
                    '$ref': '#/definitions/PersonModel'
                }
            }
        ],
        'responses': {
            '201': {
                'description': 'Person created successfully'
            }
        }
    })
    def post(self):
        # Your implementation to create a new person
        pass

# Add more routes for other CRUD operations as needed

api.add_resource(PersonResource, '/v1/person')

# Define your Swagger definitions
app.config['SWAGGER'] = {
    'title': 'Person API',
    'description': 'API for managing persons',
    'uiversion': 3,
}

swagger = Swagger(app)



if __name__ == '__main__':
    try:
        Person.create_table()
        print("Tabela 'Person' criada com sucesso!")
    except Person.peewee.OperationalError:
        print("Tabela 'Person' ja existe!")
    app.run()
