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
                'duracao' : str(song[2])
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

    sql = f"INSERT INTO `musicas` (`id`, `nome`, `duracao`, `generos_id`, `lancamento`, `created`, `modified`) VALUES ('{song['id']}', '{song['nome']}', '{song['duracao']}', '{song['generos_id']}', '{song['lancamento']}', '{song['created']}', '{song['modified']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Música cadastrada com sucesso!',
        dados = song
        )
    )

if __name__ == '__main__':
    
    app.run(host="localhost", port="5000", debug=True)