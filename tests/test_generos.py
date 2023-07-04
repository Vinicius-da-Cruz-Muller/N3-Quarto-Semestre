from flask import Flask, jsonify, make_response, request
from unittest.mock import patch
import pytest

import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Semestre202301',
    database = 'bancoteste1', #n3tripla
)

@app.route('/generos', methods=['GET'])
def get_generos():
    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM generos')
    generos = my_cursor.fetchall()

    gens = []
    for gen in generos:
        gens.append({
            'id': gen[0],
            'descricao': gen[1],
            'created': str(gen[2]),
            'modified': str(gen[3])
        })

    return make_response(jsonify({
        'mensagem': 'Lista de gêneros do banco de dados',
        'dados': gens
    }))

@patch('mysql.connector.connect')
@patch('src.app.mydb')
@patch('src.app.mydb.cursor')
def test_get_generos(mock_cursor, mock_mydb, mock_connect):
    mock_cursor_instance = mock_cursor.return_value
    mock_cursor_instance.fetchall.return_value = [
        (1, 'Gênero 1', '2023-01-01 00:00:00', '2023-01-01 00:00:00'),
        (2, 'Gênero 2', '2023-01-02 00:00:00', '2023-01-02 00:00:00')
    ]

    with app.test_client() as client:
        response = client.get('/generos')
        
        assert response.status_code == 200
        data = response.get_json()
        num = len(data['dados'])
        assert data['mensagem'] == 'Lista de gêneros do banco de dados'
        assert len(data['dados']) == num
        assert data['dados'][0]['id'] == 1
        assert data['dados'][0]['descricao'] == 'Gaúcha'
        assert data['dados'][0]['created'] == '2019-10-18 13:10:38'
        assert data['dados'][0]['modified'] == '2019-10-18 13:10:38'
        assert data['dados'][1]['id'] == 2
        assert data['dados'][1]['descricao'] == 'Pop'
        assert data['dados'][1]['created'] == '2019-10-18 13:10:42'
        assert data['dados'][1]['modified'] == '2019-10-18 13:10:42'

#----------------------------------------------------------------------------------------------------------------------------
#Gênero por id
#----------------------------------------------------------------------------------------------------------------------------


@app.route('/generos/<int:genero_id>', methods=['GET'])
def genero_por_id(genero_id):
    try: 
        my_cursor = mydb.cursor()
        sql = "SELECT descricao FROM generos WHERE id = %s"
        my_cursor.execute(sql, (genero_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            descricao = resultado[0]
            genero = {'Descrição do gênero': descricao}
            return jsonify(genero)
        else:
            return jsonify({'mensagem': 'Gênero não encontrado'}), 404
    except Exception as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@patch('mysql.connector.connect')
@patch('src.app.mydb')
@patch('src.app.mydb.cursor')
def test_genero_por_id(mock_cursor, mock_mydb, mock_connect):
    genero_id = 1
    descricao = 'Gaúcha'

    mock_cursor_instance = mock_cursor.return_value
    mock_cursor_instance.fetchone.return_value = (descricao,)

    with app.test_client() as client:
        response = client.get(f'/generos/{genero_id}')

        assert response.status_code == 200
        data = response.get_json()
        assert data == {'Descrição do gênero': descricao}

#----------------------------------------------------------------------------------------------------------------------------
#Cria gênero
#----------------------------------------------------------------------------------------------------------------------------

# @app.route('/generos', methods=['POST'])
# def inserir_genero_musical():
#     gen = request.json

#     my_cursor = mydb.cursor()

#     sql = f"INSERT INTO `generos` (`descricao`) VALUES ('{gen['descricao']}')"
#     my_cursor.execute(sql)
#     mydb.commit()

#     return make_response(jsonify({
#         'mensagem': 'Gênero musical inserido com sucesso!',
#         'dados': gen
#     }))

# @patch('mysql.connector.connect')
# @patch('src.app.mydb')
# @patch('src.app.mydb.cursor')
# def test_inserir_genero_musical(mock_cursor, mock_mydb, mock_connect):
#     gen = {'descricao': 'Gênero Teste 2'}

#     with app.test_client() as client:
#         response = client.post('/generos', json=gen)

#         assert response.status_code == 200
#         data = response.get_json()
#         assert data['mensagem'] == 'Gênero musical inserido com sucesso!'
#         assert data['dados'] == gen


#----------------------------------------------------------------------------------------------------------------------------
#Modifica gênero
#----------------------------------------------------------------------------------------------------------------------------

@app.route('/generos', methods=['PUT'])
def altera_genero():
    gen = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `generos` SET `descricao` = '{gen['descricao']}' WHERE `id` = '{gen['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(jsonify({
        'mensagem': 'Gênero musical alterado com sucesso!',
        'dados': gen
    }))

@patch('mysql.connector.connect')
@patch('src.app.mydb')
@patch('src.app.mydb.cursor')
def test_altera_genero(mock_cursor, mock_mydb, mock_connect):
    gen = {'id': 1, 'descricao': 'Gaúcha'}

    with app.test_client() as client:
        response = client.put('/generos', json=gen)

        assert response.status_code == 200
        data = response.get_json()
        assert data['mensagem'] == 'Gênero musical alterado com sucesso!'
        assert data['dados'] == gen



if __name__ == '_main_':
    pytest.main()