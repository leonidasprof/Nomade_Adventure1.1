#Permite manipular dados estruturados (nesse caso, os csv/txt)
import json
#Trabalha com os dados tabulados
import pandas as pd
# Permite usar Google Drive e acessar arquivos diretamente de lá
from google.colab import drive
# Verificar a existência de arquivos e manipula os caminhos de diretórios
import os

#Declaração de listas a serem utilizadas
atividades_pernambuco = []
ofertas_descontos = []
experiencias_proximas = []
acessar_perfil = []
buscar_hospedagem = []

# Montar o Google Drive no colab
drive.mount('/content/drive')

# Caminhos dos arquivos no Google Drive
caminho_atividades = '/content/drive/My Drive/NomadeAdventure/atividades.txt'
caminho_usuarios = '/content/drive/My Drive/NomadeAdventure/usuarios.txt'
caminho_rotas = '/content/drive/My Drive/NomadeAdventure/rotas.txt'

# Variável global para o nome do usuário logado
usuario_logado = ""

# Função para carregar atividades a partir do arquivo txt
def carregar_atividades(arquivo=caminho_atividades):
    if not os.path.exists(arquivo):
        print(f"Erro: Arquivo '{arquivo}' não encontrado. Verifique o caminho ou o arquivo no Google Drive.")
        return {}
    try:
        with open(arquivo, 'r', encoding='utf-8') as f:
            atividades = json.load(f)  # Lê o arquivo JSON
        print("Atividades carregadas com sucesso!")
        return atividades
    except json.JSONDecodeError:
        print("Erro: O arquivo está mal formatado. Certifique-se de que seja um JSON válido.")
        return {}

# Listar atividades carregadas
def listar_atividades(atividades_pernambuco):
    if not atividades_pernambuco:
        print("Nenhuma atividade foi carregada. Verifique o arquivo.")
        return

    print("\nAtividades Disponíveis em Pernambuco:")
    for local, atividades in atividades_pernambuco.items():
        print(f"\nLocal: {local}")
        for atividade in atividades:
            print(f" - {atividade['nome']}: {atividade['descricao']} (Valor: R${atividade['valor']})")
            print(f"   Curiosidade: {atividade['curiosidade']}")
            print(f"   Restrição: {atividade['restricao']}")
            print(f"   Dias disponíveis: {atividade['dias']}")
            print(f"   Horários: {atividade['horarios']}\n")

# Carregar atividades.txt no Google Drive
atividades_pernambuco = carregar_atividades()

# Função para carregar dados dos arquivos txt
def carregar_dados():
    try:
        usuarios = pd.read_csv('usuarios.txt')
    except FileNotFoundError:
        usuarios = pd.DataFrame(columns=["usuario", "senha", "preferencias"])
    try:
        atividades = pd.read_csv('atividades.txt')
    except FileNotFoundError:
        atividades = pd.DataFrame(columns=["codigo", "nome", "localizacao", "dificuldade", "clima"])
    try:
        rotas = pd.read_csv('rotas.txt')
    except FileNotFoundError:
        rotas = pd.DataFrame(columns=["usuario", "atividades"])
    return usuarios, atividades, rotas

# Função para carregar dados dos arquivos txt
def carregar_dados():
    try:
        usuarios = pd.read_csv(caminho_usuarios)
    except FileNotFoundError:
        usuarios = pd.DataFrame(columns=["usuario", "senha", "preferencias"])
    return usuarios

# Função para salvar dados no arquivo txt
def salvar_dados(usuarios):
    usuarios.to_csv(caminho_usuarios, index=False)
    print(f"Usuários salvos com sucesso em '{caminho_usuarios}'.")

