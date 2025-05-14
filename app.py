from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from validar_cpf import validar_cpf


app = Flask(__name__)
app.secret_key = '1qdee34_9n'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cep = db.Column(db.String(10), nullable=True)
    endereco = db.Column(db.String(200), nullable=True)
    senha = db.Column(db.String(100), nullable=False)

class Lanche(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nomeLanche = db.Column(db.String(100), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    img = db.Column(db.String(200), nullable=False)


@app.route('/')
@app.route('/index')
def index():
    lanches = Lanche.query.filter_by(tipo='Lanche').limit(7).all()
    bebidas = Lanche.query.filter_by(tipo='Bebida').limit(7).all()
    doces = Lanche.query.filter_by(tipo='Doce').limit(7).all()
    guarnicoes = Lanche.query.filter_by(tipo='Guarnicao').limit(7).all()
    return render_template('index.html', lanches=lanches, bebidas=bebidas, doces=doces, guarnicoes=guarnicoes)


@app.route('/bebida')
def bebida():
    tabela = Lanche.query.filter_by(tipo='Bebida').all()
    return render_template('bebida.html', tabela=tabela)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome').strip()
        email = request.form.get('email').strip()
        cpf = request.form.get('cpf').strip()
        senha = request.form.get('senha')
        confirmar = request.form.get('confirmar_senha')

        # 1. Verificar campos em branco
        if not nome or not email or not cpf or not senha or not confirmar:
            flash('Por favor, preencha todos os campos.', category='cadastro')
            return redirect(url_for('cadastro'))

        # 2. Verificar se o CPF é válido
        if not validar_cpf(cpf):
            flash('CPF inválido.', category='cadastro')
            return redirect(url_for('cadastro'))

        # 3. Verificar se email ou CPF já existem
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', category='cadastro')
            return redirect(url_for('cadastro'))

        if Usuario.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado.', category='cadastro')
            return redirect(url_for('cadastro'))

        # 4. Verificar se as senhas coincidem
        if senha != confirmar:
            flash('As senhas não coincidem.', category='cadastro')
            return redirect(url_for('cadastro'))

        # 5. Criar o usuário
        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(nome=nome, email=email, cpf=cpf, senha=senha_hash)

        db.session.add(novo_usuario)
        db.session.commit()

        flash('Cadastro realizado com sucesso!', category='cadastro')
        return redirect(url_for('login'))  # ou outra rota

    return render_template('cadastro.html')

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/dadoPessoal', methods=['GET', 'POST'])
def dadoPessoal():
    if 'usuario_id' not in session:
        flash('Você precisa estar logado para acessar esta página.')
        return redirect(url_for('login')) 
    
    usuario = Usuario.query.get(session['usuario_id'])
    
    if request.method == 'POST':  # Verifica se o formulário foi enviado via POST
        # Atualizando os dados do usuário
        usuario.nome = request.form['nome']
        usuario.email = request.form['email']
        
        # Atualizar senha se fornecida, caso contrário, não altera
        senha = request.form['senha']
        if senha:
            usuario.senha = generate_password_hash(senha)  # Criptografa a senha

        usuario.cep = request.form['cep']
        usuario.endereco = request.form['endereco']
        
        try:
            db.session.commit()  # Salva as alterações no banco de dados
            flash("Dados atualizados com sucesso!", "success")
            return redirect(url_for('dadoPessoal'))  # Redireciona para a mesma página
        except Exception as e:
            db.session.rollback()  # Desfaz as alterações em caso de erro
            flash("Erro ao atualizar dados. Tente novamente.", "danger")
    
    if usuario:
        return render_template('dadoPessoal.html', usuario=usuario)
    else:
        flash('Usuário não encontrado.')
        return redirect(url_for('login'))

@app.route('/guarnicao')
def guarnicao():
    tabela = Lanche.query.filter_by(tipo='Guarnicao').all()
    return render_template('guarnicao.html', tabela=tabela)

@app.route('/infoProduto/<int:id>')
def info_produto(id):
    produto = Lanche.query.get_or_404(id)
    return render_template('infoProduto.html', produto=produto)

@app.route('/lanche')
def lanche():
    tabela = Lanche.query.filter_by(tipo='Lanche').all()
    return render_template('lanche.html', tabela=tabela)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Buscar usuário no banco
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and check_password_hash(usuario.senha, senha):
            session['usuario_id'] = usuario.id
            flash('Login realizado com sucesso!', category='login')
            return redirect(url_for('index'))  # Redireciona para o index
        else:
            flash('Email ou senha inválidos.', category='login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_id', None) 
    return redirect(url_for('index'))  

@app.route('/pagamento')
def pagamento():
    return render_template('pagamento.html')

@app.route('/sobremesa')
def sobremesa():
    tabela = Lanche.query.filter_by(tipo='Doce').all()
    return render_template('sobremesa.html', tabela=tabela)















@app.route('/adicionar_carrinho', methods=['POST'])
def adicionar_carrinho():
    nome = request.form.get('nome')
    valor = float(request.form.get('valor'))
    quantidade = int(request.form.get('quantidade'))

    item = {
        'nome': nome,
        'valor': valor,
        'quantidade': quantidade,
        'total': round(valor * quantidade, 2)
    }

    # Inicializa o carrinho na sessão se não existir
    if 'carrinho' not in session:
        session['carrinho'] = []

    # Adiciona o item ao carrinho da sessão
    carrinho = session['carrinho']
    carrinho.append(item)
    session['carrinho'] = carrinho

    return redirect(url_for('carrinho'))












@app.route('/atualizar_quantidade', methods=['POST'])
def atualizar_quantidade():
    index = int(request.form.get('index'))
    acao = request.form.get('acao')

    if 'carrinho' in session:
        carrinho = session['carrinho']
        if 0 <= index < len(carrinho):
            item = carrinho[index]

            if acao == 'adicionar' and item['quantidade'] < 10:
                item['quantidade'] += 1
                item['total'] = round(item['valor'] * item['quantidade'], 2)

            elif acao == 'remover':
                item['quantidade'] -= 1
                if item['quantidade'] <= 0:
                    carrinho.pop(index)
                else:
                    item['total'] = round(item['valor'] * item['quantidade'], 2)

            session['carrinho'] = carrinho

    return redirect(url_for('carrinho'))

@app.route('/remover_item', methods=['POST'])
def remover_item():
    index = int(request.form.get('index'))

    if 'carrinho' in session:
        carrinho = session['carrinho']
        if 0 <= index < len(carrinho):
            carrinho.pop(index)
            session['carrinho'] = carrinho

    return redirect(url_for('carrinho'))
















if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=5153)