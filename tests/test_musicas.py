import mysql.connector
from flask import Flask, jsonify, request
from unittest.mock import Mock
import pytest

from src.app import app, get_musicas, musica_por_id, nova_musica, musicas_insert, musicas_artistas_insert

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Define um mock para o cursor do MySQL
class MockCursor:
    def execute(self, sql):
        pass

    def fetchall(self):
        return [
            (1, 'Música 1', 180, 'Artista 1'),
            (2, 'Música 2', 210, 'Artista 2')
        ]

# Define um mock para a conexão do MySQL
class MockDB:
    def cursor(self):
        return MockCursor()

# Define um mock para a conexão MySQL do aplicativo Flask
@pytest.fixture(autouse=True)
def mock_mysql_connector(mocker):
    mocker.patch('mysql.connector.connect', return_value=MockDB())

# Teste para a rota '/musicas'
def test_get_musicas(client, mocker):
    # Cria um mock do cursor e substitui a implementação da função 'execute'
    mock_cursor = Mock()
    mock_cursor.fetchall.return_value = [
        (1, 'Música 1', 180, 'Artista 1'),
        (2, 'Música 2', 210, 'Artista 2')
    ]
    mocker.patch('mysql.connector.cursor', return_value=mock_cursor)

    # Faz uma requisição GET para a rota '/musicas'
    response = client.get('/musicas')

    # Verifica se a resposta está correta
    assert response.status_code == 200
    data = response.get_json()
    assert data['mensagem'] == 'Lista de músicas'
    assert len(data['dados']) == 30
    assert data['dados'][0]['id'] == 1
    assert data['dados'][0]['nome'] == 'Conta pro tio'
    assert data['dados'][0]['duracao'] == '4:00:00'
    assert data['dados'][0]['nome do artista'] == 'Mano Lima'

    assert data['dados'][1]['id'] == 2
    assert data['dados'][1]['nome'] == 'Balaio de gato'
    assert data['dados'][1]['duracao'] == '3:05:00'
    assert data['dados'][1]['nome do artista'] == 'Mano Lima'

    # Chama a função get_musicas explicitamente
    get_musicas()


# Define um mock para o cursor do MySQL
class MockCursor:
    def execute(self, sql, params):
        pass

    def fetchone(self):
        return ('Música 1', 180, 'Artista 1')

# # Define um mock para a conexão do MySQL
# class MockDB:
#     def cursor(self):
#         return MockCursor()

# Define um mock para a conexão MySQL do aplicativo Flask
@pytest.fixture(autouse=True)
def mock_mysql_connector(mocker):
    mocker.patch('mysql.connector.connect', return_value=MockDB())

# Teste para a rota '/musicas/<int:musica_id>'
def test_musica_por_id(client, mocker):
    # Cria um mock do cursor e substitui a implementação da função 'execute'
    mock_cursor = Mock()
    mock_cursor.fetchone.return_value = ('Música 1', 180, 'Artista 1')
    mocker.patch('mysql.connector.cursor', return_value=mock_cursor)

    # Faz uma requisição GET para a rota '/musicas/1'
    response = client.get('/musicas/1')

    # Verifica se a resposta está correta
    assert response.status_code == 200
    data = response.get_json()
    assert data['Nome da música'] == 'Conta pro tio'
    assert data['Tempo de duração'] == '4:00:00'
    assert data['Nome do artista'] == 'Mano Lima'


# Define um mock para a conexão MySQL do aplicativo Flask
@pytest.fixture(autouse=True)
def mock_mysql_connector(mocker):
    mocker.patch('mysql.connector.connect')

# Teste para a rota '/musicas'
def test_nova_musica(client, mocker):
    # Define os dados do JSON de requisição
    json_data = {
        'nome': 'Música 1',
        'duracao': 180,
        'generos_id': 1,
        'lancamento': None,
        'artistas': [1, 2]
    }

    # Cria um mock para a função 'musicas_insert' e substitui a implementação
    mock_musicas_insert = Mock(return_value=(1, None))
    mocker.patch('src.app.musicas_insert', mock_musicas_insert)

    # Cria um mock para a função 'musicas_artistas_insert' e substitui a implementação
    mock_musicas_artistas_insert = Mock(return_value=None)
    mocker.patch('src.app.musicas_artistas_insert', mock_musicas_artistas_insert)

    # Faz uma requisição POST para a rota '/musicas'
    response = client.post('/musicas', json=json_data)

    # Verifica se a resposta está correta
    assert response.status_code == 201
    data = response.get_json()
    assert data['mensagem'] == 'Música criada com sucesso'

    # Verifica se as funções 'musicas_insert' e 'musicas_artistas_insert' foram chamadas corretamente
    mock_musicas_insert.assert_called_once_with('Música 1', 180, 1, None)
    mock_musicas_artistas_insert.assert_called_once_with(1, [1, 2])

# Executa os testes
if __name__ == '__main__':
    pytest.main()