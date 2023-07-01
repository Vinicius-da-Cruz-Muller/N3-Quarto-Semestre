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
def get_musicas(): #Concluído

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

@app.route('/musicas/<int:musica_id>', methods = ['GET'])
def musica_por_id(musica_id): #Concluído
    try: 
        my_cursor = mydb.cursor()
        sql = "SELECT nome, duracao FROM musicas WHERE id = %s"
        my_cursor.execute(sql, (musica_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            nome, duracao = resultado
            musica = {'Nome da música': nome, 'Tempo de duração': str(duracao)}
            return jsonify(musica)
        else:
            return jsonify({'mensagem': 'Música não encontrada'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500


#Concluída
@app.route('/musicas', methods = ['POST']) #adiciona uma nova música. id é auto incrementado e as datas são colocadas por padrão como "None"
def nova_musica(request):
    nome = request.json['nome']
    duracao = request.json['duracao']
    generos_id = request.json['generos_id']
    lancamento = request.json['lancamento']
    artistas = request.json['artistas']
    musicas_id, error = musicas_insert(nome, duracao, generos_id, lancamento)
    if error:
        return jsonify({"error": error}), 500
    error = musicas_artistas_insert(musicas_id, artistas)
    if error:
        return jsonify({"error": error}), 500
    return '', 201

def musicas_insert(nome, duracao, generos_id, lancamento):
    try:
        my_cursor = mydb.cursor()
        my_cursor.execute("INSERT INTO `musicas` (`nome`, `duracao`, `generos_id`, `lancamento`) VALUES (%s, %s, %s, %s)", (nome, duracao, generos_id, lancamento))
        mydb.commit()
        return my_cursor.lastrowid, None
    except Exception as e:
        return 0, str(e)
    
def musicas_artistas_insert(musicas_id, artistas):
    try:
        my_cursor = mydb.cursor()
        for artistas_id in artistas:
            my_cursor.execute("INSERT INTO `musicas_has_artistas` (`musicas_id`, `artistas_id`) VALUES (%s, %s)", (musicas_id, artistas_id))
        mydb.commit()
        return None
    except Exception as e:
        return 0, str(e)
    

@app.route('/musicas', methods = ['PUT']) # Altera o nome da música. Se tiver que alterar outra coisa, basta alterar o comando ou comandos sql
def altera_musica(): #Concluído?
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
def get_generos(): #Concluído

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

@app.route('/generos/<int:genero_id>', methods = ['GET'])
def genero_por_id(genero_id): #Concluído
    try: 
        my_cursor = mydb.cursor()
        sql = "SELECT descricao FROM generos WHERE id = %s"
        my_cursor.execute(sql, (genero_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            descricao = resultado
            genero = {'Descrição do gênero': descricao}
            return jsonify(genero)
        else:
            return jsonify({'mensagem': 'Gênero não encontrado'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500


@app.route('/generos', methods = ['POST']) #Insere um novo gênero musical na tabela generos
def inserir_genero_musical(): #Concluído
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

@app.route('/generos', methods = ['PUT']) # Altera a descrição do gênero musical
def altera_genero(): #Concluído
    gen = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `generos` SET `descricao` = '{gen['descricao']}' WHERE `id` = '{gen['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Gênero musical alterado com sucesso!',
        dados = gen
        )
    )

@app.route('/generos', methods = ['DELETE']) # deleta um genero musical.
def exclui_genero():
    gen = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `generos` WHERE `id` = '{gen['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Genero excluido com sucesso!',
        dados = gen
        )
    )

#------------------------------------------------------------------------------------------------------

@app.route('/artistas', methods = ['GET']) #puxa todos os artistas do banco
def get_artistas():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM artistas')
    artistas = my_cursor.fetchall()

    artists = list()
    for artist in artistas:
        artists.append(
            {
                'id' : artist[0],
                'nome' : artist[1],
                'gravadora_id' : artist[2]
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de artistas',
        dados = artists
        )
    )


@app.route('/artistas', methods = ['POST']) #adiciona um novo artista
def novo_artista():
    artist = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `artistas` (`nome`, `gravadoras_id`) VALUES ('{artist['nome']}', '{artist['gravadoras_id']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Artista inserido com sucesso!',
        dados = artist
        )
    )

@app.route('/artistas', methods = ['PUT'])  # Altera o nome do artista
def altera_artista():
    artist = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `artistas` SET `nome` = '{artist['nome']}' WHERE `id` = '{artist['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Artista alterado com sucesso!',
        dados = artist
        )
    )


@app.route('/artistas', methods = ['DELETE']) # deleta um artista
def exclui_artista():
    artist = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `artistas` WHERE `id` = '{artist['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Artista excluido com sucesso!',
        dados = artist
        )
    )

#-------------------------------------------------------------------------------------------------------------------------