# Função CRUD para gerenciar cadastro do usuário
def gerenciar_cadastro():
    global usuarios
    while True:
        print("\nOpções de Gerenciamento de Conta:")
        print("1. Alterar Usuário/Senha")
        print("2. Excluir Conta")
        print("3. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':  # Alterar dados
            usuario = input("Digite seu nome de usuário atual: ")
            if usuario in usuarios['usuario'].values:
                nova_senha = input("Digite sua nova senha: ")
                usuarios.loc[usuarios['usuario'] == usuario, 'senha'] = nova_senha
                salvar_dados(usuarios)
                print("Senha alterada com sucesso!")
            else:
                print("Usuário não encontrado!")
        elif escolha == '2':  # Excluir conta
            usuario = input("Digite o nome de usuário a ser excluído: ")
            if usuario in usuarios['usuario'].values:
                usuarios = usuarios[usuarios['usuario'] != usuario]
                salvar_dados(usuarios)
                print("Conta excluída com sucesso!")
            else:
                print("Usuário não encontrado!")
        elif escolha == '3':  # Voltar
            break
        else:
            print("Opção inválida!")

# Função para registrar novo usuário
def registrar_usuario():
    global usuarios
    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    if usuario in usuarios['usuario'].values:
        print("Usuário já cadastrado! Use outra opção.")
    else:
        novo_usuario = pd.DataFrame({"usuario": [usuario], "senha": [senha], "preferencias": [""]})
        usuarios = pd.concat([usuarios, novo_usuario], ignore_index=True)
        salvar_dados(usuarios)
        print("Usuário registrado com sucesso!")

# Função para fazer login
def fazer_login():
    global usuarios, usuario_logado
    usuario = input("Digite seu nome de usuário: ")
    senha = input("Digite sua senha: ")
    if ((usuarios['usuario'] == usuario) & (usuarios['senha'] == senha)).any():
        usuario_logado = usuario
        print(f"Login realizado com sucesso! Bem-vindo, {usuario}!")
        return True
    else:
        print("Usuário ou senha incorretos!")
        return False

# Função para exibir uma imagem relacionada ao passeio
def exibir_imagem_atividade(nome_atividade):
    print(f"\nExibindo imagem de {nome_atividade}...")
    # Exemplo de link de imagem para demonstração
    url_imagem = f"https://exemplo.com/imagens/{nome_atividade.replace(' ', '_').lower()}.jpg"
    print(f"Link para imagem: {url_imagem}\n")

# Função para pesquisar atividades radicais por localização em Pernambuco
def pesquisar_atividades():
    print("--"*30)
    print("Locais disponíveis para atividades radicais em Pernambuco:")
    print("--" * 30)
    for index, local in enumerate(atividades_pernambuco.keys(), start=1):
        print(f"{index}. {local}")

    escolha_local = int(input("\nEscolha um local (número): "))
    local_selecionado = list(atividades_pernambuco.keys())[escolha_local - 1]
    atividades = atividades_pernambuco[local_selecionado]

    print(f"\nAtividades disponíveis em {local_selecionado}:")
    for index, atividade in enumerate(atividades, start=1):
        print(f"{index}. {atividade['nome']}")

    escolha_atividade = int(input("Escolha uma atividade (número): "))
    atividade_selecionada = atividades[escolha_atividade - 1]

    # Exibindo detalhes da atividade selecionada
    print(f"\n--- {atividade_selecionada['nome']} ---")
    print(f"Descrição: {atividade_selecionada['descricao']}")
    print(f"Curiosidade: {atividade_selecionada['curiosidade']}")
    print(f"Dias disponíveis: {atividade_selecionada['dias']}")
    print(f"Horários: {atividade_selecionada['horarios']}")
    print(f"Valor: R$ {atividade_selecionada['valor']:.2f}")
    print(f"Restrições: {atividade_selecionada['restricao']}")

    # Exibição de imagem relacionada ao passeio
    exibir_imagem_atividade(atividade_selecionada['nome'])

# Função para exibir uma mensagem para opções externas
def mensagem_opcoes_externas():
    print("Essa ação usará funcionalidades externas, futuramente será programada com uma API específica.")

# Função para exibir o dashboard personalizado
def exibir_dashboard():
    global usuario_logado
    while True:
        print("--" * 20)
        print(f"Olá, seja bem-vindo à Nômade Adventure!\nNo que podemos te ajudar?")
        print("--" * 20)
        print("1. Pesquisar Atividades Radicais")
        print("2. Todos os Passeios PE")
        print("3. Ofertas e Descontos")
        print("4. Experiências Próximas")
        print("5. Acessar Perfil e Histórico")
        print("6. Buscar Hospedagem")
        print("7. Gerenciar Conta")
        print("--" * 20)
        escolha = input("Digite o número da opção desejada: ")
        print("--" * 20)

        if escolha == '1':
            pesquisar_atividades()
        elif escolha == '2':
            listar_atividades(atividades_pernambuco)
        elif escolha in ['3', '4', '5', '6']:
            mensagem_opcoes_externas()
        elif escolha == '7':
            gerenciar_cadastro()
        else:
            print("Opção inválida!")
        if input("Deseja voltar ao menu principal? (s/n): ").lower() == 'n':
            break

# Função principal
def main():
    global usuarios, atividades_pernambuco, usuario_logado
    atividades_pernambuco = carregar_atividades()
    usuarios = carregar_dados()

    print("--" * 30)
    print("\t...Seja bem-vindo ao Nômade Adventure!...\n\t    seu turismo radical em Pernambuco")
    print("--" * 30)

    #fluxo principal do programa
    while True:
        if input(f"\nJá tem cadastro? (s/n): ").lower() == 's':
            if fazer_login():
                exibir_dashboard()
                break
            else:
                print("Erro no login. Tente novamente.")
                if input("Deseja tentar novamente? (s/n): ").lower() != 's':
                    print(f"Encerrando o sistema. Até mais, {usuario_logado}!")
                    return
        else:
            registrar_usuario()
            exibir_dashboard()
            break
    print(f"Até mais, {usuario_logado}!")

if __name__ == "__main__":
    main()