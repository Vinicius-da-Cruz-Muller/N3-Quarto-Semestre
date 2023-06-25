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

@app.route('/musicas', methods = ['GET']) #puxa todas as músicas da tabela músicas, tanto as que já estavam no banco quanto as criadas na api
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
                'lancamento': str(song[4]) 
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de músicas',
        dados = songs
        )
    )

@app.route('/musicas', methods = ['POST']) #adiciona uma nova música. id é auto incrementado e as datas são colocadas por padrão como "None"
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

@app.route('/musicas', methods = ['PUT']) # Altera o nome da música. Se tiver que alterar outra coisa, basta alterar o comando ou comandos sql
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

@app.route('/musicas', methods = ['DELETE']) # deleta uma música baseado no id que é passado. existe outra parametro que se pode pedir para excluir?
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

# ----------------------------------------------------------------------------------------------------------

@app.route('/generos', methods = ['GET']) #lista todos os generos musicais
def get_generos():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM generos')
    generos = my_cursor.fetchall()

    gens = list()
    for gen in generos:
        gens.append(
            {
                'id' : gen[0],
                'descricao' : gen[1],
                'created' : str(gen[2]),
                'modified': str(gen[3]) 
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de gêneros do banco de dados',
        dados = gens
        )
    )


@app.route('/generos', methods = ['POST']) #Insere um novo gênero musical na tabela generos
def inserir_genero_musical():
    gen = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `generos` (`descricao`) VALUES ('{gen['descricao']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Gênero musical inserido com sucesso!',
        dados = gen
        )
    )


if __name__ == '__main__':
    
    app.run(host="localhost", port="5000", debug=True)