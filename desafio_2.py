from abc import ABC, abstractclassmethod,abstractproperty

from datetime import datetime

import textwrap

class Cliente:


    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    def fazer_transacao(self, conta, transacao):
        transacao.registrar(conta)
    def adicionar_conta(self, conta):
        self.contas.append(conta)      

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento    
        super().__init__(endereco)

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print("*****Operação falhou, Não tem saldo*****")
            return False
        elif valor > 0:
            self._saldo -= valor
            print("======Saque realizado com sucesso======")
            return True
        else:
            print("*******Operação falhou, valor informado inválido")
            return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("======Depósito realizado com sucesso====")
            return True
        else:
            print("**********Operação falhou, valor inválido ")
            return False
    
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    @classmethod
    def criar_nova_conta(cls, cliente, numero):
        return cls(numero=numero, cliente=cliente)

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque >= self.limite_saque

        if excedeu_limite:
            print("******Valor informado excedeu o limite******")
        elif excedeu_saques:
            print("*******Número máximo de saques excedido******")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            Conta:\t{self.numero}
            Titular:\t{self.cliente.nome}
         """
    def __str__(self):
        return f"""
            Agência:\t{self.agencia}
            Conta:\t{self.numero}
            Titular:\t{self.cliente.nome}
         """

class Historico:
    def __init__(self):
        self._transacao = []

    @property
    def transacoes(self):
        return self._transacao

    def adicionar_transacao(self, transacao):
        self._transacao.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        })

class transacao(ABC):
    
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

class Saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Saque(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            conta.historico.adicionar_transacao(self)


print('========Bem vindo ao Banco Seguro========== \nEscolha uma das opções abaixo')

def menu():
    menu = ('''

    D === Deposito
    S === Sacar
    E === Mostra extrato
    C === Criar usuário
    N === Nova conta
    L === Listar contas
    X === Sair
    ==> ''')

    return input(menu)

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n*****Cliente não possui conta******")
        return None
    return cliente.contas[0]

def deposito(clientes):
    cpf = input("Informe o seu CPF: ")
    cliente = filtro_cpf(cpf, clientes)
    if not cliente:
        print("***** Cliente não encontrado******")
        return
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.fazer_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_cpf(cpf, clientes)
    if not cliente:
        print("*****Cliente não encontrado******")
        return
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    cliente.fazer_transacao(conta, transacao)

def text_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtro_cpf(cpf, clientes)

    if not cliente:
      print("*****Cliente não encontrado******")
      return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    print("\n =================EXTRATO=============")
    transacoes= conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas Movimentações"
    else:
        for transacao in transacoes:
            extrato += f"{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\n\tR${conta.saldo:.2f}")            

def novo_usuario(clientes):

   cpf = input('Informe seu CPF: ')
   cliente = filtro_cpf(cpf, clientes)

   #vê se encontrou o usuario, se sim entra nesse if
   if cliente:
      print("\n !!!! Já existe um usuário com esse cpf !!!!")
      return
   
   nome = input("Nome completo: ")
   data_nascimento = input("Data de nascimento: ")
   endereco = input('Informe endereço(Logradoura, numero - bairro - cidade/sigla)')

   cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento = data_nascimento, endereco=endereco)

   clientes.append(cliente)

   print('=======Usuário criado com sucesso!========')

def nova_conta(clientes, contador_nova_conta, contas):
    cpf = input('Informe seu CPF: ')
    cliente = filtro_cpf(cpf, clientes)

    if not cliente:
        print('*******Cliente não encontrado******')
        return

    conta = Conta_corrente.criar_nova_conta(cliente=cliente, numero=contador_nova_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("=====Conta criada com sucesso=====")
   
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def filtro_cpf(cpf, clientes):
    for cliente in clientes:
        if cliente.cpf == cpf:
            return cliente
    return None

def principal():
    clientes = []
    contas = []

    while True:
        escolha = menu().upper()

        if escolha == "D":
            deposito(clientes)
        elif escolha == "S":
            sacar(clientes)
        elif escolha == "E":
            text_extrato(clientes)
        elif escolha == "C":
            novo_usuario(clientes)
        elif escolha == "N":
            contador_nova_conta = len(contas) + 1
            nova_conta(clientes, contador_nova_conta, contas)
        elif escolha == "L":
            listar_contas(contas)
        elif escolha == "X":
            break
        else:
            print("Opção inválida")

principal()