¿Como realizar Migraciones?

export FLASK_APP=main.py

1- flask db init
2- flask db migrate -m "Primera migracion"
3- flask db upgrade


¿How use crud basic?

1- insert_data:
    record = {"nombre": "Pablo", "correo": "pablo@example.com", "edad": 31, "color": "azul"}
    respuesta = Flask_crud.insert_data(Persona, record)

2- insert_data_all:
    record = [
        {"nombre": "Marcos", "correo": "marcos@example.com", "edad": 31, "color": "azul"},
        {"nombre": "María", "correo": "maria@example.com", "edad": 25, "color": "rojo"},
        {"nombre": "Kenny", "correo": "kenny@example.com", "edad": 25, "color": "rojo"},
    ]
    respuesta = Flask_crud.insert_data_all(Persona, record)

3- read_data:
    respuesta = Flask_crud.read_data(Persona, nombre = 'Pablo')
    return render_template('index.html', respuesta = respuesta)

4- read_data_all:
    respuesta = read_data_all(Persona)

