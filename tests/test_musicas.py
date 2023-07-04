# import mysql.connector
# from flask import Flask, jsonify, request
# from unittest.mock import Mock
# import pytest

# from src.app import app, get_musicas #, musica_por_id, nova_musica, musicas_insert, musicas_artistas_insert, altera_musica

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# class MockCursor:
#     def execute(self, sql):
#         pass

#     def fetchall(self):
#         return [
#             (1, 'Música 1', 180, 'Artista 1'),
#             (2, 'Música 2', 210, 'Artista 2')
#         ]

# # Define um mock para a conexão do MySQL
# class MockDB:
#     def cursor(self):
#         return MockCursor()

# # Define um mock para a conexão MySQL do Flask
# @pytest.fixture(autouse=True)
# def mock_mysql_connector(mocker):
#     mocker.patch('mysql.connector.connect', return_value=MockDB())

# def test_get_musicas(client, mocker):
#     mock_cursor = Mock()
#     mock_cursor.fetchall.return_value = [
#         (1, 'Música 1', 180, 'Artista 1'),
#         (2, 'Música 2', 210, 'Artista 2')
#     ]
#     mocker.patch('mysql.connector.cursor', return_value=mock_cursor)

#     response = client.get('/musicas')

#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['mensagem'] == 'Lista de músicas'
#     assert len(data['dados']) == 30
#     assert data['dados'][0]['id'] == 1
#     assert data['dados'][0]['nome'] == 'Nova música'
#     assert data['dados'][0]['duracao'] == '4:00:00'
#     assert data['dados'][0]['nome do artista'] == 'Mano Lima'

#     assert data['dados'][1]['id'] == 2
#     assert data['dados'][1]['nome'] == 'Balaio de gato'
#     assert data['dados'][1]['duracao'] == '3:05:00'
#     assert data['dados'][1]['nome do artista'] == 'Mano Lima'

#     # Chama a função get_musicas explicitamente
#     get_musicas()

# #-----------------------------------------------------------------------------------------------------------------------------------
# #Teste música por id
# #---------------------------------------------------------------------------------------------------------------------------------


# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# class MockCursor:
#     def execute(self, sql, params):
#         pass

#     def fetchone(self):
#         return ('Música 1', 180, 'Artista 1')

# class MockDB:
#     def cursor(self):
#         return MockCursor()

# @pytest.fixture(autouse=True)
# def mock_mysql_connector(mocker):
#     mocker.patch('mysql.connector.connect', return_value=MockDB())

# def test_musica_por_id(client, mocker):
#     mock_cursor = Mock()
#     mock_cursor.fetchone.return_value = ('Música 1', 180, 'Artista 1')
#     mocker.patch('mysql.connector.cursor', return_value=mock_cursor)

#     response = client.get('/musicas/1')

#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['Nome da música'] == 'Nova música'
#     assert data['Tempo de duração'] == '4:00:00'
#     assert data['Nome do artista'] == 'Mano Lima'

# #-----------------------------------------------------------------------------------------------------------------------------------
# #Teste criar música
# #---------------------------------------------------------------------------------------------------------------------------------
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# @pytest.fixture(autouse=True)
# def mock_mysql_connector(mocker):
#     mocker.patch('mysql.connector.connect')

# def test_nova_musica(client, mocker):
#     json_data = {
#         'nome': 'Música 1',
#         'duracao': 180,
#         'generos_id': 1,
#         'lancamento': None,
#         'artistas': [1, 2]
#     }

#     mock_musicas_insert = Mock(return_value=(1, None))
#     mocker.patch('src.app.musicas_insert', mock_musicas_insert)

#     mock_musicas_artistas_insert = Mock(return_value=None)
#     mocker.patch('src.app.musicas_artistas_insert', mock_musicas_artistas_insert)

#     response = client.post('/musicas', json=json_data)

#     assert response.status_code == 201
#     data = response.get_json()
#     assert data['mensagem'] == 'Música criada com sucesso'

#     mock_musicas_insert.assert_called_once_with('Música 1', 180, 1, None)
#     mock_musicas_artistas_insert.assert_called_once_with(1, [1, 2])

# #-----------------------------------------------------------------------------------------------------------------------------------
# #Teste editar música
# #---------------------------------------------------------------------------------------------------------------------------------
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# class MockCursor:
#     def execute(self, sql):
#         pass

#     def fetchone(self):
#         return ('Música alterada',)

#     def cursor(self):
#         return MockCursor()

# @pytest.fixture(autouse=True)
# def mock_mysql_connector(mocker):
#     mocker.patch('mysql.connector.connect', return_value=MockDB())

# def test_altera_musica(client, mocker):
#     mock_cursor = Mock()
#     mock_cursor.fetchone.return_value = ('Música alterada',)
#     mocker.patch('mysql.connector.cursor', return_value=mock_cursor)

#     data = {'id': 1, 'nome': 'Nova música'}

#     response = client.put('/musicas', json=data)

#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['mensagem'] == 'Música alterada com sucesso!'
#     assert data['dados']['id'] == 1
#     assert data['dados']['nome'] == 'Nova música'



# # Executa os testes
# if __name__ == '__main__':
#     pytest.main()