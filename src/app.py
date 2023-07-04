import mysql.connector
from flask import Flask, request, jsonify, make_response

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Semestre202301',
    database = 'bancoteste1', #n3tripla
)

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/musicas', methods = ['GET']) #puxa todas as músicas da tabela músicas, tanto as que já estavam no banco quanto as criadas na api
def get_musicas(): #Concluído
    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT musicas.id, musicas.nome AS 'Nome da música', musicas.duracao AS 'Tempo de duração', artistas.nome AS 'Nome do artista'
        FROM musicas
        JOIN musicas_has_artistas ON musicas.id = musicas_has_artistas.musicas_id
        JOIN artistas ON musicas_has_artistas.artistas_id = artistas.id
        """
        my_cursor.execute(sql)
        resultado = my_cursor.fetchall()

        songs = []
        for row in resultado:
            musica = {
                'id': row[0],
                'nome': row[1],
                'duracao': str(row[2]),
                'nome do artista': row[3]
            }
            songs.append(musica)

        return make_response(jsonify({
            'mensagem': 'Lista de músicas',
            'dados': songs
        }))
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@app.route('/musicas/<int:musica_id>', methods = ['GET'])
def musica_por_id(musica_id): #Concluído
    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT musicas.nome AS 'Nome da música', musicas.duracao AS 'Tempo de duração', artistas.nome AS 'Nome do artista'
        FROM musicas
        JOIN musicas_has_artistas ON musicas.id = musicas_has_artistas.musicas_id
        JOIN artistas ON musicas_has_artistas.artistas_id = artistas.id
        WHERE musicas.id = %s
        """
        my_cursor.execute(sql, (musica_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            nome_musica, duracao, nome_artista = resultado
            musica = {'Nome da música': nome_musica, 'Tempo de duração': str(duracao), 'Nome do artista': nome_artista}
            return jsonify(musica)
        else:
            return jsonify({'mensagem': 'Música não encontrada'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500


@app.route('/musicas', methods = ['POST']) #adiciona uma nova música. id é auto incrementado e as datas são colocadas por padrão como "None"
def nova_musica(): #Concluído
    nome = request.json['nome']
    duracao = request.json['duracao']
    generos_id = request.json['generos_id']
    lancamento = request.json['lancamento']
    artistas = request.json['artistas']
    musicas_id, error = musicas_insert(nome, duracao, generos_id, lancamento)
    if error:
        return jsonify({"mensagem": "Erro ao criar música"}), 500
    error = musicas_artistas_insert(musicas_id, artistas)
    if error:
        return jsonify({"mensagem": "Erro ao relacionar artistas"}), 500
    return jsonify({"mensagem": "Música criada com sucesso"}), 201


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
def exclui_musica(): #Testar depois
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
def exclui_genero(): #Concluído
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
def get_artistas(): #Concluído
    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT artistas.id, artistas.nome AS 'Nome do artista', IFNULL(gravadoras.nome, 'Gravadora não existe') AS 'Nome da gravadora'
        FROM artistas
        LEFT JOIN gravadoras ON artistas.gravadoras_id = gravadoras.id
        """
        my_cursor.execute(sql)
        resultado = my_cursor.fetchall()

        artists = []
        for row in resultado:
            artista = {
                'id': row[0],
                'nome': row[1],
                'nome_gravadora': row[2]
            }
            artists.append(artista)

        return make_response(jsonify({
            'mensagem': 'Lista de artistas',
            'dados': artists
        }))
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@app.route('/artistas/<int:artista_id>', methods = ['GET'])
def artista_por_id(artista_id): #Concluído
    try:
        my_cursor = mydb.cursor()

        # Consulta SQL para buscar as informações do artista e suas músicas
        sql = """
        SELECT artistas.nome AS 'Nome do artista',
               IFNULL(gravadoras.nome, 'Gravadora não existe') AS 'Nome da gravadora',
               musicas.nome AS 'Nome da música'
        FROM artistas
        LEFT JOIN gravadoras ON artistas.gravadoras_id = gravadoras.id
        LEFT JOIN musicas_has_artistas ON artistas.id = musicas_has_artistas.artistas_id
        LEFT JOIN musicas ON musicas_has_artistas.musicas_id = musicas.id
        WHERE artistas.id = %s
        """
        my_cursor.execute(sql, (artista_id,))
        resultado = my_cursor.fetchall()

        if resultado:
            nome_artista, nome_gravadora, musicas = resultado[0][0], resultado[0][1], []
            for row in resultado:
                if row[2]:
                    musicas.append(row[2])

            artista = {'Nome do artista': nome_artista, 'Nome da gravadora': nome_gravadora}

            if musicas:
                artista['Músicas'] = musicas
            else:
                artista['Mensagem'] = 'O artista não possui músicas'

            return jsonify(artista)
        else:
            return jsonify({'mensagem': 'Artista não encontrado'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500
    
@app.route('/artistas', methods = ['POST']) #adiciona um novo artista
def novo_artista(): #Concluído
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
def altera_artista(): #Concluído
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
def exclui_artista(): #Concluído
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
def get_gravadoras(): #Concluído

    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT gravadoras.id, gravadoras.nome AS 'Nome da gravadora', artistas.nome AS 'Nome do artista'
        FROM gravadoras
        LEFT JOIN artistas ON gravadoras.id = artistas.gravadoras_id
        """
        my_cursor.execute(sql)
        resultado = my_cursor.fetchall()

        gravadoras = []
        for row in resultado:
            gravadora_id, gravadora_nome, artista_nome = row

            # Verifica se a gravadora já existe na lista
            gravadora_existente = next((gravadora for gravadora in gravadoras if gravadora['id'] == gravadora_id), None)
            if gravadora_existente:
                gravadora_existente['artistas'].append(artista_nome)
            else:
                gravadora = {
                    'id': gravadora_id,
                    'nome': gravadora_nome,
                    'artistas': [artista_nome] if artista_nome else []
                }
                gravadoras.append(gravadora)

        return make_response(jsonify({
            'mensagem': 'Lista de gravadoras',
            'dados': gravadoras
        }))
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@app.route('/gravadoras/<int:gravadora_id>', methods = ['GET'])
def gravadora_por_id(gravadora_id): #Concluído
    try:
        my_cursor = mydb.cursor()
        
        # Consulta para obter a gravadora
        gravadora_sql = "SELECT nome, valor_contrato FROM gravadoras WHERE id = %s"
        my_cursor.execute(gravadora_sql, (gravadora_id,))
        gravadora = my_cursor.fetchone()

        if gravadora:
            nome, valor_contrato = gravadora
            
            # Consulta para obter os artistas da gravadora
            artistas_sql = "SELECT artistas.nome FROM artistas JOIN gravadoras ON artistas.gravadoras_id = gravadoras.id WHERE gravadoras.id = %s"
            my_cursor.execute(artistas_sql, (gravadora_id,))
            artistas = [row[0] for row in my_cursor.fetchall()]
            
            # Criar o objeto de resposta
            resposta = {
                'Nome da gravadora': nome,
                'Valor do contrato': str(valor_contrato),
                'Artistas': artistas
            }
            
            return jsonify(resposta)
        else:
            return jsonify({'mensagem': 'Gravadora não encontrada'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500
    
@app.route('/gravadoras', methods = ['POST']) #adiciona uma nova gravadora
def nova_gravadora(): #Concluído
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
def altera_gravadora(): #Concluído
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
def exclui_gravadora(): #Concluído
    record = request.json

    my_cursor = mydb.cursor()

    # Primeiro, atualize a tabela artistas
    update_sql = f"UPDATE artistas SET gravadoras_id = NULL WHERE gravadoras_id = '{record['id']}'"
    my_cursor.execute(update_sql)
    mydb.commit()

    # Em seguida, delete a gravadora da tabela gravadoras
    delete_sql = f"DELETE FROM gravadoras WHERE id = '{record['id']}'"
    my_cursor.execute(delete_sql)
    mydb.commit()

    return make_response(
        jsonify(
            mensagem='Gravadora excluída com sucesso!',
            dados=record
        )
    )

#----------------------------------------------------------------------------------------------------------------

@app.route('/clientes', methods = ['GET']) #mostra todos os clientes
def get_clientes(): #Concluído

    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT id, login, senha, IFNULL(planos_id, 'sem plano') AS planos_id, email
        FROM clientes
        """
        my_cursor.execute(sql)
        clientes = my_cursor.fetchall()

        clients = []
        for cli in clientes:
            clients.append({
                'id': cli[0],
                'login': cli[1],
                'senha': cli[2],
                'planos_id': cli[3],
                'email': cli[4]
            })

        return make_response(jsonify({
            'mensagem': 'Lista de clientes',
            'dados': clients
        }))
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente_por_id(cliente_id): #Concluído
    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT id, login, senha, IFNULL(planos_id, 'sem plano') AS planos_id, email
        FROM clientes
        WHERE id = %s
        """
        my_cursor.execute(sql, (cliente_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            cliente = {
                'id': resultado[0],
                'login': resultado[1],
                'senha': resultado[2],
                'planos_id': resultado[3],
                'email': resultado[4]
            }
            return jsonify(cliente)
        else:
            return jsonify({'mensagem': 'Cliente não encontrado'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500

@app.route('/clientes', methods = ['POST']) #adiciona um novo cliente
def novo_cliente(): #Concluído
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


@app.route('/clientes', methods = ['PUT'])  # Altera o login e senha do cliente
def altera_cliente(): #Concluído
    client = request.json

    my_cursor = mydb.cursor()

    sql = f"UPDATE `clientes` SET `login` = %s, `senha` = %s WHERE `id` = %s"
    values = (client['login'], client['senha'], client['id'])
    my_cursor.execute(sql, values)
    mydb.commit()

    if my_cursor.rowcount > 0:
        return make_response(jsonify({
            'mensagem': 'Cliente alterado com sucesso!',
            'dados': client
        }))
    else:
        return jsonify({'mensagem': 'Não foi possível alterar o cliente. Verifique se o cliente existe.'}), 404


@app.route('/clientes', methods = ['DELETE']) # deleta um cliente
def exclui_cliente(): #Concluído
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
def get_planos(): #Testar se mostra apenas os que não são nulos

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

@app.route('/planos/<int:plano_id>', methods=['GET'])
def get_plano_por_id(plano_id): #Concluído
    try:
        my_cursor = mydb.cursor()
        sql = """
        SELECT * FROM planos WHERE id = %s
        """
        my_cursor.execute(sql, (plano_id,))
        resultado = my_cursor.fetchone()

        if resultado:
            plano = {
                'id': resultado[0],
                'descricao': resultado[1],
                'valor': resultado[2],
                'limite': resultado[3]
            }
            return jsonify(plano)
        else:
            return jsonify({'mensagem': 'Plano não encontrado'}), 404
    except mysql.connector.Error as error:
        return jsonify({'mensagem': f'Erro no banco de dados: {error}'}), 500
    
@app.route('/planos', methods = ['POST']) #adiciona um novo plano
def novo_plano(): #Concluído
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


@app.route('/planos', methods = ['PUT'])  # Altera o nome do plano e/ou o valor
def altera_plano(): #Concluído
    plan = request.json

    my_cursor = mydb.cursor()

    sql = "UPDATE `planos` SET `descricao` = %s, `valor` = %s WHERE `id` = %s"
    values = (plan['descricao'], plan['valor'], plan['id'])
    my_cursor.execute(sql, values)
    mydb.commit()

    if my_cursor.rowcount > 0:
        return make_response(jsonify({
            'mensagem': 'Plano alterado com sucesso!',
            'dados': plan
        }))
    else:
        return jsonify({'mensagem': 'Não foi possível alterar o plano. Verifique se o plano existe.'}), 404

@app.route('/planos', methods=['DELETE']) #Concluído
def exclui_plano():

    plan = request.json

    my_cursor = mydb.cursor()

    # Atualiza planos_id como NULL na tabela clientes para os clientes que possuem o plano sendo excluído
    update_sql = "UPDATE `clientes` SET `planos_id` = NULL WHERE `planos_id` = %s"
    my_cursor.execute(update_sql, (plan['id'],))
    mydb.commit()

    # Exclui o plano da tabela planos
    delete_sql = "DELETE FROM `planos` WHERE `id` = %s"
    my_cursor.execute(delete_sql, (plan['id'],))
    mydb.commit()

    if my_cursor.rowcount > 0:
        return make_response(jsonify({
            'mensagem': 'Plano excluído com sucesso!',
            'dados': plan
        }))
    else:
        return jsonify({'mensagem': 'Não foi possível excluir o plano. Verifique se o plano existe.'}), 404


if __name__ == '__main__':
    
    app.run(host="localhost", port="5000", debug=True)

   