# Lista para armazenar usuários e contas correntes
usuarios = []
contas_correntes = []
prox_num_conta = 1
AGENCIA_PADRAO = "0001"

class Usuario:
    def __init__(self, nome, data_nascimento, nif, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.nif = nif
        self.endereco = endereco

def criar_usuario():
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário: ")
    nif = input("Digite o NIF do usuário (apenas números): ")
    endereco = input("Digite o endereço do usuário (logradouro, nro, bairro, cidade, estado): ")

    # Verifica se o NIF já está cadastrado
    nif_numeros = ''.join(filter(str.isdigit, nif))
    for usuario in usuarios:
        if usuario.nif == nif_numeros:
            print("NIF já cadastrado. Não é possível criar o usuário.")
            return

    usuario = Usuario(nome, data_nascimento, nif_numeros, endereco)
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")

class ContaCorrente:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.extrato = []
        self.saques_diarios = 0

def criar_conta_corrente():
    global prox_num_conta

    if not usuarios:
        print("Não há usuários cadastrados. Crie um usuário primeiro.")
        return

    usuario_nif = input("Digite o NIF do usuário para vincular à conta (apenas números): ")
    usuario_encontrado = None

    for usuario in usuarios:
        if usuario.nif == usuario_nif:
            usuario_encontrado = usuario
            break

    if not usuario_encontrado:
        print("NIF não encontrado. Verifique o número e tente novamente.")
        return

    conta = ContaCorrente(AGENCIA_PADRAO, prox_num_conta, usuario_encontrado)
    contas_correntes.append(conta)
    prox_num_conta += 1
    print(f"Conta corrente criada com sucesso! Número da conta: {conta.numero_conta}")

def deposito(conta, valor_deposito):
    conta.saldo += valor_deposito
    conta.extrato.append(f"Depósito: +{valor_deposito:.2f} KZ")

def saque(conta, valor_saque):
    if conta.saques_diarios < 3:
        if valor_saque <= conta.saldo and valor_saque <= 500:
            conta.saldo -= valor_saque
            conta.saques_diarios += 1
            conta.extrato.append(f"Saque: -{valor_saque:.2f} KZ")
        else:
            print("Valor inválido para saque. Verifique o saldo e o limite máximo (500 KZ).")
    else:
        print("Limite diário de saques atingido. Você já realizou 3 saques hoje.")

def mostrar_extrato(conta):
    print("========== Extrato ==========")
    for operacao in conta.extrato:
        print(operacao)
    print("                            ")
    print(f"Saldo atual: {conta.saldo:.2f} KZ")

def menu():
    print("========== Menu ==========")
    print("1. Criar usuário")
    print("2. Criar conta corrente")
    print("3. Depósito")
    print("4. Saque")
    print("5. Extrato")
    print("0. Sair")
    print("==========================")
    opcao = int(input("Escolha uma opção: "))
    return opcao

while True:
    opcao = menu()

    if opcao == 1:
        criar_usuario()

    elif opcao == 2:
        criar_conta_corrente()

    elif opcao == 3:
        if contas_correntes:
            num_conta = int(input("Digite o número da conta para depósito: "))
            conta_encontrada = None

            for conta in contas_correntes:
                if conta.numero_conta == num_conta:
                    conta_encontrada = conta
                    break

            if not conta_encontrada:
                print("Conta não encontrada. Verifique o número e tente novamente.")
            else:
                valor_deposito = float(input("Digite o valor do depósito (apenas valores positivos): "))
                if valor_deposito > 0:
                    deposito(conta_encontrada, valor_deposito)
                else:
                    print("Valor inválido para depósito. O valor deve ser positivo.")
        else:
            print("Crie uma conta corrente primeiro.")

    elif opcao == 4:
        if contas_correntes:
            num_conta = int(input("Digite o número da conta para saque: "))
            conta_encontrada = None

            for conta in contas_correntes:
                if conta.numero_conta == num_conta:
                    conta_encontrada = conta
                    break

            if not conta_encontrada:
                print("Conta não encontrada. Verifique o número e tente novamente.")
            else:
                valor_saque = float(input("Digite o valor do saque (até 500 KZ): "))
                saque(conta_encontrada, valor_saque)
        else:
            print("Crie uma conta corrente primeiro.")

    elif opcao == 5:
        if contas_correntes:
            num_conta = int(input("Digite o número da conta para mostrar o extrato: "))
            conta_encontrada = None

            for conta in contas_correntes:
                if conta.numero_conta == num_conta:
                    conta_encontrada = conta
                    break

            if not conta_encontrada:
                print("Conta não encontrada. Verifique o número e tente novamente.")
            else:
                mostrar_extrato(conta_encontrada)
        else:
            print("Crie uma conta corrente primeiro.")

    elif opcao == 0:
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Digite um número válido conforme as opções do menu.")
