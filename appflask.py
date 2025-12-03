from flask import Flask, render_template, request, redirect
import requests

# Inicializa o app Flask
app = Flask(__name__)

# URL base da API FastAPI — onde estão os endpoints CRUD
API_URL = "http://127.0.0.1:8000"


# -----------------------------------------------------------
# ROTA PRINCIPAL (Página Inicial)
# -----------------------------------------------------------
@app.route("/")
def index():
    """
    Carrega a lista de livros consumindo o endpoint GET /livros
    da API FastAPI. Os dados recebidos em JSON são enviados para
    o template index.html renderizar na tela.
    """

    # Faz requisição GET para buscar todos os livros
    response = requests.get(f"{API_URL}/livros")

    # Se a API não responder corretamente, retorna lista vazia
    if response.status_code != 200:
        livros = []
    else:
        # Converte o JSON da API para lista de dicionários
        livros = response.json()

    # Renderiza o HTML com os livros carregados
    return render_template("index.html", livros=livros)


# -----------------------------------------------------------
# ROTA PARA ADICIONAR LIVRO
# -----------------------------------------------------------
@app.route("/add", methods=["POST"])
def add_livro():
    """
    Recebe o formulário do HTML e envia os dados para a API FastAPI,
    utilizando o endpoint POST /livros.
    """

    # Captura dados enviados pelo formulário
    novo_livro = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "ano_publicacao": int(request.form["ano_publicacao"]),
        "disponivel": True if "disponivel" in request.form else False
    }

    # Envia para a API FastAPI criando um novo livro
    requests.post(f"{API_URL}/livros", json=novo_livro)

    # Redireciona de volta para a página inicial
    return redirect("/")


# -----------------------------------------------------------
# ROTA PARA EXCLUIR UM LIVRO
# -----------------------------------------------------------
@app.route("/delete/<int:id>")
def delete_livro(id):
    """
    Remove um livro através do endpoint DELETE /livros/{id}
    da API FastAPI.
    """
    
    # Envia requisição DELETE para a API
    requests.delete(f"{API_URL}/livros/{id}")

    # Retorna para a página inicial
    return redirect("/")


# -----------------------------------------------------------
# ROTA PARA EDITAR UM LIVRO
# -----------------------------------------------------------
@app.route("/edit/<int:id>", methods=["POST"])
def edit_livro(id):
    """
    Atualiza um livro existente através do endpoint PUT /livros/{id}
    da API FastAPI.
    """

    # Dados enviados pelo formulário
    update_data = {
        "titulo": request.form["titulo"],
        "autor": request.form["autor"],
        "ano_publicacao": int(request.form["ano_publicacao"]),
        "disponivel": True if "disponivel" in request.form else False
    }

    # Faz a requisição PUT na API
    requests.put(f"{API_URL}/livros/{id}", json=update_data)

    # Retorna para a página inicial
    return redirect("/")


# -----------------------------------------------------------
# INICIALIZA O SERVIDOR FLASK
# -----------------------------------------------------------
if __name__ == "__main__":
    # Servidor rodando em http://127.0.0.1:5000
    app.run(port=5000, debug=True)

