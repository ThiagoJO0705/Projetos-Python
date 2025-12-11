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
            number_player, list_card_players, manilha_list = choose_players(deck_clean, is_dirty=False)
        case '2':
            print('\nVocê escolheu o Baralho Sujo!')
            number_player, list_card_players, manilha_list  = choose_players(deck_dirty, is_dirty=True)
        case _:
            print('\nOpção inválida! Usando baralho sujo por padrão.')
            number_player, list_card_players, manilha_list = choose_players(deck_dirty, is_dirty=True)
    start_game(number_player, list_card_players, manilha_list)
    

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

def choose_players(deck, is_dirty):
    number_player = int(input('Selecione o número de jogadores (2 ou 4): '))
    if is_dirty == True:
        match number_player:
            case 2:
                print('Iniciando jogo para 2 jogadores...')
                list_card_players, manilha_list = shuffle_deck(deck, number_player, is_dirty=True)
            case 4:
                print('Iniciando jogo para 4 jogadores...')
                list_card_players, manilha_list = shuffle_deck(deck, number_player, is_dirty=True)
            case _:
                print('Número inválido de jogadores! Iniciando jogo para 2 jogadores por padrão...')
    else:
        match number_player:
            case 2:
                print('Iniciando jogo para 2 jogadores...')
                # shuffle_deck(deck, number_player, is_dirty=False)
                list_card_players, manilha_list = shuffle_deck(deck, number_player, is_dirty=False)
            case 4:
                print('Iniciando jogo para 4 jogadores...')
                # shuffle_deck(deck, number_player, is_dirty=False)
                list_card_players, manilha_list = shuffle_deck(deck, number_player, is_dirty=False)
            case _:
                print('Número inválido de jogadores! Iniciando jogo para 2 jogadores por padrão...')
    return number_player, list_card_players, manilha_list

def shuffle_deck(deck, number_player, is_dirty):
    wich_deck = 'Sujo' if is_dirty == True else 'Limpo'
    print(f'\nEmbaralhando o Baralho {wich_deck}...\n')
    list_card_players = []
    vira = ''
    manilha = ''
    for i in range(3 * number_player + 1):
        random_index_deck = random.randint(0,3)
        # print(random_index_deck)
        choice_card = random.choice(deck[random_index_deck])
        # print(choice_card)
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
    order_strength = ['4', '5', '6', '7', 'Q', 'J', 'K', 'A', '2', '3'] if is_dirty == True else ['Q', 'J', 'K', 'A', '2', '3']
    index_vira = order_strength.index(vira[0])
    if index_vira == order_strength[-1]:
        manilha = order_strength[0]
    else:
        manilha = order_strength[index_vira + 1]
    manilha_list = [f'{manilha} ♣', f'{manilha} ♥', f'{manilha} ♠', f'{manilha} ♦']
    print(f'As Manilhas são: {manilha_list}')
    return list_card_players, manilha_list


