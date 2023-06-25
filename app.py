import mysql.connector
from flask import Flask, request, jsonify, make_response

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Semestre202301',
    database = 'n3tripla',
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/musicas', methods = ['GET'])
def get_musicas():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM musicas')
    musicas = my_cursor.fetchall()

    songs = list()
    for song in musicas:
        songs.append(
            {
                'id' : song[0],
                'nome' : song[1],
                'duracao' : str(song[2]),
                'lancamento': str(song[4]) #retorna None como padrão
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de músicas',
        dados = songs
        )
    )

@app.route('/musicas', methods = ['POST'])
def nova_musica():
    song = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `musicas` (`nome`, `duracao`, `generos_id`) VALUES ('{song['nome']}', '{song['duracao']}', '{song['generos_id']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Música cadastrada com sucesso!',
        dados = song
        )
    )

@app.route('/musicas', methods = ['PUT'])
def altera_musica():
    song = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `musicas` SET `nome` = '{song['nome']}' WHERE `id` = '{song['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Música alterada com sucesso!',
        dados = song
        )
    )

@app.route('/musicas', methods = ['DELETE'])
def exclui_musica():
    song = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `musicas` WHERE `id` = '{song['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Música excluida com sucesso!',
        dados = song
        )
    )

if __name__ == '__main__':
    
    app.run(host="localhost", port="5000", debug=True)