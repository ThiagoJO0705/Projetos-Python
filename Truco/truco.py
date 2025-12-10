import random

def play_truco():
    print('\nIniciando uma nova partida de Truco!')
    print('Qual o tipo de baralho você quer usar?')
    print('1 - Baralho Limpo')
    print('2 - Baralho Sujo')
    truco_option = input('Escolha uma opção (1 ou 2): ').strip()
    match truco_option:
        case '1':
            print('\nVocê escolheu o Baralho Limpo!')
            number_player, list_card_players = choose_players(deck_clean, is_dirty=False)
        case '2':
            print('\nVocê escolheu o Baralho Sujo!')
            number_player, list_card_players = choose_players(deck_dirty, is_dirty=True)
        case _:
            print('\nOpção inválida! Usando baralho sujo por padrão.')
            number_player, list_card_players = choose_players(deck_dirty, is_dirty=True)
    start_game(number_player, list_card_players)
    

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
                list_card_players = shuffle_deck(deck, number_player, is_dirty=True)
            case 4:
                print('Iniciando jogo para 4 jogadores...')
                list_card_players = shuffle_deck(deck, number_player, is_dirty=True)
            case _:
                print('Número inválido de jogadores! Iniciando jogo para 2 jogadores por padrão...')
    else:
        match number_player:
            case 2:
                print('Iniciando jogo para 2 jogadores...')
                # shuffle_deck(deck, number_player, is_dirty=False)
                list_card_players = shuffle_deck(deck, number_player, is_dirty=False)
            case 4:
                print('Iniciando jogo para 4 jogadores...')
                # shuffle_deck(deck, number_player, is_dirty=False)
                list_card_players = shuffle_deck(deck, number_player, is_dirty=False)
            case _:
                print('Número inválido de jogadores! Iniciando jogo para 2 jogadores por padrão...')
    return number_player, list_card_players


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
    print(f'As Manilhas são: {manilha} ♣, {manilha} ♥, {manilha} ♠, {manilha} ♦')
    return list_card_players


def start_game(number_player, list_card_players):
    print('\nIniciando o jogo de Truco...')
    print(f'Número de jogadores: {number_player}')
    print(f'Cartas dos jogadores: {list_card_players}')
    vira = list_card_players[-1]
    number_vira = vira[0]
    suit_vira = vira[2]

    match number_player:
        case 2:
            player1_cards = list_card_players[0:3]
            player2_cards = list_card_players[3:6]
            print(f'Jogador 1 cartas: {player1_cards}')
            print(f'Jogador 2 cartas: {player2_cards}')
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
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                      ┌─────┐                                        │')
            print(f'│                                      │{suit_vira}    │                                        │')
            print(f'│                                      │  {number_vira}  │                                        │')
            print(f'│                                      │    {suit_vira}│                                        │')
            print(f'│                                      └─────┘                                        │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                                                                                     │')
            print(f'│                              ┌─────┐ ┌─────┐ ┌─────┐                                │')
            print(f'│                              │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │ │{player1_cards[2][2]}    │                                │')
            print(f'│                              │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │ │  {player1_cards[2][0]}  │                                │')
            print(f'│                              │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│                                │')
            print(f'│                              └─────┘ └─────┘ └─────┘                                │')
            print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')
        case 4:
            player1_cards = list_card_players[0:3]
            player2_cards = list_card_players[3:6]
            player3_cards = list_card_players[6:9]
            player4_cards = list_card_players[9:12]
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
            print(f'│                              ┌─────┐ ┌─────┐ ┌─────┐                                │')
            print(f'│                              │{player1_cards[0][2]}    │ │{player1_cards[1][2]}    │ │{player1_cards[2][2]}    │                                │')
            print(f'│                              │  {player1_cards[0][0]}  │ │  {player1_cards[1][0]}  │ │  {player1_cards[2][0]}  │                                │')
            print(f'│                              │    {player1_cards[0][2]}│ │    {player1_cards[1][2]}│ │    {player1_cards[2][2]}│                                │')
            print(f'│                              └─────┘ └─────┘ └─────┘                                │')
            print(f'└─────────────────────────────────────────────────────────────────────────────────────┘')
        
        






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

        

    # ♥  ♦  ♠  ♣