def start_game(number_player, list_card_players, manilha_list):
    print('\nIniciando o jogo de Truco...')
    print(f'Número de jogadores: {number_player}')
    print(f'Cartas dos jogadores: {list_card_players}')
    print(f'Manilhas: {manilha_list}')
    vira = list_card_players[-1]
    number_vira = vira[0]
    suit_vira = vira[2]

    match number_player:
        case 2:
            while True:
                player1_cards = list_card_players[0:3]
                player2_cards = list_card_players[3:6]
                points = []
                player1_truco = False
                player2_truco = False
                round_value = 1
                count_points_player1 = 0
                count_points_player2 = 0
                points_player1 = '00'
                points_player2 = '00'
                isround_over = False
                print(f'Jogador 1 cartas: {player1_cards}')
                print(f'Jogador 2 cartas: {player2_cards}')
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
                print(f'│                                       ┌─────┐                                       │')
                print(f'│                                       │{suit_vira}    │                                       │')
                print(f'│                                       │  {number_vira}  │                                       │')
                print(f'│                                       │    {suit_vira}│                                       │')
                print(f'│                                       └─────┘                                       │')
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
                print(f'│ │   {points_player1}   │   {points_player2}   │           │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│        │ 〇 〇 〇 │ 〇 〇 〇 ││')
                print(f'│ └─────────────────┘           └─────┘ └─────┘ └─────┘        └─────────────────────┘│')
                print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')

                while True:
                    print('\nQual carta você quer jogar? ')
                    print(f'1 - {player1_cards[0]}')
                    print(f'2 - {player1_cards[1]}')
                    print(f'3 - {player1_cards[2]}')
                    print(f'4 - Pedir Truco')
                    card_option = input('Escolha uma opção (1, 2 ou 3): ').strip()
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
                            print('Você pediu Truco!')
                            player1_truco = True   
                            for card in player2_cards:
                                if card in manilha_list:
                                    print('O oponente aceitou o Truco!')
                                    round_value = 3
                                    break
                            else:
                                print('O oponente recusou o Truco! Você ganha a rodada.')
                                count_points_player1 += round_value
                                isround_over = True
                                points_player1 = f'0{count_points_player1}' if count_points_player1 < 10 else str(count_points_player1)
                                break
                            
                            
                        case _:
                            print('Opção inválida! Tente novamente')

                if isround_over == True:
                    list_card_players_continue, manilha_list_continue = shuffle_deck(deck_dirty, number_player=2, is_dirty=True)
                    continue_game(list_card_players_continue, manilha_list_continue, points_player1, points_player2, number_player=2)
                    break
                else:
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
                    print(f'│                                       ┌─────┐                                       │')
                    print(f'│                                       │{suit_vira}    │                                       │')
                    print(f'│                                       │  {number_vira}  │                                       │')
                    print(f'│                                       │    {suit_vira}│                                       │')
                    print(f'│                                       └─────┘                                       │')
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
                    print(f'│ │   {points_player1}   │   {points_player2}   │               │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│            │ 〇 〇 〇 │ 〇 〇 〇 ││')
                    print(f'│ └─────────────────┘               └─────┘ └─────┘            └─────────────────────┘│')
                    print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')          
                    
                    time.sleep(1)        
            
            
        
            
        case 4:
            player1_cards = list_card_players[0:3]
            player2_cards = list_card_players[3:6]
            player3_cards = list_card_players[6:9]
            player4_cards = list_card_players[9:12]
            points_team1 = '00'
            points_team2 = '00'
            print(f'Jogador 1 cartas: {player1_cards}')
            print(f'Jogador 2 cartas: {player2_cards}')
            print(f'Jogador 3 cartas: {player3_cards}')
            print(f'Jogador 4 cartas: {player4_cards}')
            print(f'┌─────────────────────────────────────────────────────────────────────────────────────┐')
            print(f'│                              ┌─────┐ ┌─────┐ ┌─────┐                                │')
            print(f'│                              │ ┌─┐ │ │ ┌─┐ │ │ ┌─┐ │                                │')
            print(f'│                              │ │ │ │ │ │ │ │ │ │ │ │                                │')
            print(f'│                              │ └─┘ │ │ └─┘ │ │ └─┘ │                                │')
            print(f'│                              └─────┘ └─────┘ └─────┘                                │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│  ┌──────────┐                                                         ┌──────────┐  │')
            print(f'│  │ ┌──────┐ │                                                         │ ┌──────┐ │  │')
            print(f'│  │ └──────┘ │                                                         │ └──────┘ │  │')
            print(f'│  └──────────┘                                                         └──────────┘  │')
            print(f'│  ┌──────────┐                        ┌─────┐                          ┌──────────┐  │')
            print(f'│  │ ┌──────┐ │                        │{suit_vira}    │                          │ ┌──────┐ │  │')
            print(f'│  │ └──────┘ │                        │  {number_vira}  │                          │ └──────┘ │  │')
            print(f'│  └──────────┘                        │    {suit_vira}│                          └──────────┘  │')
            print(f'│  ┌──────────┐                        └─────┘                          ┌──────────┐  │')
            print(f'│  │ ┌──────┐ │                                                         │ ┌──────┐ │  │')
            print(f'│  │ └──────┘ │                                                         │ └──────┘ │  │')
            print(f'│  └──────────┘                                                         └──────────┘  │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│ ┌─────────────────┐                                          ┌─────────────────────┐│')
            print(f'│ │     Placar      │           ┌─────┐ ┌─────┐ ┌─────┐        │       Rodadas       ││')
            print(f'│ │  ─────────────  │           │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │ │{player1_cards[2][2]}    │        │  ─────────────────  ││')
            print(f'│ │  Vocês │  Eles  │           │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │ │  {player1_cards[2][0]}  │        │   Vocês  │    Eles  ││')
            print(f'│ │   {points_team1}   │   {points_team2}   │           │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│        │ 〇 〇 〇 │ 〇 〇 〇 ││')
            print(f'│ └─────────────────┘           └─────┘ └─────┘ └─────┘        └─────────────────────┘│')
            print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')
        
        

def continue_game(list_card_players_continue, list_manilha_continue, points_player1, points_player2, number_player):
    manilha_list = list_manilha_continue 
    print(f'Manilhas: {manilha_list}')
    vira = list_card_players_continue[-1]
    number_vira = vira[0]
    suit_vira = vira[2]

    match number_player:
        case 2:
            while True:
                player1_cards = list_card_players_continue[0:3]
                player2_cards = list_card_players_continue[3:6]
                player1_truco = False
                player2_truco = False
                round_value = 1
                points_p1 = points_player1 
                points_p2 = points_player2 
                isround_over = False
                print(f'Jogador 1 cartas: {player1_cards}')
                print(f'Jogador 2 cartas: {player2_cards}')
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
                print(f'│                                       ┌─────┐                                       │')
                print(f'│                                       │{suit_vira}    │                                       │')
                print(f'│                                       │  {number_vira}  │                                       │')
                print(f'│                                       │    {suit_vira}│                                       │')
                print(f'│                                       └─────┘                                       │')
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
                print(f'│ │   {points_p1}   │   {points_p2}   │           │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│        │ 〇 〇 〇 │ 〇 〇 〇 ││')
                print(f'│ └─────────────────┘           └─────┘ └─────┘ └─────┘        └─────────────────────┘│')
                print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')
                
                while True:
                    print('\nQual carta você quer jogar? ')
                    print(f'1 - {player1_cards[0]}')
                    print(f'2 - {player1_cards[1]}')
                    print(f'3 - {player1_cards[2]}')
                    print(f'4 - Pedir Truco')
                    
                    card_option = input('Escolha uma opção (1, 2 ou 3): ').strip()
    





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