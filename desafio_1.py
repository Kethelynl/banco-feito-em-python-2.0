from abc import ABC, abstractclassmethod,abstractproperty

from datetime import datetime


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
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()     
    @classmethod    
    def saldo(cls, cliente, numero):
        return cls(numero, cliente)
    @property
    def nova_conta(self):
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
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("*****Operação falhou, Não tem saldo*****")

        elif valor > 0:
                self._saldo -= valor
                print("======Saque realizado com sucesso======")
                return True
        else:
            print("*******Operação falhou, valor informado invalido")
        return False    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("======Deposito realizado com sucesso====")
        else:
            print("**********Operação falhou, valor infalido ")
            return False
        return True
    
class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque
    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacao if transacao["tipo"] == Saque.__name__]
        )    

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saque >= self.limite_saque

        if excedeu_limite:
            print("******Valor informado excedeu o limite******")
        elif excedeu_saques:
            print("*******Numero maximo de saques excedido******")
        else: 
            return super().sacar(valor)
        return False
    def __str__(self):
        return f"""
            agencia:\t{self.agencia}
            C\C\t{self.numero}
            titular:\t{self.cliente.nome}
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
            "data": datetime.now().strftime
            ("%d-%m-%Y %H:%M:%s"),
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
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)