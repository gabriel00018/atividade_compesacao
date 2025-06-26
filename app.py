from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'compensacao_secret_key'  # Chave secreta para sessões

# Lista para armazenar produtos
produtos = []


@app.route('/')
def index():
    return redirect(url_for('cadastrar'))


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        try:
            # Obter e validar dados do formulário
            nome = request.form['produto'].strip()
            quantidade = int(request.form['quantidade'])
            preco = float(request.form['preco_do_produto'])

            if not nome or quantidade <= 0 or preco <= 0:
                raise ValueError("Dados inválidos")

            # Adicionar novo produto
            produtos.append({
                'nome': nome,
                'quantidade': quantidade,
                'preco': preco
            })

            return redirect(url_for('lista'))

        except (ValueError, KeyError) as e:
            print(f"Erro no cadastro: {e}")
            return render_template('cadastrar.html', error="Por favor, preencha todos os campos corretamente.")

    return render_template('cadastrar.html')


@app.route('/lista')
def lista():
    # Calcular valor total
    total = sum(p['preco'] * p['quantidade'] for p in produtos)
    return render_template('lista.html', produtos=produtos, total=total)


@app.route('/editar/<int:index>', methods=['GET', 'POST'])
def editar(index):
    # Verificar se o índice é válido
    if index < 0 or index >= len(produtos):
        return redirect(url_for('lista'))

    if request.method == 'POST':
        try:
            # Atualizar produto
            produtos[index]['nome'] = request.form['produto'].strip()
            produtos[index]['quantidade'] = int(request.form['quantidade'])
            produtos[index]['preco'] = float(request.form['preco'])
            return redirect(url_for('lista'))
        except (ValueError, KeyError) as e:
            print(f"Erro na edição: {e}")
            return render_template('editar.html', produto=produtos[index], index=index, error="Dados inválidos")

    return render_template('editar.html', produto=produtos[index], index=index)


@app.route('/excluir/<int:index>')
def excluir(index):
    if 0 <= index < len(produtos):
        produtos.pop(index)
    return redirect(url_for('lista'))


if __name__ == '__main__':
    app.run(debug=True)