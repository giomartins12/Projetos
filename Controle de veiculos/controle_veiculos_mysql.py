'''
- Controle para cadastro de veículos com banco de dados MySQL no
AWS RDS
'''

import mysql.connector
from mysql.connector import errorcode
from mysql.connector import errors
import os
import time
from tabulate import tabulate
import getpass

# lista de funções

def titulo():
    print("\n")
    print("\t####################################")
    print("\t#                                  #")
    print("\t# Programa de controle de veiculos #")
    print("\t#                                  #")
    print("\t####################################")
    print("\n")

def menu_opcao():
    print("\nEscolha uma opção: ")
    print("\n1.Cadastra veiculo: ")
    print("\n2.listar veiculos: ")
    print("\n3.Apagar veiculos: ")
    print("\n4.sair")

def menu_listar():
    print("\nEscolha uma opção: ")
    print("\n1.lista todos veiculos: ")
    print("\n2.lista por campo:  \n")

def menu_apagar():
    print("\nEscolha uma opção: ")
    print("\n1.Apagar todos os dados: ")
    print("\n2.Apagar um registro: ")

def cadastra_veiculo():
    inf_modelo = input("\nDigite o modelo do veiculo: ")
    inf_marca = input("\nDigite a marca do veiculo: ")
    inf_ano = input("\nDigite o ano do veiculo: ")
    inf_placa = input("\nDigite a placa do veiculo: ")
    menu = (f'{inf_modelo}', f'{inf_marca}', inf_ano, f'{inf_placa}', )
    sql = "INSERT INTO nome_da_tabela (modelo, marca, ano, placa) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, menu)
    db_connection.commit()
    cadastro = cursor.lastrowid
    print("Foi cadastrado o novo usuario de id: ", cadastro)

def lista_veiculos():
    lista_veiculo = "SELECT * FROM nome_da_tabela"
    cursor.execute(lista_veiculo)
    veiculo_result = cursor.fetchall()
    print("\n")
    print(tabulate(veiculo_result, headers=["id", "modelo", "marca", "ano", "placa"]))

def lista_pesquisa_veiculo():
    pesquisa_veiculo = input("\nDigite qual campo deseja pesquisar (modelo, marca, ano e placa): ")
    nome_pesquisa = input(f"\nDigite o(a) {pesquisa_veiculo}: ")
    lista_pesquisa = f"SELECT * FROM nome_da_tabela WHERE {pesquisa_veiculo}= '{nome_pesquisa}'"
    cursor.execute(lista_pesquisa)
    pesquisa_result = cursor.fetchall()
    print("\n")
    print(tabulate(pesquisa_result, headers=["id", "modelo", "marca", "ano", "placa"]))

def apaga_veiculos():
    apaga_veiculo = "TRUNCATE nome_da_tabela"
    cursor.execute(apaga_veiculo)
    db_connection.commit()
    print("\nApagando dados...")
    time.sleep(2)
    print("\nDados apagados!")

def apaga_veiculos_campo():
    pesquisa_apagar = input("\nDigite o campo para apagar o registro (modelo, marca, ano e placa): ")
    apaga_dado = input(f"\nDigite o(a) {pesquisa_apagar}: ")
    apaga_veiculo = f"DELETE FROM nome_da_tabela WHERE {pesquisa_apagar}= '{apaga_dado}'"
    cursor.execute(apaga_veiculo)
    db_connection.commit()
    print("\nApagando dados...")
    time.sleep(2)
    print("\nDados apagados!")

# Conexão com banco de dados

os.system('cls') or None
print("\nIniciando a conexão com banco de dados...")
time.sleep(3)
print("\n")
usuario = input("Digite o nome do usuário: ")
senha = getpass.getpass("Digite a senha: ")

try:

        db_connection = mysql.connector.connect(host='db_name.us-east-1.rds.amazonaws.com',
                                                user=f'{usuario}', password=f'{senha}', database='bd_name')
        print("\nBanco de dados conectado!\n")
        time.sleep(3)
except mysql.connector.Error as error:
       if error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("\nErro na conexão com banco de dados... verifique login ou senha!")
          print('\n')
       elif error.errno == errorcode.ER_BAD_DB_ERROR:
           print("Verifique se o banco de dados foi iniciado!")
       else:
           print(error)

else:
    cursor = db_connection.cursor()

# Instruções condicionais

    flag = True
    while flag:
        titulo()
        try:
            menu_opcao()
            opcao = int(input("\nDigite a opção: "))
            if opcao == 1:
                os.system('cls') or None
                cadastra_veiculo()
            elif opcao == 2:
                os.system('cls') or None
                menu_listar()
                opcao_lista = int(input("\nDigite a opção: "))
                if opcao_lista == 1:
                    lista_veiculos()
                elif opcao_lista == 2:
                     lista_pesquisa_veiculo()
                else:
                    print("\nOpção invalida!")
            elif opcao == 3:
                 menu_apagar()
                 opcao_apagar = int(input("\nDigite a opção: "))
                 if opcao_apagar == 1:
                    apaga_veiculos()
                 elif opcao_apagar == 2:
                     apaga_veiculos_campo()
                 else:
                    print("\nOpção invalida!")
            elif opcao == 4:
                flag = False
            else:
                print("\nOpção invalida!")
        except ValueError:
             print("\nDigite somente números!")

cursor.close()
db_connection.close()
os.system('cls') or None
titulo()
print("\nEncerrando conexão com banco de dados...")
time.sleep(3)
print("\nObrigado! volte sempre!")
time.sleep(2)
os.system('cls') or None





