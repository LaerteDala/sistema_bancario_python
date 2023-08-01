import textwrap

class Usuario:
    def __init__(self, nif, nome, data_nascimento, endereco):
        self.nif = nif
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.endereco = endereco

class Conta:
    def __init__(self, agencia, numero_conta, usuario):
        self.agencia = agencia
        self.numero_conta = numero_conta
        self.usuario = usuario
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0
        self.limite_saques = 3

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tKZ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= self.limite_saques

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tKZ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tKZ {self.saldo:.2f}")
        print("==========================================")


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia = "0001"
        self.numero_conta = 1

    def criar_usuario(self):
        cpf = input("Informe o NIF (somente número): ")
        usuario = self.filtrar_usuario(cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse NIF! @@@")
            return None

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        novo_usuario = Usuario(cpf, nome, data_nascimento, endereco)
        self.usuarios.append(novo_usuario)
        print("=== Usuário criado com sucesso! ===")
        return novo_usuario

    def filtrar_usuario(self, nif):
        usuarios_filtrados = [usuario for usuario in self.usuarios if usuario.nif == nif]
        return usuarios_filtrados[0] if usuarios_filtrados else None

    def criar_conta(self, usuario):
        if not usuario:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
            return None

        nova_conta = Conta(self.agencia, self.numero_conta, usuario)
        self.contas.append(nova_conta)
        self.numero_conta += 1
        print("\n=== Conta criada com sucesso! ===")
        return nova_conta

    def listar_contas(self):
        for conta in self.contas:
            linha = f"""\
                Agência:\t{conta.agencia}
                C/C:\t\t{conta.numero_conta}
                Titular:\t{conta.usuario.nome}
            """
            print("=" * 100)
            print(textwrap.dedent(linha))


def menu():
    menu = """\n
    ================ MENU ================
    [d]\t Depositar
    [s]\t Sacar
    [e]\t Extrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\t Sair
    => """
    return input(textwrap.dedent(menu))


def main():
    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta = banco.contas[int(input("Informe o número da conta: ")) - 1]
            conta.depositar(valor)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta = banco.contas[int(input("Informe o número da conta: ")) - 1]
            conta.sacar(valor)

        elif opcao == "e":
            conta = banco.contas[int(input("Informe o número da conta: ")) - 1]
            conta.exibir_extrato()

        elif opcao == "nu":
            banco.criar_usuario()

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(cpf)
            banco.criar_conta(usuario)

        elif opcao == "lc":
            banco.listar_contas()

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
