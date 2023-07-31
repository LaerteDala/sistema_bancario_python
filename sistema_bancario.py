# Variável para armazenar operações
extrato = []

# Variáveis para armazenar depósitos e saques
depositos = []
saques = []

# Saldo inicial
saldo = 0

# Contadores de saques diários
saques_diarios = 0

# Menu do sistema
opcao = 1

while opcao != 0:
    print("========== Menu ==========")
    print("1. Depósito")
    print("2. Saque")
    print("3. Extrato")
    print("0. Sair")
    print("==========================")

    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        valor_deposito = float(input("Digite o valor do depósito (apenas valores positivos): "))
        if valor_deposito > 0:
            depositos.append(valor_deposito)
            saldo += valor_deposito
            extrato.append(f"Depósito: +{valor_deposito:.2f} KZ")
        else:
            print("Valor inválido para depósito. O valor deve ser positivo.")

    elif opcao == 2:
        if saques_diarios < 3:
            valor_saque = float(input("Digite o valor do saque (até 500 KZ): "))
            if valor_saque > 0 and valor_saque <= 500:
                saques.append(valor_saque)
                saldo -= valor_saque
                saques_diarios += 1
                extrato.append(f"Saque: -{valor_saque:.2f} KZ")
            else:
                print("Valor inválido para saque. O valor deve ser positivo e até 500 KZ.")
        else:
            print("Limite diário de saques atingido. Você já realizou 3 saques hoje.")

    elif opcao == 3:
        print("========== Extrato ==========")
        for operacao in extrato:
            print(operacao)
        print("                            ")
        print(f"Saldo atual: {saldo:.2f} KZ")

    elif opcao == 0:
        print("Saindo do sistema...")
        break

    else:
        print("Opção inválida. Digite um número válido conforme as opções do menu.")
