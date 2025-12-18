import random
import time

def play_truco():
    print('\nIniciando uma nova partida de Truco!')
    print('Qual o tipo de baralho você quer usar?')
    print('1 - Baralho Limpo')
    print('2 - Baralho Sujo')
    truco_option = input('Escolha uma opção (1 ou 2): ').strip()
    match truco_option:
        case '1':
            print('\nVocê escolheu o Baralho Limpo!')
            start_game(number_player=2, deck=deck_clean)
        case '2':
            print('\nVocê escolheu o Baralho Sujo!')
            
            start_game(number_player=2, deck=deck_dirty)
        case _:
            print('\nOpção inválida! Usando baralho sujo por padrão.')
            start_game(number_player=2, deck=deck_dirty)
    
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

def shuffle_deck(deck, number_player):
    wich_deck = 'Sujo' if deck == deck_dirty else 'Limpo'
    print(f'\nEmbaralhando o Baralho {wich_deck}...\n')
    list_card_players = []
    vira = ''
    manilha = ''
    for i in range(3 * number_player + 1):
        random_index_deck = random.randint(0,3)
        choice_card = random.choice(deck[random_index_deck])
        while choice_card in list_card_players:
            random_index_deck = random.randint(0,3)
            choice_card_again = random.choice(deck[random_index_deck])

            if choice_card_again != choice_card and choice_card_again not in list_card_players:
                list_card_players.append(choice_card_again)
                break
        else:
            list_card_players.append(choice_card)
            
        # print (list_card_players)
    vira = list_card_players[-1]    
    print(f'O Vira é {vira}')
    order_strength = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3'] if deck == deck_dirty else ['Q', 'J', 'K', 'A', '2', '3']
    index_vira = order_strength.index(vira[0])
    if index_vira == len(order_strength) - 1:
        manilha = order_strength[0]
    else:
        manilha = order_strength[index_vira + 1]
    manilha_list = [f'{manilha} ♣', f'{manilha} ♥', f'{manilha} ♠', f'{manilha} ♦']
    print(f'As Manilhas são: {manilha_list}')
    return list_card_players, manilha_list

def screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, what_round, player1_discard, player2_discard, rounds):
    if what_round == '1' and player1_discard == False and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                               ┌─────┐ ┌─────┐ ┌─────┐                               │')
        print(f'│                               │ ┌─┐ │ │ ┌─┐ │ │ ┌─┐ │                               │')
        print(f'│                               │ │ │ │ │ │ │ │ │ │ │ │                               │')
        print(f'│                               │ └─┘ │ │ └─┘ │ │ └─┘ │                               │')
        print(f'│                               └─────┘ └─────┘ └─────┘                               │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │           ┌─────┐ ┌─────┐ ┌─────┐        │       Rodadas       ││')
        print(f'│ │  ─────────────  │           │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │ │{player1_cards[2][2]}    │        │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │           │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │ │  {player1_cards[2][0]}  │        │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │           │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│        │ ☆  ☆  ☆  │ ☆  ☆  ☆  ││')
        print(f'│ └─────────────────┘           └─────┘ └─────┘ └─────┘        └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '1' and player1_discard == True and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                               ┌─────┐ ┌─────┐ ┌─────┐                               │')
        print(f'│                               │ ┌─┐ │ │ ┌─┐ │ │ ┌─┐ │                               │')
        print(f'│                               │ │ │ │ │ │ │ │ │ │ │ │                               │')
        print(f'│                               │ └─┘ │ │ └─┘ │ │ └─┘ │                               │')
        print(f'│                               └─────┘ └─────┘ └─────┘                               │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │               ┌─────┐ ┌─────┐            │       Rodadas       ││')
        print(f'│ │  ─────────────  │               │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │            │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │               │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │            │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │               │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│            │ ☆  ☆  ☆  │ ☆  ☆  ☆  ││')
        print(f'│ └─────────────────┘               └─────┘ └─────┘            └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '1' and player1_discard == True and player2_discard == True:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                   ┌─────┐ ┌─────┐                                   │')
        print(f'│                                   │ ┌─┐ │ │ ┌─┐ │                                   │')
        print(f'│                                   │ │ │ │ │ │ │ │                                   │')
        print(f'│                                   │ └─┘ │ │ └─┘ │                                   │')
        print(f'│                                   └─────┘ └─────┘                                   │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{enemy_played_card[2]}    │                                       │')
        print(f'│                                       │  {enemy_played_card[0]}  │                                       │')
        print(f'│                                       │    {enemy_played_card[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │               ┌─────┐ ┌─────┐            │       Rodadas       ││')
        print(f'│ │  ─────────────  │               │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │            │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │               │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │            │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │               │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│            │ ☆  ☆  ☆  │ ☆  ☆  ☆  ││')
        print(f'│ └─────────────────┘               └─────┘ └─────┘            └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '2' and player1_discard == False and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                   ┌─────┐ ┌─────┐                                   │')
        print(f'│                                   │ ┌─┐ │ │ ┌─┐ │                                   │')
        print(f'│                                   │ │ │ │ │ │ │ │                                   │')
        print(f'│                                   │ └─┘ │ │ └─┘ │                                   │')
        print(f'│                                   └─────┘ └─────┘                                   │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │               ┌─────┐ ┌─────┐            │       Rodadas       ││')
        print(f'│ │  ─────────────  │               │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │            │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │               │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │            │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │               │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│            │ {rounds[0][0]}  ☆  ☆  │ {rounds[1][0]}  ☆  ☆  ││')
        print(f'│ └─────────────────┘               └─────┘ └─────┘            └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '2' and player1_discard == True and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                   ┌─────┐ ┌─────┐                                   │')
        print(f'│                                   │ ┌─┐ │ │ ┌─┐ │                                   │')
        print(f'│                                   │ │ │ │ │ │ │ │                                   │')
        print(f'│                                   │ └─┘ │ │ └─┘ │                                   │')
        print(f'│                                   └─────┘ └─────┘                                   │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                   ┌─────┐                │       Rodadas       ││')
        print(f'│ │  ─────────────  │                   │{player1_cards[0][2]}    │                │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                   │  {player1_cards[0][0]}  │                │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                   │    {player1_cards[0][2]}│                │ {rounds[0][0]}  ☆  ☆  │ {rounds[1][0]}  ☆  ☆  ││')
        print(f'│ └─────────────────┘                   └─────┘                └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')

    elif what_round == '2' and player1_discard == False and player2_discard == True:       
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │ ┌─┐ │                                       │')
        print(f'│                                       │ │ │ │                                       │')
        print(f'│                                       │ └─┘ │                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{enemy_played_card[2]}    │                                       │')
        print(f'│                                       │  {enemy_played_card[0]}  │                                       │')
        print(f'│                                       │    {enemy_played_card[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │               ┌─────┐ ┌─────┐            │       Rodadas       ││')
        print(f'│ │  ─────────────  │               │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │            │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │               │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │            │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │               │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│            │ {rounds[0][0]}  ☆  ☆  │ {rounds[1][0]}  ☆  ☆  ││')
        print(f'│ └─────────────────┘               └─────┘ └─────┘            └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '2' and player1_discard == True and player2_discard == True:  
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │ ┌─┐ │                                       │')
        print(f'│                                       │ │ │ │                                       │')
        print(f'│                                       │ └─┘ │                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{enemy_played_card[2]}    │                                       │')
        print(f'│                                       │  {enemy_played_card[0]}  │                                       │')
        print(f'│                                       │    {enemy_played_card[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                   ┌─────┐                │       Rodadas       ││')
        print(f'│ │  ─────────────  │                   │{player1_cards[0][2]}    │                │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                   │  {player1_cards[0][0]}  │                │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                   │    {player1_cards[0][2]}│                │ {rounds[0][0]}  ☆  ☆  │ {rounds[1][0]}  ☆  ☆  ││')
        print(f'│ └─────────────────┘                   └─────┘                └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '3' and player1_discard == False and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │ ┌─┐ │                                       │')
        print(f'│                                       │ │ │ │                                       │')
        print(f'│                                       │ └─┘ │                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                   ┌─────┐                │       Rodadas       ││')
        print(f'│ │  ─────────────  │                   │{player1_cards[0][2]}    │                │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                   │  {player1_cards[0][0]}  │                │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                   │    {player1_cards[0][2]}│                │ {rounds[0][0]}  {rounds[0][1]}  ☆  │ {rounds[1][0]}  {rounds[1][1]}  ☆  ││')
        print(f'│ └─────────────────┘                   └─────┘                └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')


    if what_round == '3' and player1_discard == True and player2_discard == False:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │ ┌─┐ │                                       │')
        print(f'│                                       │ │ │ │                                       │')
        print(f'│                                       │ └─┘ │                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                                          │       Rodadas       ││')
        print(f'│ │  ─────────────  │                                          │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                                          │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                                          │ {rounds[0][0]}  {rounds[0][1]}  ☆  │ {rounds[1][0]}  {rounds[1][1]}  ☆  ││')
        print(f'│ └─────────────────┘                                          └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')

    elif what_round == '3' and player1_discard == False and player2_discard == True:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{enemy_played_card[2]}    │                                       │')
        print(f'│                                       │  {enemy_played_card[0]}  │                                       │')
        print(f'│                                       │    {enemy_played_card[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                   ┌─────┐                │       Rodadas       ││')
        print(f'│ │  ─────────────  │                   │{player1_cards[0][2]}    │                │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                   │  {player1_cards[0][0]}  │                │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                   │    {player1_cards[0][2]}│                │ {rounds[0][0]}  {rounds[0][1]}  ☆  │ {rounds[1][0]}  {rounds[1][1]}  ☆  ││')
        print(f'│ └─────────────────┘                   └─────┘                └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')

    
    if what_round == '3' and player1_discard == True and player2_discard == True:
        print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{enemy_played_card[2]}    │                                       │')
        print(f'│                                       │  {enemy_played_card[0]}  │                                       │')
        print(f'│                                       │    {enemy_played_card[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{vira[2]}    │                                       │')
        print(f'│                                       │  {vira[0]}  │                                       │')
        print(f'│                                       │    {vira[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│                                                                                     │')
        print(f'│                                       ┌─────┐                                       │')
        print(f'│                                       │{card_in_table[2]}    │                                       │')
        print(f'│                                       │  {card_in_table[0]}  │                                       │')
        print(f'│                                       │    {card_in_table[2]}│                                       │')
        print(f'│                                       └─────┘                                       │')
        print(f'│                                                                                     │')
        print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
        print(f'│ │     Placar      │                                          │       Rodadas       ││')
        print(f'│ │  ─────────────  │                                          │  ─────────────────  ││')
        print(f'│ │  Você  │  Ele   │                                          │   Você   │    Ele   ││')
        print(f'│ │   {points_player1}   │   {points_player2}   │                                          │ {rounds[0][0]}  {rounds[0][1]}  ☆  │ {rounds[1][0]}  {rounds[1][1]}  ☆  ││')
        print(f'│ └─────────────────┘                                          └─────────────────────┘│')
        print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')

def p1_truco(p2_cards, man_list, r_value, isr_over, c_p_p2, p_p2, s_man, c_p_p1, p_p1, p1_tc, rounds):                                       
    print('\nVocê pediu Truco! Esperando o Adversário responder.')
    p1_tc = True
    time.sleep(1)
    strong_cards = 0   
    for card in p2_cards:
        if card in man_list or card[0] == '3' or card[0] == '2':
            strong_cards += 1
    if strong_cards >= 2 or strong_cards == 1 and '★' in rounds[1]:
        r_value = 3
        print('O Adversário pediu 6! Você aceita ?')
        print('1 - Aceitar')
        print('2 - Correr')
        print('3 - Pedir 9')
        truco_choice = input('Escolha uma das opções acima: ')
        while True:
            match truco_choice:
                case '1':
                    print('Você aceitou! A rodada está valendo 6 pontos.')
                    r_value = 6
                    break
                case '2':
                    print('Você correu! O Adversário ganhou a rodada.')
                    c_p_p2 += r_value
                    isr_over = True
                    p_p2 = f'0{c_p_p2}' if c_p_p2 < 10 else str(c_p_p2)
                    break
                case '3':
                    print('Você pediu 9! Esperando o Adversário responder.')
                    time.sleep(1)
                    ai_has_strong_manilha_card = False
                    ai_has_weak_manilha_card = False
                    for card in p2_cards:
                        if card in man_list and card[2] in s_man[2:4]:
                            ai_has_strong_manilha_card = True
                        elif card in man_list and card[2] in s_man[0:2]:
                            ai_has_weak_manilha_card = True
                    if ai_has_strong_manilha_card:
                        while True:
                            r_value = 9
                            print('O Adversário pediu 12! Você aceita ?')
                            print('1 - Aceitar')
                            print('2 - Correr')
                            truco_choice = input('Escolha uma das opções acima: ')
                            match truco_choice:
                                case '1': 
                                    print('Você aceitou! A rodada está valendo 12 pontos')
                                    r_value = 12
                                    break
                                case '2':
                                    print('Você correu! O Adversário ganhou a rodada.')
                                    c_p_p2 += r_value
                                    isr_over = True
                                    p_p2 = f'0{c_p_p2}' if c_p_p2 < 10 else str(c_p_p2)
                                    break
                                case _:
                                    print('Opção inválida! Tente novamente')
                    elif ai_has_weak_manilha_card:
                        print('O Adversário aceitou! A rodada está valendo 9.')
                        r_value = 9
                        break
                    else:
                        r_value = 9
                        print('Você ganhou a rodada! O Adversário correu.')
                        c_p_p1 += r_value
                        isr_over = True
                        p_p1 = f'0{c_p_p1}' if c_p_p1 < 10 else str(c_p_p1)
                        break
                    break
                case _:
                    print('Opção inválida! Tente novame')
    elif strong_cards == 1 or '★' in rounds[1]:
        print('O Adversário aceitou o Truco! ')
        r_value = 3
    else:
        print('O Adversário recusou o Truco! Você ganha a rodada.')
        c_p_p1 += r_value
        isr_over = True
        p_p1 = f'0{c_p_p1}' if c_p_p1 < 10 else str(c_p_p1)
    return r_value, isr_over, p1_tc, p_p1, p_p2 

def p2_truco(p2_cards, man_list, r_value, isr_over, c_p_p1, p_p1, c_p_p2, p_p2, s_man, p2_tc, rounds):
    strong_cards = 0   
    for card in p2_cards:
        if card in man_list or card[0] == '3' or card[0] == '2':
            strong_cards += 1
            
    should_ask = False
    if strong_cards >= 2:
        should_ask = True
    elif strong_cards == 1 and '★' in rounds[1]: 
        should_ask = True
        
    if should_ask:
        next_val = 3
        if r_value == 3: next_val = 6
        elif r_value == 6: next_val = 9
        elif r_value == 9: next_val = 12
        
        print(f'\nO Adversário pediu Truco! Você aceita?')
        p2_tc = True
        time.sleep(1)
        
        print('1 - Aceitar')
        print('2 - Correr')
        if next_val < 12:
            print(f'3 - Pedir {next_val + 3}')
            
        truco_choice = input('Escolha uma das opções acima: ').strip()
        
        while True:
            match truco_choice:
                case '1':
                    print(f'Você aceitou! A rodada está valendo {next_val} pontos.')
                    r_value = next_val
                    break
                case '2':
                    print('Você correu! O Adversário ganhou a rodada.')
                    c_p_p2 += r_value
                    isr_over = True
                    p_p2 = f'0{c_p_p2}' if c_p_p2 < 10 else str(c_p_p2)
                    break
                case '3':
                    if next_val >= 12:
                        print('Opção inválida! O jogo já vale 12.')
                        truco_choice = input('Tente novamente: ')
                        continue

                    raised_val = next_val + 3
                    print(f'Você pediu {raised_val}! Esperando o Adversário responder...')
                    time.sleep(1)
                    
                    ai_accepts = False
                    has_top_manilha = False
                    for card in p2_cards:
                        if card in man_list and card[2] in s_man[2:4]:
                            has_top_manilha = True
                    
                    if has_top_manilha or strong_cards >= 2:
                        print(f'O Adversário aceitou! A rodada está valendo {raised_val}.')
                        r_value = raised_val
                    else:
                        print('Você ganhou a rodada! O Adversário correu.')
                        c_p_p1 += next_val
                        isr_over = True
                        p_p1 = f'0{c_p_p1}' if c_p_p1 < 10 else str(c_p_p1)
                    break
                case _:
                    print('Opção inválida! Tente novamente')
                    truco_choice = input('Escolha: ')

    return r_value, isr_over, p2_tc, c_p_p1, p_p1, c_p_p2, p_p2

def start_game(number_player,  deck):
    print('\nIniciando o jogo de Truco...')
    print(f'Número de jogadores: {number_player}')
    time.sleep(2)

    match number_player:
        case 2:
            order_strength = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3']
            suits_manilha = ['♦', '♠', '♥', '♣']

            count_points_player1 = 0
            count_points_player2 = 0
            points_player1 = '00'
            points_player2 = '00'
            while count_points_player1 < 12 and count_points_player2 < 12:
                list_card_players, manilha_list = shuffle_deck(deck, number_player=2)
                print(f'Cartas dos jogadores: {list_card_players}')
                print(f'Manilhas: {manilha_list}')
                time.sleep(2)
                vira = list_card_players[-1]
                number_vira = vira[0]
                suit_vira = vira[2]
                manilhas = manilha_list
                rounds = [[],
                        []]
                player1_cards = list_card_players[0:3]
                player2_cards = list_card_players[3:6]
                count_round_player1 = 0
                count_round_player2 = 0
                round_value = 1
                isround_over = False
                round_win = '★'
                round_loose = '☆'
                player1_has_manilha = False
                player2_has_manilha = False
                player1_truco = False
                player2_truco = False
                #Rodada 1
                print(f'Jogador 1 cartas: {player1_cards}')
                print(f'Jogador 2 cartas: {player2_cards}')
                screen(vira, player1_cards, points_player1, points_player2, '', '', '1', False, False, rounds)

                while True:
                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                    print(f'1 - {player1_cards[0]}')
                    print(f'2 - {player1_cards[1]}')
                    print(f'3 - {player1_cards[2]}')
                    print(f'4 - Pedir Truco')
                    card_option = input('Escolha uma das opções acima: ').strip()
                    card_in_table = ''
                    match card_option:
                        case '1':
                            played_card = player1_cards[0]
                            print(f'Você jogou a carta: {played_card}')
                            card_in_table = played_card
                            player1_cards.remove(played_card)
                            break
                        case '2':
                            played_card = player1_cards[1]
                            print(f'Você jogou a carta: {played_card}')
                            card_in_table = played_card
                            player1_cards.remove(played_card)
                            break
                        case '3':
                            played_card = player1_cards[2]
                            print(f'Você jogou a carta: {played_card}')
                            card_in_table = played_card
                            player1_cards.remove(played_card)
                            break
                        case '4':
                            if player1_truco or player2_truco:
                                print('\nO Jogo já está Trucado!')
                                continue

                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                            if isround_over:
                                break 
                        case _:
                            print('Opção inválida! Tente novamente')

                if isround_over == True:
                    time.sleep(2)
                    continue
                else:
                    if player1_truco or player2_truco:
                        print('\nO Jogo já está Trucado!')

                    round_value, isround_over, player2_truco, count_points_player1, points_player1, count_points_player2, points_player2 = p2_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player1, points_player1, count_points_player2, points_player2, suits_manilha, player2_truco, rounds)

                    if isround_over == True:
                        time.sleep(2)
                        continue

                    print('Vez do seu adersário de Jogar...')
                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '1', True, False, rounds)
                    
                    time.sleep(2)        

                    enemy_played_card = random.choice(player2_cards)
                    player2_cards.remove(enemy_played_card)
                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '1', True, True, rounds)     
                    
                    print('\n')
                    time.sleep(2)
                    index_card_player1 = 0
                    index_card_player2 = 0
                    

                    player1_has_manilha = False
                    player2_has_manilha = False

                    for i in order_strength:
                        if card_in_table[0] == i:
                            index_card_player1 = order_strength.index(i)
                        elif enemy_played_card[0] == i:
                            index_card_player2 = order_strength.index(i)
                    
                    if card_in_table in manilhas:
                        player1_has_manilha = True
                    if enemy_played_card in manilhas:
                        player2_has_manilha = True




                    #Rodada 1 - Player 1 vence

                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                        print('Você venceu essa Rodada!')
                        rounds[0].append(round_win)
                        rounds[1].append(round_loose)
                        time.sleep(2)
                        screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)

                        while True:
                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                            print(f'1 - {player1_cards[0]}')
                            print(f'2 - {player1_cards[1]}')
                            print(f'4 - Pedir Truco')
                            card_option = input('Escolha uma das opções acima: ').strip()
                            card_in_table = ''
                            match card_option:
                                case '1':
                                    played_card = player1_cards[0]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '2':
                                    played_card = player1_cards[1]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '4':
                                    if player1_truco or player2_truco:
                                        print('\nO Jogo já está Trucado!')
                                        continue

                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                    if isround_over:
                                        break 
                                case _:
                                    print('Opção inválida! Tente novamente')

                        if isround_over == True:
                                          
                            time.sleep(2)
                            continue
                        else:
                            print('Vez do seu adersário de Jogar...')
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '2', True, False, rounds)        
                            
                            time.sleep(2)        
                            enemy_played_card = random.choice(player2_cards)
                            player2_cards.remove(enemy_played_card)
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)    
                            
                            print('\n')
                            time.sleep(2)
                            index_card_player1 = 0
                            index_card_player2 = 0

                            player1_has_manilha = False
                            player2_has_manilha = False


                            for i in order_strength:
                                if card_in_table[0] == i:
                                    index_card_player1 = order_strength.index(i)
                                elif enemy_played_card[0] == i:
                                    index_card_player2 = order_strength.index(i)

                            if card_in_table in manilhas:
                                player1_has_manilha = True
                            if enemy_played_card in manilhas:
                                player2_has_manilha = True

                            #Rodada 2 - Player1 vence rodada 1 e 2

                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                print('Você venceu a Rodada')
                                print('Você ganhou!!')
                                time.sleep(2)
                                count_points_player1 += round_value
                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              
                                continue

                            #Rodada 2 - Player1 vence rodada 1 e 2 com manilha

                            elif player1_has_manilha == True and player2_has_manilha == False:
                                print('Você venceu essa Rodada!')
                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                print('Você ganhou!!')
                                time.sleep(2)
                                count_points_player1 += round_value
                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              

                                continue

                            #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                            elif player2_has_manilha == True and player1_has_manilha == False:
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                print('Seu adversário venceu essa Rodada!')
                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                count_round_player2 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)  

                                time.sleep(2)
                                enemy_played_card = random.choice(player2_cards)
                                player2_cards.remove(enemy_played_card)
                                screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)

                                
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0

                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  

                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  

                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                        time.sleep(2)
                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                          
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                        time.sleep(2)
                                        continue
                            

                            elif player1_has_manilha == True and player2_has_manilha == True:
                                for i in suits_manilha:
                                    if card_in_table[2] == i:
                                        index_card_player1 = suits_manilha.index(i)
                                    elif enemy_played_card[2] == i:
                                        index_card_player2 = suits_manilha.index(i)

                                #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                if index_card_player1 > index_card_player2:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    print('Você ganhou!!')
                                    time.sleep(2)
                                    count_points_player1 += round_value
                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              

                                    continue
                                #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                else:
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                    count_round_player2 += 1
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)

                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                    time.sleep(2)
                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)

                                    screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)

                                    
                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break                                            
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      

                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)
                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0

                                        player1_has_manilha = False
                                        player2_has_manilha = False


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True

                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      

                                            continue

                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                   
                                            continue



                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                       
                                            continue



                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)


                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                         
                                                continue
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                            
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                    
                                            continue

                            #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                            else:
                                print('Seu adversário venceu essa Rodada!')          
                                count_round_player2 += 1
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)     
                                

                                time.sleep(2)
                                enemy_played_card = random.choice(player2_cards)
                                player2_cards.remove(enemy_played_card)

                                screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)     



                                
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0

                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True

                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
             
                                        continue

                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                      
                                        continue



                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue



                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)


                                        
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                       
                                            continue
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                     
                                            continue
                                        
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue

                    #Rodada 1 - Player 1 vence manilha
                    elif player1_has_manilha == True and player2_has_manilha == False:
                        print('Você venceu essa Rodada!')
                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                        rounds[0].append(round_win)
                        rounds[1].append(round_loose)
                        count_round_player1 += 1
                        time.sleep(2)
                        screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)      

                        while True:
                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                            print(f'1 - {player1_cards[0]}')
                            print(f'2 - {player1_cards[1]}')
                            print(f'4 - Pedir Truco')
                            card_option = input('Escolha uma das opções acima: ').strip()
                            card_in_table = ''
                            match card_option:
                                case '1':
                                    played_card = player1_cards[0]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '2':
                                    played_card = player1_cards[1]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '4':
                                    if player1_truco or player2_truco:
                                        print('\nO Jogo já está Trucado!')
                                        continue  
                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                    if isround_over:
                                        break 
                                case _:
                                    print('Opção inválida! Tente novamente')
                        if isround_over == True:
                                      
                            time.sleep(2)
                            continue
                        else:
                            print('Vez do seu adersário de Jogar...')
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '2', True, False, rounds)               
                            
                            time.sleep(2)        
                            enemy_played_card = random.choice(player2_cards)
                            player2_cards.remove(enemy_played_card)
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)         
                            
                            print('\n')
                            time.sleep(2)


                            



                            index_card_player1 = 0
                            index_card_player2 = 0
                            player1_has_manilha = False
                            player2_has_manilha = False


                            for i in order_strength:
                                if card_in_table[0] == i:
                                    index_card_player1 = order_strength.index(i)
                                elif enemy_played_card[0] == i:
                                    index_card_player2 = order_strength.index(i)

                            if card_in_table in manilhas:
                                player1_has_manilha = True
                            if enemy_played_card in manilhas:
                                player2_has_manilha = True

                            #Rodada 2 - Player1 vence rodada 1 e 2

                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                print('Você venceu a Rodada')
                                print('Você ganhou!!')
                                time.sleep(2)
                                count_points_player1 += round_value
                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                              
                                continue

                            #Rodada 2 - Player1 vence rodada 1 e 2 com manilha

                            elif player1_has_manilha == True and player2_has_manilha == False:
                                print('Você venceu essa Rodada!')
                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                print('Você ganhou!!')
                                time.sleep(2)
                                count_points_player1 += round_value
                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                      
                                continue

                            #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                            elif player2_has_manilha == True and player1_has_manilha == False:
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                print('Seu adversário venceu essa Rodada!')
                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                count_round_player2 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)  

                                time.sleep(2)
                                enemy_played_card = random.choice(player2_cards)
                                player2_cards.remove(enemy_played_card)
                                screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)

                                
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                 
                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                    
                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  

                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                          
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                   
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue
                            

                            elif player1_has_manilha == True and player2_has_manilha == True:
                                for i in suits_manilha:
                                    if card_in_table[2] == i:
                                        index_card_player1 = suits_manilha.index(i)
                                    elif enemy_played_card[2] == i:
                                        index_card_player2 = suits_manilha.index(i)

                                #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                if index_card_player1 > index_card_player2:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    print('Você ganhou!!')
                                    time.sleep(2)
                                    count_points_player1 += round_value
                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              
                              
                                    continue
                                #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                else:
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                    count_round_player2 += 1
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)

                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                    time.sleep(2)
                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)

                                    screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)



                                    
                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      

                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)
                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False
                                        


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True

                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                      
                                            continue

                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                         
                                            continue



                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue



                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)


                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                             
                                                continue
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                          
                                                continue
                                            
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue

                            #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                            else:
                                print('Seu adversário venceu essa Rodada!')          
                                count_round_player2 += 1
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)     
                                

                                time.sleep(2)
                                enemy_played_card = random.choice(player2_cards)
                                player2_cards.remove(enemy_played_card)

                                screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)     



                                
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True

                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                         
                                        continue

                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                           
                                        continue



                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue



                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)


                                        
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                        
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue





































                    #Rodada 1 - Player 2 vence manilha
                    elif player2_has_manilha == True and player1_has_manilha == False:
                        print('Seu adversário venceu essa Rodada!')
                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                        count_round_player2 += 1
                        rounds[0].append(round_loose)
                        rounds[1].append(round_win)
                        time.sleep(2)
                        screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)  

                        time.sleep(2)
                        enemy_played_card = random.choice(player2_cards)
                        player2_cards.remove(enemy_played_card)
                        screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '2', False, True, rounds)

                                
                        while True:
                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                            print(f'1 - {player1_cards[0]}')
                            print(f'2 - {player1_cards[1]}')
                            print(f'4 - Pedir Truco')
                            card_option = input('Escolha uma das opções acima: ').strip()
                            card_in_table = ''
                            match card_option:
                                case '1':
                                    played_card = player1_cards[0]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '2':
                                    played_card = player1_cards[1]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '4':
                                        
                                    if player1_truco or player2_truco:
                                        print('\nO Jogo já está Trucado!')
                                        continue
                                        
                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)
                                        
                                    if isround_over:
                                        break 
                                case _:
                                    print('Opção inválida! Tente novamente')
                        if isround_over == True:
                                      
                            time.sleep(2)
                            continue
                        else:      
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)
                            print('\n')
                            time.sleep(2)

                            index_card_player1 = 0
                            index_card_player2 = 0
                            player1_has_manilha = False
                            player2_has_manilha = False


                            for i in order_strength:
                                if card_in_table[0] == i:
                                    index_card_player1 = order_strength.index(i)
                                elif enemy_played_card[0] == i:
                                    index_card_player2 = order_strength.index(i)

                            if card_in_table in manilhas:
                                player1_has_manilha = True
                            if enemy_played_card in manilhas:
                                player2_has_manilha = True

                            #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2

                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                print('Você venceu a Rodada')
                                rounds[0].append(round_win)
                                rounds[1].append(round_loose)
                                count_round_player1 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                    time.sleep(2)

                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    

                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                

                            #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2 com manilha

                            elif player1_has_manilha == True and player2_has_manilha == False:
                                print('Você venceu essa Rodada!')
                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                rounds[0].append(round_win)
                                rounds[1].append(round_loose)
                                count_round_player1 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                    time.sleep(2)

                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    

                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue

                            #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                            elif player2_has_manilha == True and player1_has_manilha == False:
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                print('Seu adversário venceu essa Rodada!')
                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                print('Você Perdeu!!')
                                count_points_player2 += round_value
                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                          
                                continue
                            

                            elif player1_has_manilha == True and player2_has_manilha == True:
                                for i in suits_manilha:
                                    if card_in_table[2] == i:
                                        index_card_player1 = suits_manilha.index(i)
                                    elif enemy_played_card[2] == i:
                                        index_card_player2 = suits_manilha.index(i)

                                #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                if index_card_player1 > index_card_player2:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '', False, False, rounds)

                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                        time.sleep(2)

                                        enemy_played_card = random.choice(player2_cards)
                                        player2_cards.remove(enemy_played_card)
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        

                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False



                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                            
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)

                                            continue


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)

                                            continue


                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)

                                        

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
   
                                            continue

                                #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                else:
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)
                                    print('Você Perdeu!!')
                                    count_points_player2 += round_value
                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                              
     
                                    continue

                            #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                            else:
                                print('Seu adversário venceu essa Rodada!')          
                                print('Você perdeu!!')
                                time.sleep(2)
                                count_points_player2 += round_value
                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                continue
























                    elif player1_has_manilha == True and player2_has_manilha == True:
                        for i in suits_manilha:
                            if card_in_table[2] == i:
                                index_card_player1 = suits_manilha.index(i)
                            elif enemy_played_card[2] == i:
                                index_card_player2 = suits_manilha.index(i)


                        #Rodada 1 - Player 1 vence manilha contra manilha
                        if index_card_player1 > index_card_player2:
                            print('Você venceu essa Rodada!')
                            print(f'A sua manilha {card_in_table} é mais forte que a do adversário {enemy_played_card}')
                            count_round_player1 += 1
                            rounds[0].append(round_win)
                            rounds[1].append(round_loose)
                            count_round_player1 += 1
                            time.sleep(2)
                            screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)      

                            while True:
                                print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                print(f'1 - {player1_cards[0]}')
                                print(f'2 - {player1_cards[1]}')
                                print(f'4 - Pedir Truco')
                                card_option = input('Escolha uma das opções acima: ').strip()
                                card_in_table = ''
                                match card_option:
                                    case '1':
                                        played_card = player1_cards[0]
                                        print(f'Você jogou a carta: {played_card}')
                                        card_in_table = played_card
                                        player1_cards.remove(played_card)
                                        break
                                    case '2':
                                        played_card = player1_cards[1]
                                        print(f'Você jogou a carta: {played_card}')
                                        card_in_table = played_card
                                        player1_cards.remove(played_card)
                                        break
                                    case '4':
                                        if player1_truco or player2_truco:
                                            print('\nO Jogo já está Trucado!')
                                            continue

                                        round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                        if isround_over:
                                            break 
                                    case _:
                                        print('Opção inválida! Tente novamente')
                            if isround_over == True:
                                          
                                time.sleep(2)
                                continue
                            else:
                                print('Vez do seu adersário de Jogar...')
                                screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '2', True, False, rounds)               
                                
                                time.sleep(2)        
                                enemy_played_card = random.choice(player2_cards)
                                player2_cards.remove(enemy_played_card)
                                screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)         
                                
                                print('\n')
                                time.sleep(2)


                                



                                index_card_player1 = 0
                                index_card_player2 = 0
                                player1_has_manilha = False
                                player2_has_manilha = False


                                for i in order_strength:
                                    if card_in_table[0] == i:
                                        index_card_player1 = order_strength.index(i)
                                    elif enemy_played_card[0] == i:
                                        index_card_player2 = order_strength.index(i)

                                if card_in_table in manilhas:
                                    player1_has_manilha = True
                                if enemy_played_card in manilhas:
                                    player2_has_manilha = True

                                #Rodada 2 - Player1 vence rodada 1 e 2

                                if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                    print('Você venceu a Rodada')
                                    print('Você ganhou!!')
                                    time.sleep(2)
                                    count_points_player1 += round_value
                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              
                                    continue

                                #Rodada 2 - Player1 vence rodada 1 e 2 com manilha

                                elif player1_has_manilha == True and player2_has_manilha == False:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    print('Você ganhou!!')
                                    time.sleep(2)
                                    count_points_player1 += round_value
                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                              
                                    continue

                                #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                                elif player2_has_manilha == True and player1_has_manilha == False:
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                    count_round_player2 += 1
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)  

                                    time.sleep(2)
                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)
                                    screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)

                                    
                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                            
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)

                                            continue


                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)

                                        

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      

                                            continue
                                

                                elif player1_has_manilha == True and player2_has_manilha == True:
                                    for i in suits_manilha:
                                        if card_in_table[2] == i:
                                            index_card_player1 = suits_manilha.index(i)
                                        elif enemy_played_card[2] == i:
                                            index_card_player2 = suits_manilha.index(i)

                                    #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                    if index_card_player1 > index_card_player2:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue
                                    #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                        count_round_player2 += 1
                                        rounds[0].append(round_loose)
                                        rounds[1].append(round_win)

                                        time.sleep(2)
                                        screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                        time.sleep(2)
                                        enemy_played_card = random.choice(player2_cards)
                                        player2_cards.remove(enemy_played_card)

                                        screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)



                                        
                                        while True:
                                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                            print(f'1 - {player1_cards[0]}')
                                            print(f'4 - Pedir Truco')
                                            card_option = input('Escolha uma das opções acima: ').strip()
                                            card_in_table = ''
                                            match card_option:
                                                case '1':
                                                    played_card = player1_cards[0]
                                                    print(f'Você jogou a carta: {played_card}')
                                                    card_in_table = played_card
                                                    player1_cards.remove(played_card)
                                                    break
                                                case '4':
                                                    if player1_truco or player2_truco:
                                                        print('\nO Jogo já está Trucado!')
                                                        continue

                                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                    if isround_over:
                                                        break 
                                                case _:
                                                    print('Opção inválida! Tente novamente')
                                        if isround_over == True:
                                                      
                                            time.sleep(2)
                                            continue
                                        else:      

                                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)
                                            
                                            print('\n')
                                            time.sleep(2)
                                            
                                            index_card_player1 = 0
                                            index_card_player2 = 0
                                            player1_has_manilha = False
                                            player2_has_manilha = False
                                            


                                            for i in order_strength:
                                                if card_in_table[0] == i:
                                                    index_card_player1 = order_strength.index(i)
                                                elif enemy_played_card[0] == i:
                                                    index_card_player2 = order_strength.index(i)

                                            if card_in_table in manilhas:
                                                player1_has_manilha = True
                                            if enemy_played_card in manilhas:
                                                player2_has_manilha = True

                                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                                print('Você venceu a Rodada')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            elif player1_has_manilha == True and player2_has_manilha == False:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue



                                            elif player2_has_manilha == True and player1_has_manilha == False:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                                print('Você perdeu!!')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          

                                                continue



                                            elif player1_has_manilha == True and player2_has_manilha == True:
                                                for i in suits_manilha:
                                                    if card_in_table[2] == i:
                                                        index_card_player1 = suits_manilha.index(i)
                                                    elif enemy_played_card[2] == i:
                                                        index_card_player2 = suits_manilha.index(i)


                                                if index_card_player1 > index_card_player2:
                                                    print('Você venceu essa Rodada!')
                                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                    print('Você ganhou!!')
                                                    time.sleep(2)
                                                    count_points_player1 += round_value
                                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                              
                                                    continue
                                                else:
                                                    print('Seu adversário venceu essa Rodada!')
                                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                    time.sleep(2)
                                                    count_points_player2 += round_value
                                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                              
                                                    continue
                                                
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print('Você perdeu!!')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          

                                                continue

                                #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                                else:
                                    print('Seu adversário venceu essa Rodada!')          
                                    count_round_player2 += 1
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)     
                                    

                                    time.sleep(2)
                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)

                                    screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '3', False, True, rounds)     



                                    
                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True

                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue

                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue



                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue



                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)


                                            
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                            
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue

                            
























                        #Rodada 1 - Player 2 vence manilha contra manilha
                        else:
                            print('Seu adversário venceu essa Rodada!')
                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                            count_round_player2 += 1
                            rounds[0].append(round_loose)
                            rounds[1].append(round_win)
                            time.sleep(2)
                            screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)  

                            time.sleep(2)
                            enemy_played_card = random.choice(player2_cards)
                            player2_cards.remove(enemy_played_card)
                            screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '2', False, True, rounds)

                                    
                            while True:
                                print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                print(f'1 - {player1_cards[0]}')
                                print(f'2 - {player1_cards[1]}')
                                print(f'4 - Pedir Truco')
                                card_option = input('Escolha uma das opções acima: ').strip()
                                card_in_table = ''
                                match card_option:
                                    case '1':
                                        played_card = player1_cards[0]
                                        print(f'Você jogou a carta: {played_card}')
                                        card_in_table = played_card
                                        player1_cards.remove(played_card)
                                        break
                                    case '2':
                                        played_card = player1_cards[1]
                                        print(f'Você jogou a carta: {played_card}')
                                        card_in_table = played_card
                                        player1_cards.remove(played_card)
                                        break
                                    case '4':
                                        if player1_truco or player2_truco:
                                            print('\nO Jogo já está Trucado!')
                                            continue

                                        round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                        if isround_over:
                                            break 
                                    case _:
                                        print('Opção inválida! Tente novamente')
                            if isround_over == True:
                                          
                                time.sleep(2)
                                continue
                            else:      
                                screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)
                                print('\n')
                                time.sleep(2)

                                index_card_player1 = 0
                                index_card_player2 = 0
                                player1_has_manilha = False
                                player2_has_manilha = False


                                for i in order_strength:
                                    if card_in_table[0] == i:
                                        index_card_player1 = order_strength.index(i)
                                    elif enemy_played_card[0] == i:
                                        index_card_player2 = order_strength.index(i)

                                if card_in_table in manilhas:
                                    player1_has_manilha = True
                                if enemy_played_card in manilhas:
                                    player2_has_manilha = True

                                #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2

                                if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                    print('Você venceu a Rodada')
                                    rounds[0].append(round_win)
                                    rounds[1].append(round_loose)
                                    count_round_player1 += 1
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)
                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                        time.sleep(2)

                                        enemy_played_card = random.choice(player2_cards)
                                        player2_cards.remove(enemy_played_card)
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        

                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                            
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue


                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)

                                        

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue


                                    

                                #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2 com manilha

                                elif player1_has_manilha == True and player2_has_manilha == False:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    rounds[0].append(round_win)
                                    rounds[1].append(round_loose)
                                    count_round_player1 += 1
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                            case _:
                                                print('Opção inválida! Tente novamente')
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                        time.sleep(2)

                                        enemy_played_card = random.choice(player2_cards)
                                        player2_cards.remove(enemy_played_card)
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        

                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False


                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                            
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue


                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)

                                        

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue

                                #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                                elif player2_has_manilha == True and player1_has_manilha == False:
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                    print('Você Perdeu!!')
                                    count_points_player2 += round_value
                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                              
                                    time.sleep(2)
                                    continue
                                

                                elif player1_has_manilha == True and player2_has_manilha == True:
                                    for i in suits_manilha:
                                        if card_in_table[2] == i:
                                            index_card_player1 = suits_manilha.index(i)
                                        elif enemy_played_card[2] == i:
                                            index_card_player2 = suits_manilha.index(i)

                                    #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                    if index_card_player1 > index_card_player2:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        time.sleep(2)
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '', False, False, rounds)

                                        while True:
                                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                            print(f'1 - {player1_cards[0]}')
                                            print(f'4 - Pedir Truco')
                                            card_option = input('Escolha uma das opções acima: ').strip()
                                            card_in_table = ''
                                            match card_option:
                                                case '1':
                                                    played_card = player1_cards[0]
                                                    print(f'Você jogou a carta: {played_card}')
                                                    card_in_table = played_card
                                                    player1_cards.remove(played_card)
                                                    break
                                                case '4':
                                                    if player1_truco or player2_truco:
                                                        print('\nO Jogo já está Trucado!')
                                                        continue

                                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                    if isround_over:
                                                        break 
                                                case _:
                                                    print('Opção inválida! Tente novamente')
                                        if isround_over == True:
                                                      
                                            time.sleep(2)
                                            continue
                                        else:      
                                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                            time.sleep(2)

                                            enemy_played_card = random.choice(player2_cards)
                                            player2_cards.remove(enemy_played_card)
                                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                            

                                            
                                            print('\n')
                                            time.sleep(2)
                                            
                                            index_card_player1 = 0
                                            index_card_player2 = 0
                                            player1_has_manilha = False
                                            player2_has_manilha = False



                                            for i in order_strength:
                                                if card_in_table[0] == i:
                                                    index_card_player1 = order_strength.index(i)
                                                elif enemy_played_card[0] == i:
                                                    index_card_player2 = order_strength.index(i)

                                            if card_in_table in manilhas:
                                                player1_has_manilha = True
                                            if enemy_played_card in manilhas:
                                                player2_has_manilha = True


                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                                print('Você venceu a Rodada')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue
                                                
                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                            elif player1_has_manilha == True and player2_has_manilha == False:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue


                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                            elif player2_has_manilha == True and player1_has_manilha == False:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                                print('Você perdeu!!')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue


                                            elif player1_has_manilha == True and player2_has_manilha == True:
                                                for i in suits_manilha:
                                                    if card_in_table[2] == i:
                                                        index_card_player1 = suits_manilha.index(i)
                                                    elif enemy_played_card[2] == i:
                                                        index_card_player2 = suits_manilha.index(i)

                                            

                                                #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                                if index_card_player1 > index_card_player2:
                                                    print('Você venceu essa Rodada!')
                                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                    print('Você ganhou!!')
                                                    time.sleep(2)
                                                    count_points_player1 += round_value
                                                    points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                              
                                                    continue

                                                #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                                else:
                                                    print('Seu adversário venceu essa Rodada!')
                                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                    time.sleep(2)
                                                    count_points_player2 += round_value
                                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                              
                                                    continue
                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print('Você perdeu!!')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue

                                    #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                        rounds[0].append(round_loose)
                                        rounds[1].append(round_win)
                                        print('Você Perdeu!!')
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue

                                #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                                else:
                                    print('Seu adversário venceu essa Rodada!')          
                                    print('Você perdeu!!')
                                    time.sleep(2)
                                    count_points_player2 += round_value
                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                              
                                    continue







































                    # Rodada 1 - Player 2 vence
                    # Rodada 2
                    else:
                        print('Seu adversário venceu essa Rodada!')
                        time.sleep(2)
                        count_round_player2 += 1
                        rounds[0].append(round_loose)
                        rounds[1].append(round_win)
                        time.sleep(2)
                        screen(vira, player1_cards, points_player1, points_player2, '', '', '2', False, False, rounds)  

                        time.sleep(2)
                        enemy_played_card = random.choice(player2_cards)
                        player2_cards.remove(enemy_played_card)
                        screen(vira, player1_cards, points_player1, points_player2, '', enemy_played_card, '2', False, True, rounds)

                                
                        while True:
                            print('\nSua vez de Jogar, qual carta você quer jogar? ')
                            print(f'1 - {player1_cards[0]}')
                            print(f'2 - {player1_cards[1]}')
                            print(f'4 - Pedir Truco')
                            card_option = input('Escolha uma das opções acima: ').strip()
                            card_in_table = ''
                            match card_option:
                                case '1':
                                    played_card = player1_cards[0]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '2':
                                    played_card = player1_cards[1]
                                    print(f'Você jogou a carta: {played_card}')
                                    card_in_table = played_card
                                    player1_cards.remove(played_card)
                                    break
                                case '4':
                                    if player1_truco or player2_truco:
                                        print('\nO Jogo já está Trucado!')
                                        continue

                                    round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                    if isround_over:
                                        break 
                                case _:
                                    print('Opção inválida! Tente novamente')
                        if isround_over == True:
                                      
                            time.sleep(2)
                            continue
                        else:      
                            screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '2', True, True, rounds)
                            print('\n')
                            time.sleep(2)

                            index_card_player1 = 0
                            index_card_player2 = 0
                            player1_has_manilha = False
                            player2_has_manilha = False


                            for i in order_strength:
                                if card_in_table[0] == i:
                                    index_card_player1 = order_strength.index(i)
                                elif enemy_played_card[0] == i:
                                    index_card_player2 = order_strength.index(i)

                            if card_in_table in manilhas:
                                player1_has_manilha = True
                            if enemy_played_card in manilhas:
                                player2_has_manilha = True

                            #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2

                            if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                print('Você venceu a Rodada')
                                rounds[0].append(round_win)
                                rounds[1].append(round_loose)
                                count_round_player1 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)
                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                    time.sleep(2)

                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    

                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                

                            #Rodada 2 - Player2 vence rodada 1 e player 1 vence rodada 2 com manilha

                            elif player1_has_manilha == True and player2_has_manilha == False:
                                print('Você venceu essa Rodada!')
                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                rounds[0].append(round_win)
                                rounds[1].append(round_loose)
                                count_round_player1 += 1
                                time.sleep(2)
                                screen(vira, player1_cards, points_player1, points_player2, '', '', '3', False, False, rounds)

                                while True:
                                    print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                    print(f'1 - {player1_cards[0]}')
                                    print(f'4 - Pedir Truco')
                                    card_option = input('Escolha uma das opções acima: ').strip()
                                    card_in_table = ''
                                    match card_option:
                                        case '1':
                                            played_card = player1_cards[0]
                                            print(f'Você jogou a carta: {played_card}')
                                            card_in_table = played_card
                                            player1_cards.remove(played_card)
                                            break
                                        case '4':
                                            if player1_truco or player2_truco:
                                                print('\nO Jogo já está Trucado!')
                                                continue

                                            round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                            if isround_over:
                                                break 
                                        case _:
                                            print('Opção inválida! Tente novamente')
                                if isround_over == True:
                                              
                                    time.sleep(2)
                                    continue
                                else:      
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                    time.sleep(2)

                                    enemy_played_card = random.choice(player2_cards)
                                    player2_cards.remove(enemy_played_card)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                    

                                    
                                    print('\n')
                                    time.sleep(2)
                                    
                                    index_card_player1 = 0
                                    index_card_player2 = 0
                                    player1_has_manilha = False
                                    player2_has_manilha = False


                                    for i in order_strength:
                                        if card_in_table[0] == i:
                                            index_card_player1 = order_strength.index(i)
                                        elif enemy_played_card[0] == i:
                                            index_card_player2 = order_strength.index(i)

                                    if card_in_table in manilhas:
                                        player1_has_manilha = True
                                    if enemy_played_card in manilhas:
                                        player2_has_manilha = True


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                    if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                        print('Você venceu a Rodada')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue
                                        
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                    elif player1_has_manilha == True and player2_has_manilha == False:
                                        print('Você venceu essa Rodada!')
                                        print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                        print('Você ganhou!!')
                                        time.sleep(2)
                                        count_points_player1 += round_value
                                        points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                  
                                        continue


                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                    elif player2_has_manilha == True and player1_has_manilha == False:
                                        print('Seu adversário venceu essa Rodada!')
                                        print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue


                                    elif player1_has_manilha == True and player2_has_manilha == True:
                                        for i in suits_manilha:
                                            if card_in_table[2] == i:
                                                index_card_player1 = suits_manilha.index(i)
                                            elif enemy_played_card[2] == i:
                                                index_card_player2 = suits_manilha.index(i)

                                    

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                        if index_card_player1 > index_card_player2:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue

                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue
                                    #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                    else:
                                        print('Seu adversário venceu essa Rodada!')
                                        print('Você perdeu!!')
                                        time.sleep(2)
                                        count_points_player2 += round_value
                                        points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                  
                                        continue

                            #Rodada 2 - Player1 vence rodada 1 e player 2 vence rodada 2 com manilha

                            elif player2_has_manilha == True and player1_has_manilha == False:
                                rounds[0].append(round_loose)
                                rounds[1].append(round_win)
                                print('Seu adversário venceu essa Rodada!')
                                print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                print('Você Perdeu!!')
                                count_points_player2 += round_value
                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                          
                                time.sleep(2)
                                continue
                            

                            elif player1_has_manilha == True and player2_has_manilha == True:
                                for i in suits_manilha:
                                    if card_in_table[2] == i:
                                        index_card_player1 = suits_manilha.index(i)
                                    elif enemy_played_card[2] == i:
                                        index_card_player2 = suits_manilha.index(i)

                                #Rodada 2 - Player1 vence rodada 1 e 2 com manilha mais forte que a do adversário
                                if index_card_player1 > index_card_player2:
                                    print('Você venceu essa Rodada!')
                                    print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                    time.sleep(2)
                                    screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '', False, False, rounds)

                                    while True:
                                        print('\nSua vez de Jogar, qual carta você quer jogar? ')
                                        print(f'1 - {player1_cards[0]}')
                                        print(f'4 - Pedir Truco')
                                        card_option = input('Escolha uma das opções acima: ').strip()
                                        card_in_table = ''
                                        match card_option:
                                            case '1':
                                                played_card = player1_cards[0]
                                                print(f'Você jogou a carta: {played_card}')
                                                card_in_table = played_card
                                                player1_cards.remove(played_card)
                                                break
                                            case '4':
                                                if player1_truco or player2_truco:
                                                    print('\nO Jogo já está Trucado!')
                                                    continue

                                                round_value, isround_over, player1_truco, points_player1, points_player2 = p1_truco(player2_cards, manilha_list, round_value, isround_over, count_points_player2, points_player2, suits_manilha, count_points_player1, points_player1, player1_truco, rounds)

                                                if isround_over:
                                                    break 
                                    if isround_over == True:
                                                  
                                        time.sleep(2)
                                        continue
                                    else:      
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, '', '3', True, False, rounds)     
                                        time.sleep(2)

                                        enemy_played_card = random.choice(player2_cards)
                                        player2_cards.remove(enemy_played_card)
                                        screen(vira, player1_cards, points_player1, points_player2, card_in_table, enemy_played_card, '3', True, True, rounds)     
                                        

                                        
                                        print('\n')
                                        time.sleep(2)
                                        
                                        index_card_player1 = 0
                                        index_card_player2 = 0
                                        player1_has_manilha = False
                                        player2_has_manilha = False



                                        for i in order_strength:
                                            if card_in_table[0] == i:
                                                index_card_player1 = order_strength.index(i)
                                            elif enemy_played_card[0] == i:
                                                index_card_player2 = order_strength.index(i)

                                        if card_in_table in manilhas:
                                            player1_has_manilha = True
                                        if enemy_played_card in manilhas:
                                            player2_has_manilha = True


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence
                                        if index_card_player1 > index_card_player2 and player1_has_manilha == False and player2_has_manilha == False:
                                            print('Você venceu a Rodada')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue
                                            
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manilha
                                        elif player1_has_manilha == True and player2_has_manilha == False:
                                            print('Você venceu essa Rodada!')
                                            print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                            print('Você ganhou!!')
                                            time.sleep(2)
                                            count_points_player1 += round_value
                                            points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                      
                                            continue


                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 e 3 com manilha
                                        elif player2_has_manilha == True and player1_has_manilha == False:
                                            print('Seu adversário venceu essa Rodada!')
                                            print(f'Você jogou {card_in_table} e seu adversário jogou a manilha {enemy_played_card}')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue


                                        elif player1_has_manilha == True and player2_has_manilha == True:
                                            for i in suits_manilha:
                                                if card_in_table[2] == i:
                                                    index_card_player1 = suits_manilha.index(i)
                                                elif enemy_played_card[2] == i:
                                                    index_card_player2 = suits_manilha.index(i)

                                        

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player1 vence com manila mais forte que o adversário
                                            if index_card_player1 > index_card_player2:
                                                print('Você venceu essa Rodada!')
                                                print(f'Você jogou a manilha {card_in_table} e seu adversário jogou a carta {enemy_played_card}')
                                                print('Você ganhou!!')
                                                time.sleep(2)
                                                count_points_player1 += round_value
                                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                                          
                                                continue

                                            #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence com manila mais forte que a sua
                                            else:
                                                print('Seu adversário venceu essa Rodada!')
                                                print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                                time.sleep(2)
                                                count_points_player2 += round_value
                                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                          
                                                continue
                                        #Rodada 3 - Player1 vence rodada 1, player 2 vence rodada 2 com manilha, player2 vence rodada 3
                                        else:
                                            print('Seu adversário venceu essa Rodada!')
                                            print('Você perdeu!!')
                                            time.sleep(2)
                                            count_points_player2 += round_value
                                            points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                                      
                                            continue

                                #Rodada 2 - Player1 vence rodada 1 e player2 vence rodada 2 com manilha mais forte que a sua
                                else:
                                    print('Seu adversário venceu essa Rodada!')
                                    print(f'A sua manilha {card_in_table} é mais fraco que a do adversário {enemy_played_card}')
                                    rounds[0].append(round_loose)
                                    rounds[1].append(round_win)
                                    print('Você Perdeu!!')
                                    count_points_player2 += round_value
                                    points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                              
                                    time.sleep(2)
                                    continue

                            #Rodada 3 - player1 vence rodada 1 e player2 vence rodada 2
                            else:
                                print('Seu adversário venceu essa Rodada!')          
                                print('Você perdeu!!')
                                time.sleep(2)
                                count_points_player2 += round_value
                                points_player2 = f'0{count_points_player2}' if count_points_player2 < 10 else str(count_points_player2)
                                          
                                continue
            
            if count_points_player1 >= 12:
                print('Você venceu a partida!')
                print(f'Você fez {count_points_player1} pontos e seus adversário fez {count_points_player2} pontos')
            elif count_points_player2 >= 12:
                print('Você perdeu a partida!')
                print(f'Você fez {count_points_player1} pontos e seus adversário fez {count_points_player2} pontos')


    


                    


        


































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
            break
        case _:
            print('Opção inválida! Por favor, escolha uma opção válida.')

        

    # ♥  ♦  ♠  ♣ 〇 ⬤