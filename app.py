# Importa as classes necessárias do Flask
from flask import Flask, render_template, request, redirect, url_for

# Cria uma instância da aplicação Flask
app = Flask(__name__)
# Define uma chave secreta para a aplicação (necessária para sessões)
app.secret_key = 'compensacao_secret_key'  # Chave secreta para sessões

# Lista em memória para armazenar os produtos (em produção, usar banco de dados)
produtos = []

# Rota principal que redireciona para a página de cadastro
@app.route('/')
def index():
    # Redireciona para a rota 'cadastrar'
    return redirect(url_for('cadastrar'))

# Rota para cadastrar produtos, aceita métodos GET e POST
@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    # Verifica se a requisição é do tipo POST (envio de formulário)
    if request.method == 'POST':
        try:
            # Obtém e limpa o nome do produto do formulário
            nome = request.form['produto'].strip()
            # Converte a quantidade para inteiro
            quantidade = int(request.form['quantidade'])
            # Converte o preço para float
            preco = float(request.form['preco_do_produto'])

            # Valida se os campos estão preenchidos corretamente
            if not nome or quantidade <= 0 or preco <= 0:
                # Lança exceção se dados forem inválidos
                raise ValueError("Dados inválidos")

            # Adiciona um novo produto à lista
            produtos.append({
                'nome': nome,          # Nome do produto
                'quantidade': quantidade,  # Quantidade em estoque
                'preco': preco         # Preço unitário
            })

            # Redireciona para a página de lista após cadastro
            return redirect(url_for('lista'))

        # Captura erros de validação ou campos faltantes
        except (ValueError, KeyError) as e:
            # Log do erro no console (para debug)
            print(f"Erro no cadastro: {e}")
            # Re-renderiza a página de cadastro com mensagem de erro
            return render_template('cadastrar.html', error="Por favor, preencha todos os campos corretamente.")

    # Se for método GET, mostra o formulário vazio
    return render_template('cadastrar.html')

# Rota para listar todos os produtos
@app.route('/lista')
def lista():
    # Calcula o valor total multiplicando preço pela quantidade de cada produto
    total = sum(p['preco'] * p['quantidade'] for p in produtos)
    # Renderiza o template lista.html passando os produtos e o total
    return render_template('lista.html', produtos=produtos, total=total)

# Rota para editar um produto específico (aceita GET e POST)
@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    # Verifica se o índice recebido é válido
    if index < 0 or index >= len(produtos):
        # Se inválido, redireciona para a lista
        return redirect(url_for('lista'))

    # Se for uma submissão de formulário (POST)
    if request.method == 'POST':
        try:
            # Atualiza os dados do produto no índice especificado
            produtos[index]['nome'] = request.form['produto'].strip()
            produtos[index]['quantidade'] = int(request.form['quantidade'])
            produtos[index]['preco'] = float(request.form['preco'])
            # Redireciona para a lista após atualização
            return redirect(url_for('lista'))
        # Captura erros de validação
        except (ValueError, KeyError) as e:
            # Log do erro no console
            print(f"Erro na edição: {e}")
            # Re-renderiza a página de edição com mensagem de erro
            return render_template('editar.html', produto=produtos[index], index=index, error="Dados inválidos")

    # Se for GET, mostra o formulário preenchido com os dados atuais
    return render_template('editar.html', produto=produtos[index], index=index)

# Rota para excluir um produto
@app.route('/excluir/<int:index>')
def excluir(index):
    # Verifica se o índice é válido antes de remover
    if 0 <= index < len(produtos):
        # Remove o produto da lista
        produtos.pop(index)
    # Redireciona para a lista após exclusão
    return redirect(url_for('lista'))

# Verifica se este arquivo está sendo executado diretamente
if __name__ == '__main__':
    # Inicia a aplicação em modo debug (reinicia automaticamente em mudanças)
    app.run(debug=True)