@app.route('/gravadoras', methods = ['GET']) #puxa todas as gravadoras
def get_gravadoras():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM gravadoras')
    gravadoras = my_cursor.fetchall()

    records = list()
    for rec in gravadoras:
        records.append(
            {
                'id' : rec[0],
                'nome' : rec[1],
                'valor_contrato' : str(rec[2]),
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de gravadoras',
        dados = records
        )
    )

@app.route('/gravadoras', methods = ['POST']) #adiciona uma nova gravadora
def nova_gravadora():
    record = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `gravadoras` (`nome`, `valor_contrato`) VALUES ('{record['nome']}', '{record['valor_contrato']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Gravadora inserida com sucesso!',
        dados = record
        )
    )


@app.route('/gravadoras', methods = ['PUT'])  # Altera o nome da gravadora
def altera_gravadora():
    record = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `gravadoras` SET `nome` = '{record['nome']}' WHERE `id` = '{record['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Gravadora alterada com sucesso!',
        dados = record
        )
    )

@app.route('/gravadoras', methods = ['DELETE']) # deleta uma gravadora
def exclui_gravadora():
    record = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `gravadoras` WHERE `id` = '{record['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Gravadora excluida com sucesso!',
        dados = record
        )
    )

#----------------------------------------------------------------------------------------------------------------

@app.route('/clientes', methods = ['GET']) #mostra todos os clientes
def get_clientes():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM clientes')
    clientes = my_cursor.fetchall()

    clients = list()
    for cli in clientes:
        clients.append(
            {
                'id' : cli[0],
                'login' : cli[1],
                'senha' : cli[2],
                'planos_id': cli[5],
                'email': cli[6]
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de clientes',
        dados = clients
        )
    )


@app.route('/clientes', methods = ['POST']) #adiciona um novo cliente
def novo_cliente():
    client = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `clientes` (`login`, `senha`,`planos_id`,`email`) VALUES ('{client['login']}', '{client['senha']}', '{client['planos_id']}', '{client['email']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Cliente inserido com sucesso!',
        dados = client
        )
    )


@app.route('/clientes', methods = ['PUT'])  # Altera o nome do cliente
def altera_cliente():
    client = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `clientes` SET `login` = '{client['login']}' WHERE `id` = '{client['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Cliente alterado com sucesso!',
        dados = client
        )
    )


@app.route('/clientes', methods = ['DELETE']) # deleta um cliente
def exclui_cliente():
    client = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `clientes` WHERE `id` = '{client['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Cliente excluído com sucesso!',
        dados = client
        )
    )

#------------------------------------------------------------------------------------------------

@app.route('/planos', methods = ['GET']) #mostra todos os planos
def get_planos():

    my_cursor = mydb.cursor()
    my_cursor.execute('SELECT * FROM planos')
    planos = my_cursor.fetchall()

    plans = list()
    for plan in planos:
        plans.append(
            {
                'id' : plan[0],
                'descricao' : plan[1],
                'valor' : plan[2],
                'limite': plan[3]
            }
        )

    return make_response(
        jsonify(
        mensagem = 'Lista de planos',
        dados = plans
        )
    )

@app.route('/planos', methods = ['POST']) #adiciona um novo plano
def novo_plano():
    plan = request.json

    my_cursor = mydb.cursor()

    sql = f"INSERT INTO `planos` (`descricao`, `valor`,`limite`) VALUES ('{plan['descricao']}', '{plan['valor']}', '{plan['limite']}')"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Plano inserido com sucesso!',
        dados = plan
        )
    )


@app.route('/planos', methods = ['PUT'])  # Altera o nome do plano
def altera_plano():
    plan = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `planos` SET `descricao` = '{plan['descricao']}' WHERE `id` = '{plan['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Plano alterado com sucesso!',
        dados = plan
        )
    )

@app.route('/planos', methods = ['DELETE']) # deleta um plano
def exclui_plano():
    plan = request.json

    my_cursor = mydb.cursor()

    sql = f"DELETE from `planos` WHERE `id` = '{plan['id']}'"
    my_cursor.execute(sql)
    mydb.commit()

    return make_response(
        jsonify(
        mensagem = 'Plano excluído com sucesso!',
        dados = plan
        )
    )

if __name__ == '__main__':
    
    app.run(host="localhost", port="5000", debug=True)

    # def nova_musica():
#     song = request.json

#     my_cursor = mydb.cursor()

#     sql = f"INSERT INTO `musicas` (`nome`, `duracao`, `generos_id`) VALUES ('{song['nome']}', '{song['duracao']}', '{song['generos_id']}')"
#     my_cursor.execute(sql)
#     mydb.commit()

#     return make_response(
#         jsonify(
#         mensagem = 'Música cadastrada com sucesso!',
#         dados = song
#         )
#     )