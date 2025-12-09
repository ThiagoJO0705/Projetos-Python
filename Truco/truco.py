import random

def play_truco():
    print('Qual o tipo de baralho você quer usar?')
    print('1 - Baralho Limpo')
    print('2 - Baralho Sujo')
    truco_option = input('Escolha uma opção (1 ou 2): ').strip()
    match truco_option:
        case '1':
            print('Você escolheu o Baralho Limpo!')
        case '2':
            print('Você escolheu o Baralho Sujo!')
        case _:
            print('Opção inválida! Usando baralho sujo por padrão.')

def rules_truco():
    print("\nRegras Gerais")
    print("---------------------------------------------------------")
    print("Objetivo: Fazer 12 pontos para vencer a partida.")
    print("Mão: Cada rodada (melhor de 3 rodadas) vale inicialmente 1 ponto.")
    print("Rodadas: A mão é disputada em melhor de três. O time que vencer duas rodadas, vence a mão.")
    print("Pontuação (O Truco): O valor da mão pode ser aumentado com o pedido de Truco:")
    print("  -  Truco: 3 pontos")
    print("  -  Seis: 6 pontos")
    print("  -  Nove: 9 pontos")
    print("  -  Doze: 12 pontos")
    print("Hierarquia das Manilhas: Definida pela 'Vira'. A ordem de força é sempre:")
    print("(Mais Forte)  ♣ Paus (mais conhecido como Zap) > ♥ Copas > ♠ Espadas (mais conhecido como Espadilha) > ♦ Ouros (mais conhecido como Pikafumo) (Mais Fraco)")
    print("\nHierarquia das Cartas")
    print("---------------------------------------------------------")
    print("A força das cartas é dividida em dois grupos: as Manilhas e as Cartas Normais.")
    print("\nCartas Normais do Baralho Sujo(do mais forte ao mais fraco)")
    normal_hierarchy_dirty_deck = ['3', '2', 'A', 'K', 'J', 'Q', '7', '6', '5', '4']
    print(f"Ordem: {' > '.join(normal_hierarchy_dirty_deck)}")
    print("\nCartas Normais do Baralho Limpo(do mais forte ao mais fraco)")
    normal_hierarchy_clean_deck = ['3', '2', 'A', 'K', 'J', 'Q']
    print(f"Ordem: {' > '.join(normal_hierarchy_clean_deck)}")
    print("\n - Importante: Dentro das cartas normais, os naipes não possuem diferença de força.")
    print("\nManilhas")
    print("São as quatro cartas imediatamente superiores à carta virada, sendo a mais forte a de ♣ Paus (Zap), seguida por ♥ Copas, ♠ Espadas (Espadilha)  e ♦ Ouros (Pikafumo).")
    
    print("\nRegras da Vira e Manilhas")
    print("---------------------------------------------------------")
    print("Vira: É a carta que determina quais serão as manilhas na rodada. A manilha é a carta seguinte da vira.")
    order_strength = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
    suits_manilha = ['♦', '♠', '♥', '♣']
    
    card_vira = random.choice(order_strength)
    index_vira = order_strength.index(card_vira)
    manilha_card = random.choice(suits_manilha)
    print("\nExemplo de Vira e Manilhas:")
    print(f"A carta virada é: {card_vira} {manilha_card}")
    if index_vira == len(order_strength) - 1:
        next_card = order_strength[0]
    else:
        next_card = order_strength[index_vira + 1]
    print(f"As manilhas serão as cartas: {next_card} ♣ (Zap), {next_card} ♥, {next_card} ♠ (Espadilha), {next_card} ♦ (Pikafumo)")

    print("\n**Conclusão da Força Total:**")
    print("A força total das cartas em Truco é determinada primeiro pelas manilhas, seguidas pelas cartas normais.")
    print('Zap > Copas > Espadilha > Pikafumo > 3 > 2 > A > K > J > Q > 7 > 6 > 5 > 4 (Baralho Sujo)')
    print('Zap > Copas > Espadilha > Pikafumo > 3 > 2 > A > K > J > Q (Baralho Limpo)')


    


deck_dirty = [['4 ♥', '5 ♥', '6 ♥', '7 ♥', 'Q ♥', 'J ♥', 'K ♥', 'A ♥', '2 ♥', '3 ♥'], 
              ['4 ♦', '5 ♦', '6 ♦', '7 ♦', 'Q ♦', 'J ♦', 'K ♦', 'A ♦', '2 ♦', '3 ♦'], 
              ['4 ♠', '5 ♠', '6 ♠', '7 ♠', 'Q ♠', 'J ♠', 'K ♠', 'A ♠', '2 ♠', '3 ♠'], 
              ['4 ♣', '5 ♣', '6 ♣', '7 ♣', 'Q ♣', 'J ♣', 'K ♣', 'A ♣', '2 ♣', '3 ♣']]

deck_clean = [['Q ♥', 'J ♥', 'K ♥', 'A ♥', '2 ♥', '3 ♥'],
              ['Q ♦', 'J ♦', 'K ♦', 'A ♦', '2 ♦', '3 ♦'], 
              ['Q ♠', 'J ♠', 'K ♠', 'A ♠', '2 ♠', '3 ♠'], 
              ['Q ♣', 'J ♣', 'K ♣', 'A ♣', '2 ♣', '3 ♣']]


print('\n♥ ♦ Bem-Vindo ao Truco! ♠ ♣')
while True:

    print('\n========== Menu Inicial ==========')
    print('1 - Jogar Truco')
    print('2 - Regras do Truco')
    print('3 - Sair')

    truco_option = input('Escolha uma opção: ').strip()
    match truco_option:
        case '1':
            play_truco()
        case '2':
            rules_truco()
        case '3':
            print('Saindo do jogo. Até a próxima!')
        case _:
            print('Opção inválida! Por favor, escolha uma opção válida.')

        

    # ♥  ♦  ♠  ♣