import psycopg2
from flask import Flask, request, jsonify, render_template
from psycopg2.extras import RealDictCursor

from database import criar_conexao

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

@app.route(rule= '/filme', methods = ['GET'])
def listar_filmes():
   conn = criar_conexao()
   cursor = conn.cursor(cursor_factory=RealDictCursor)

   cursor.execute("SELECT * FROM filmes")
   resposta = cursor.fetchall()

   conn.close()

   return render_template("index.html", filmes = resposta)

@app.route(rule='/filme', methods = ['POST'])
def cadastrar_filme():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados invalidos"}), 400

    print(f'Novo filme: {dados}')

    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute(
    '''
        INSERT INTO filmes (usuario_id, titulo, ano_lancamento,
        genero, nota, capa_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    ''',
        (dados['usuario_id'], dados['titulo'], dados['ano_lancamento'], dados['genero'],
         dados['nota'], dados['capa_url'])
    )

    novo_id = cursor.fetchone()[0]
    conn.commit()

    conn.close()


    return jsonify(
        {"message": "Filme salvo com sucesso!",
         "fime_id": novo_id
         }
    ), 201


@app.route(rule='/produto', methods = ['PUT'])
def atualizar_produto():
    produto = {"id":1,
    "nome": "Caneta azul",
    "preco": 1.5,
    "descricao": "Caneta esfereográfica",
    "marca":"bic"}

    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados invalidos"}), 400

    if dados["id"] == produto["id"]:
        produto = dados
        print(f"Novo produto: {produto}")
        return jsonify({"message": "produto atualizado com sucesso!"}), 201
    else:
        return jsonify({"message": "produto não encontrado!"}), 404

@app.route('/teste/db', methods = ['GET'])
def testar_conexao():
    conn = criar_conexao()
    print('Testando conexao', conn)
    conn.close()
    return jsonify({"message": "Banco conectado com sucesso!"}), 200




if __name__ == '__main__':
    app.run(debug=True)

