import textwrap
from abc import ABC, abstractclassmethod , abstractproperty 
from datetime import datetime

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
       return self._transacoes
    
    def adicionar_transacoes(self,transacao):
       self._transacoes.append({
          "Tipo": transacao.__class__.__name__,
          "Valor" : transacao.valor,
          "data": datetime.now().strftime("%d -%m -%Y  %H:%M:%s"),
       })

class Conta:

    def __init__(self,numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente , numero):
        return cls(cliente, numero)
        
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
      saldo = self.saldo
      excedeu_saldo = valor > saldo


      if excedeu_saldo:
        print("Saldo insuficiente, verifique novamente")
      elif valor > 0:
         print("Saque realizado com sucesso, Obrigado por ser nosso cliente!")
         return True
      else:
         print("=== operação falhou, digite o valor correto ===")
         return False
        
    def depositar(self,valor):
     if valor > 0:
      self.saldo += valor
      print("Deposito realizado, obrigado por ser nosso cliente!")
     else:
       print("Falha na operação, valor invalido!")
       return False
            
            
     return True          

class Conta_corrente(Conta):
    def __init__(self, numero, cliente, limite = 500, limite_saque = 3):
       super().__init__(numero, cliente)
       self.limite = limite
       self.limite_saque = limite_saque

    def sacar(self, valor):
       numero_saques = len([transacao for transacao in self.historico.transacoes 
                            if transacao ["tipo"] == Saque.__name__])
       

       excedeu_limite = valor > self.limite
       excedeu_saque = numero_saques >= self.limite_saque 


       if excedeu_limite:
           print("Limite excedido!")

       elif excedeu_saque:
           print("Limite de saques atingido")

       else:
          return super().sacar(valor)
       
       return False
    
    def __str__(self):
       return f""" \\
         Agência :\t{self.agencia} 
         CC : \t {self.numero}
         Titular : \t {self.cliente.nome}
         """
        
class Cliente:
    def __init__(self, endereco):
        self.contas = []
        self.endereco = endereco 

    def realizar_transacao(self, conta , transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class Pessoa_fisica(Cliente):
    def __init__(self, endereco,cpf,nome,data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        super().__init__(endereco)

class Transacao(ABC):
   @property
   @abstractproperty
   def valor(self):
      pass
   
   @abstractclassmethod
   def registra(self,conta):
      pass
   
class Saque(Transacao):
   def __init__(self, valor):
    self._valor = valor

   @property
   def valor(self):
      return self._valor
   
   def registrar(self,conta):
      sucesso_transacao = conta.sacar(self.valor)

      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
     self._valor = valor

    @property
    def valor(self):
      return self._valor
   
    def registrar(self,conta):
      sucesso_transacao = conta.depositar(self.valor)

      if sucesso_transacao:
         conta.historico.adicionar_transacao(self)

def menu():
    menu = """\n
    ===========MENU=========

    [d ]\tDepositar
    [s ]\tSacar
    [e ]\tExtrato
    [q ]\tSair
    [nc]\tNova conta
    [nu]\tNovo usuario
    [lc]\tlistar contas   
   
    Selecione a opção desejada => """
    return input(menu)


def depositar(cliente):
   cpf = input("Informe o CPF do cliente:  ")
   cliente = filtrar_cliente(cpf,cliente)

   if not cliente:
      print("========= Cliente não encontrado ===========")
      return
   
   valor = float(input("Informe o valor do deposito:  "))
   transacao = Deposito(valor)


   conta = recuperar_conta_cliente(cliente)

   if not conta:
      return
   
   cliente.realiza_transacao(conta,transacao)



def sacar (cliente):
   cpf = input("Informe o CPF do cliente:  ")
   cliente = filtrar_cliente(cpf,cliente)

   if not cliente:
      print("========= Cliente não encontrado ===========")
      return
   
   valor = float(input("Informe o valor do Saque:  "))
   transacao = Saque(valor)


   conta = recuperar_conta_cliente(cliente)

   if not conta:
      return
   
   cliente.realiza_transacao(conta,transacao)
   
def exibir_extrato(cliente):
   cpf = input("Informe o CPF do cliente:  ")
   cliente = filtrar_cliente(cpf,cliente)

   if not cliente:
      print("========= Cliente não encontrado ===========")
      return
   
   conta = recuperar_conta_cliente(cliente)

   if not conta:
      return
   


   print("\n================ EXTRATO ================")
   transacoes = conta.historico.transacoes

   extrato = ""
   if not transacoes:
        extrato = "Não foram realizadas movimentações."
   else:
       for transacao in transacoes:
           extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

   print(extrato)
   print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
   print("==========================================")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n========= Cliente não possui conta! ==========")
        return

    return cliente.contas[0]
   

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = Conta_corrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


   
   
def main():
   cliente = []
   conta = []

   while True:
      opcao = menu()
      if opcao =="d":
         depositar(cliente)

      elif opcao == "s":
         sacar(cliente)

      elif opcao == "e":
         exibir_extrato(cliente)

      elif opcao == "nc":
         numero_conta = len(conta) + 1
         criar_conta(numero_conta, cliente ,conta)

      elif opcao == "nu":
         criar_cliente(cliente)

      elif opcao == "lc":
         listar_contas(cliente)

      elif opcao == "q":
         break
      
      
      else:
        print("Operação invalida, por favor selecione novamente a operação desejada")

main()
        














      

   







