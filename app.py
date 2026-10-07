from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '<h1>Hello World!</h1>'

@app.route(rule= '/usuario', methods = ['GET'])
def buscar_usuario():
    usuario = {
        "nome": "Manoel",
        "idade": 16,
        "telefone": "(19) 997920205"
    }
    return usuario

@app.route(rule='/produto', methods = ['POST'])
def cadastrar_produto():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados invalidos"}), 400

    print(f'Novos produtos: {dados}')

    return jsonify(
        {"message": "Produto salvo com sucesso!"}), 201


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




if __name__ == '__main__':
    app.run(debug=True)

