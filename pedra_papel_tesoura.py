import os
import random

lista_jogadas = {0:'papel',1:'pedra',2:'tesoura'}

def mostrar_jogada(x,y):
    print('========')
    print(f'Sua jogada: {lista_jogadas[x]}')
    print(f'Jogada do computador: {lista_jogadas[y]}')



print('========')
print('Bem vindo ao jogo de Pedra, Papel e Tesoura')      
print('========\n\n\n\n\n')

contatdor_pessoa = 0
contador_computador = 0

print(f'Placar:\nVocê:{contatdor_pessoa}\nMaquina:{contador_computador}\n\n\n\n')
while True:
    print('Escolha o seu lance:')
    print('0 - Papel | 1 - Pedra | 2 - Tesoura')
    while True:
        jogada_pessoa = int(input())
        if jogada_pessoa not in [0,1,2]:
            print('Opção não valida, escolha entre 0, 1 ou 2')
            jogada_pessoa = int(input())
        else:
            break

    jogada_computador = random.randint(0,2)

    if jogada_pessoa == 0:
        if jogada_computador == 0:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Empate!')
            print('========')
            
        elif jogada_computador == 1:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você venceu!')
            print('========')
            contatdor_pessoa += 1
            
        else:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você Perdeu!')
            print('========')
            contador_computador +=1

    elif jogada_pessoa == 1:
        if jogada_computador == 0:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você Perdeu!')
            print('========')
            contador_computador +=1
            
        elif jogada_computador == 1:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Empate!')
            print('========')
            
        else:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você venceu!')
            print('========')
            contatdor_pessoa += 1

    else:
        if jogada_computador == 0:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você venceu!')
            print('========')
            contatdor_pessoa += 1
            
        elif jogada_computador == 1:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Você Perdeu!')
            print('========')
            contador_computador +=1
            
        else:
            mostrar_jogada(jogada_pessoa,jogada_computador)
            print('Empate!')
            print('========')
    print('Jogar novamente? 0 - SIM | 1 - NÃO')        
    while True:
        continuar = int(input())
        if continuar not in [0,1]:
            print('Opção invalida! Escolha se quer continuar (0) ou deseja parar (1)')
            continuar = int(input())
        else:
            break

    if continuar == 0:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'Placar:\nVocê:{contatdor_pessoa}\nMaquina:{contador_computador}\n\n\n\n')
        continue

    else:
        break   


    

        
    
