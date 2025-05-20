import sqlite3
import os

# Caminho correto para o banco dentro da pasta instance
caminho_banco = os.path.join("instance", "site.db")

# Conexão com o banco
conn = sqlite3.connect(caminho_banco)
cursor = conn.cursor()

# Lista de bebidas
bebidas = [
    ("Fanta Laranja 2l", "Bebida", 1, "Refrigerante sabor laranja de 2 litros, ideal para compartilhar.", "fantalaranja2l.png"),
    ("Fanta Laranja em Lata", "Bebida", 1, "Fanta Laranja em lata, refrescante e perfeita para uma pausa rápida.", "fantalaranjalata.png"),
    ("Fanta Uva 2l", "Bebida", 1, "Refrigerante sabor uva de 2 litros, sabor marcante para todos os momentos.", "fantauva2l.png"),
    ("Fanta Uva em Lata", "Bebida", 1, "Fanta Uva em lata, prática e deliciosa para qualquer ocasião.", "fantauvalata.png"),
    ("Guaraná 2l", "Bebida", 1, "Tradicional refrigerante de guaraná em embalagem de 2 litros.", "guarana2l.png"),
    ("Guaraná em Lata", "Bebida", 1, "Guaraná em lata, sabor brasileiro em dose individual.", "guaranalata.png"),
    ("Guaraná Zero em Lata", "Bebida", 1, "Guaraná sem açúcar, em lata, para quem busca leveza sem perder o sabor.", "guaranazerolata.png"),
    ("Pepsi 2l", "Bebida", 1, "Refrigerante Pepsi em garrafa de 2 litros, refrescância para dividir.", "pepsi2l.png"),
    ("Pepsi Black em Lata", "Bebida", 1, "Pepsi Black sem açúcar em lata, ideal para acompanhar lanches.", "pepsiblacklata.png"),
    ("Pepsi Lata", "Bebida", 1, "Pepsi tradicional em lata, sabor intenso e refrescante.", "pepsilata.png"),
    ("Sprite 2l", "Bebida", 1, "Sprite limonada gaseificada, embalagem de 2 litros.", "sprite2l.png"),
    ("Sprite Em Lata", "Bebida", 1, "Sprite em lata, refrescante e com sabor cítrico.", "spritelata.png"),
    ("Suco Laranja", "Bebida", 1, "Suco natural sabor laranja, rico em vitamina C.", "sucolaranja.png"),
    ("Suco Limão", "Bebida", 1, "Suco de limão, levemente ácido e muito refrescante.", "sucolimao.png"),
    ("Suco Maracujá", "Bebida", 1, "Suco de maracujá, sabor tropical e calmante.", "sucomaracuja.png"),
    ("Suco Uva", "Bebida", 1, "Suco de uva concentrado, doce e nutritivo.", "sucouva.png"),
    ("Sukita Uva 2L", "Bebida", 1, "Refrigerante Sukita sabor uva em garrafa de 2 litros.", "sukita2.png"),
    ("Sukita Laranja 2l", "Bebida", 1, "Sukita laranja com muito gás e sabor, embalagem 2 litros.", "sukitalaranja2I.png"),
    ("Sukita Laranja em Lata", "Bebida", 1, "Sukita laranja em lata, perfeita para lanches rápidos.", "sukitalaranjalata.png"),
    ("Sukita Uva em Lata", "Bebida", 1, "Sukita uva em lata, com sabor marcante e refrescante.", "sukitalata.png")
]

# Inserção dos dados
cursor.executemany("""
    INSERT INTO lanche (nomeLanche, tipo, valor, descricao, img)
    VALUES (?, ?, ?, ?, ?)
""", bebidas)

# Salvar e fechar
conn.commit()
conn.close()

print("Dados inseridos com sucesso!")
