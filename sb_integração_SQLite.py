import textwrap
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()


class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nif = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    data_nascimento = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    contas = relationship("Conta", back_populates="usuario", cascade="all, delete")

    @classmethod
    def novo_usuario(cls, nif, nome, data_nascimento, endereco):
        return cls(nif=nif, nome=nome, data_nascimento=data_nascimento, endereco=endereco)


class Conta(Base):
    __tablename__ = 'contas'

    id = Column(Integer, primary_key=True)
    agencia = Column(String, nullable=False)
    numero_conta = Column(Integer, nullable=False)
    saldo = Column(Float, default=0)
    limite = Column(Float, default=500)
    extrato = Column(String, default="")
    numero_saques = Column(Integer, default=0)
    limite_saques = Column(Integer, default=3)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="contas")

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
        self.agencia = "0001"
        self.numero_conta = 1

    def criar_usuario(self, session):
        cpf = input("Informe o NIF (somente número): ")
        usuario = self.filtrar_usuario(session, cpf)

        if usuario:
            print("\n@@@ Já existe usuário com esse NIF! @@@")
            return None

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        novo_usuario = Usuario.novo_usuario(nif=cpf, nome=nome, data_nascimento=data_nascimento, endereco=endereco)
        session.add(novo_usuario)
        session.commit()
        print("=== Usuário criado com sucesso! ===")
        return novo_usuario

    def filtrar_usuario(self, session, nif):
        return session.query(Usuario).filter_by(nif=nif).first()

    def criar_conta(self, session, usuario):
        if not usuario:
            print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")
            return None

        nova_conta = Conta(agencia=self.agencia, numero_conta=self.numero_conta, usuario=usuario)
        session.add(nova_conta)
        session.commit()
        self.numero_conta += 1
        print("\n=== Conta criada com sucesso! ===")
        return nova_conta

    def listar_contas(self, contas):
        for conta in contas:
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
    engine = create_engine('sqlite:///banco.db', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    banco = Banco()

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            conta = session.query(Conta).get(int(input("Informe o número da conta: ")))
            conta.depositar(valor)
            session.commit()

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            conta = session.query(Conta).get(int(input("Informe o número da conta: ")))
            conta.sacar(valor)
            session.commit()

        elif opcao == "e":
            conta = session.query(Conta).get(int(input("Informe o número da conta: ")))
            conta.exibir_extrato()

        elif opcao == "nu":
            banco.criar_usuario(session)

        elif opcao == "nc":
            cpf = input("Informe o CPF do usuário: ")
            usuario = banco.filtrar_usuario(session, cpf)
            banco.criar_conta(session, usuario)

        elif opcao == "lc":
            contas = session.query(Conta).all()
            banco.listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
