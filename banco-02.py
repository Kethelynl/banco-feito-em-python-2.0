
print('========Bem vindo ao Banco Seguro========== \nEscolha uma das opções abaixo')

def menu():
    menu = ('''

    D === Deposito
    S === Sacar
    E === Mostra extrato
    C === Criar usuário
    N === Nova conta
    L === Listar contas
    S === Sair
    ==> ''')

    return input(menu)

def deposito(deposito_valor, valortotal, extrato, /):
  
  if deposito_valor > 0:
      valortotal += deposito_valor    
      extrato += f'Valor depositado\tR${deposito_valor:.2f}\n'

      print("Depositado com sucesso!")
      
  else:
     print('!!!Esse valor é infálido!!!')

  return valortotal, extrato

def sacar(*, recebe, valortotal, extrato, saque_dia, cont):
   excedeu_saldo = recebe > valortotal
   excedeu_limite = recebe > 500
   excedeu_limite_diario = cont >= saque_dia

   if excedeu_limite:
      print("!!!!Excedeu ao limite permitido por saque!!!!")

   elif excedeu_limite_diario:
      print ('!!!!Limite diário excedido!!!!')   
   
   elif excedeu_saldo:
      print("!!!Você excedeu seu limite de seu saldo!!!!")

   elif recebe > 0:

      valortotal -= recebe
      extrato += f'Saldo retirado {recebe:.2f}\n'

      print("Valor retirado com sucesso")
   
   else:
      print("!!!Valor infálido, apenas valores maiores que 0!!!")
   return valortotal, extrato
   
def text_extrato(valortotal, /, *, extrato):
   
   print("=========EXTRATO=========")
   print("Não foram realizadas movimentações." if not extrato else extrato)
   print(f"\nsaldo\t\tR${valortotal}\n")

   return extrato

def novo_usuario(usuarios):

   cpf = input('Informe seu CPF: ')
   usuario = filtro_cpf(cpf, usuarios)

   #vê se encontrou o usuario, se sim entra nesse if
   if usuario:
      print("\n !!!! Já existe um usuário com esse cpf !!!!")
      return
   
   nome = input("Nome completo: ")
   data = input("Data de nascimento: ")
   endereco = input('Informe endereço(Logradoura, numero - bairro - cidade/sigla)')

   #trasformei em dicionario
   usuarios.append({"nome": nome, "data": data, "cpf" : cpf, "endereco" : endereco})

   print('Usuário criado com sucesso!')

def nova_conta(usuarios, contador_nova_conta):
   
   cpf = input('Informe seu CPF: ')
   usuario = filtro_cpf(cpf, usuarios)

   if usuario:
      print('Conta criada com sucesso!')
      return {"agencia": "0001", "numero_conta":contador_nova_conta, "usuario": usuario}
   
   
   print("!!!! CPF não cadastrado !!!!")
   
def listar_conta(contas):
   for conta in contas:
      listar = f"""\
      =================================================
      Agencia   = \t0001
      Numero da conta =\t{conta["numero_conta"]}
      Nome usuáio     =\t{conta["usuario"]["nome"]}
   """
   print(listar)

def filtro_cpf(cpf, usuarios):
   #  Para cada usuario na lista usuarios.if usuario['cpf'] == cpf: Se o valor da chave 'cpf' do usuario for igual ao valor da variável cpf.
   cpf_filtrar = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
   return cpf_filtrar[0] if cpf_filtrar else None

def principal():
   
   SAQUE_DIA = 3

   cont = 0
   contador_nova_conta = 0
   valortotal = 0
   extrato = ""
   deposito_valor = 0
   recebe = 0
   contas = []
   usuarios = []
  
   
   
   while True:
      
    escolha = menu().upper()

    if escolha == "D":
        deposito_valor = float(input('Valor do depósito: '))

        valortotal, extrato = deposito(deposito_valor, valortotal, extrato)

    elif escolha == "S":
        recebe = float(input(" Quando quer sacar? "))

        recebe, extrato = sacar(valortotal=valortotal, recebe=recebe,saque_dia=SAQUE_DIA, extrato=extrato, cont=cont)

        cont = cont + 1
    
    elif escolha =="E":
       text_extrato(valortotal, extrato=extrato)
    
    elif escolha == "C":
        novo_usuario(usuarios)

    elif escolha == "N":   
       contador_nova_conta = len(contas) + 1
       conta = nova_conta(usuarios, contador_nova_conta)

       if conta:
          contas.append(conta)
    
    elif escolha == "L":
       listar_conta(contas)
    
    elif escolha == "S":
       break
    else:
       print("opção inválida")
    

principal()