'''
Criar rotina de cálculo de carrinho de compras:
- Deve ser baseado em um dicionário ou lista.
- Depois você precisa enumerar ao menos 3 itens para ele somar e dar o preço final.
- Quantidades diferentes de cada item.
'''

import os


compras = []
while True:
     produto = input("\nDigite o produto (digite 'fim' para sair): ")
     if produto == "fim":
         break
     quantidade = float(input("Digite a quantidade: "))
     preço = float(input("Digite o preço: "))
     compras.append([produto, quantidade, preço])

soma = 0.0
os.system('cls') or None

print("\n###################################")
print("Prod.   Quant.  Vr.UN  Vr.Total")
print("-----------------------------------")

for compra in compras:
     print("%5s  %2.1f   R$%3.2f  R$%5.2f" % (compra[0], compra[1], compra[2], compra[1] * compra[2]))
     soma += compra[1] * compra[2]

print("-----------------------------------")
print("Total: R$%5.2f" % soma)
print("###################################\n")