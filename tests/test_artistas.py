# import pytest
# from src import app

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client

# def test_meu_teste(client):
#     # Use a fixture 'client' no seu teste
#     response = client.get('/meu-endpoint')
#     assert response.status_code == 200
#     # Restante do código de teste

# def test_artista_existente(client, mocker):
#     # Mock do cursor do banco de dados
#     mock_cursor = mocker.Mock()

#     # Resultado simulado retornado pelo banco de dados
#     resultado_simulado = [
#         ('Nome do Artista', 'Nome da Gravadora', 'Nome da Música')
#     ]

#     # Simula a execução da consulta SQL
#     mocker.patch('app.mydb.cursor', return_value=mock_cursor)
#     mock_cursor.fetchall.return_value = resultado_simulado

#     # Teste da rota do endpoint
#     response = client.get('/artistas/1')
#     data = response.get_json()

#     assert response.status_code == 200
#     assert 'Nome do Artista' in data
#     assert 'Nome da Gravadora' in data

# def test_artista_nao_encontrado(client, mocker):
#     # Mock do cursor do banco de dados
#     mock_cursor = mocker.Mock()

#     # Simula o retorno vazio do banco de dados
#     mocker.patch('app.mydb.cursor', return_value=mock_cursor)
#     mock_cursor.fetchall.return_value = []

#     # Teste da rota do endpoint
#     response = client.get('/artistas/1')
#     data = response.get_json()

#     assert response.status_code == 404
#     assert 'mensagem' in data