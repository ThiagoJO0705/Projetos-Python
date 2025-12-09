
import tabulate

def addManwha(manwha_list, manwha_obj):
    genres_list = ['Tower', 'Martial Arts', 'Action', 'Super Power', 'Fantasy', 'Romance', 'Comedy', 'Drama', 'Isekai', 'Adventure', 'Sci-fi', 'Time Travel']

    title = input('\nDigite o título do manwha: ').strip()
    while not title:
        print('\nTítulo não pode ser vazio. Tente novamente.')
        title = input('Digite o título do manwha: ').strip()

    while any(manwha['title'].lower() == title.lower() for manwha in manwha_list):
        print('\nManwha já existe na biblioteca. Tente outro título.')
        title = input('Digite o título do manwha: ').strip()
    manwha_obj['title'] = title.title()

    print(f'\nGêneros disponíveis: {genres_list}')
    
    genres_input = input('\nDigite o(s) gênero(s) do manwha (separados por vírgula): ').strip()
    genres_list_final = [] 
    for g in genres_input.split(','): 
        genres_list_final.append(g.strip().title())

    while not all(g in genres_list for g in genres_list_final):
        print('\nUm ou mais gêneros são inválidos.')
        print(f'\nGêneros disponíveis: {genres_list}')
        y_or_n = input('\nDeseja selecionar "Outro" como gênero? (s/n): ').strip().lower()
        if y_or_n == 's':
            genres_list_final = ['Outro']
            break
        genres_input = input('\nDigite o(s) gênero(s) do manwha (separados por vírgula): ').strip()
        genres_list_final = [] 
        for g in genres_input.split(','): 
            genres_list_final.append(g.strip())

    manwha_obj['genre'] = genres_list_final

    while True:
        try:
            manwha_obj['chapter'] = int(input('\nDigite o número do capítulos atual: ').strip())
            break
        except (ValueError, TypeError):
            print('\nPor favor, insira um número válido para o capítulo atual.')
            
    while True:
        try:
            read_until = int(input('\nDigite até qual capítulo você leu: ').strip())
            while read_until > manwha_obj['chapter']:
                print('\nO capítulo lido não pode ser maior que o capítulo atual.')
                read_until = int(input('\nDigite até qual capítulo você leu: ').strip())
            break
            
        except (ValueError, TypeError):
            print('\nPor favor, insira um número válido para o capítulo lido.')
        
    manwha_obj['read_until'] = read_until

    while True:
        try:
            print('\nStatus disponíveis: 1 - Em Andamento, 2 - Concluído, 3 - Hiato, 4 - Cancelado')
            status_option= int(input('\nSelecione o status do Manwha: ').strip())
            break
        except (ValueError, TypeError):
            print('\nPor favor, insira um número válido para o status.')

    match status_option:
        case 1:
            manwha_obj['status'] = 'Em Andamento'
        case 2:
            manwha_obj['status'] = 'Concluído'
        case 3:
            manwha_obj['status'] = 'Hiato'
        case 4:
            manwha_obj['status'] = 'Cancelado'
        case _:
            manwha_obj['status'] = 'Em Andamento'
    

    print('\nIdiomas disponíveis: 1 - pt-br (Português), 2 - en (Inglês), 3 - es (Espanhol)')

    while True:
        try:
            language_option= int(input('\nEscolha o idioma do manwha (1, 2 ou 3): ').strip())
            break
        except (ValueError, TypeError):
            print('\nPor favor, insira um número válido para o idioma.')

    match language_option:
        case 1:
            manwha_obj['language'] = 'pt-br'
        case 2:
            manwha_obj['language'] = 'en'
        case 3:
            manwha_obj['language'] = 'es'
        case _:
            manwha_obj['language'] = 'pt-br'

    manwha_obj['id'] = id_generator(manwha_list)

    manwha_list.append(manwha_obj.copy())

    print(f'\nManwha "{title}" adicionada com sucesso!')



def listManwhas(manwha_list, headers):

    if not manwha_list:
        print('\nNenhum manwha na biblioteca.')
        return

    print('\nLista de Manwhas na Biblioteca:')
    print('----------------------------------')

    print(tabulate.tabulate(manwha_list, headers=headers, tablefmt="simple_grid"))


def removeManwha(manwha_list):
    title = input('\nDigite o título do manwha que deseja remover: ').strip().title()
    for manwha in manwha_list:
        if manwha['title'].lower() == title.lower():
            manwha_list.remove(manwha)
            print(f'\nManwha "{title}" removida com sucesso!')
            return
        else:
            print(f'\nManwha "{title}" não encontrada na biblioteca.')
            return
        

def searchManwha(manwha_list, headers):
    print('\n1 - Buscar Manwha na Biblioteca por Título')
    print('2 - Buscar por Gênero')
    print('3 - Buscar por Status')
    match_option = input('\nEscolha uma opção (1, 2 ou 3): ').strip()
    match match_option:
        case '1':
            searchManwhaByTitle(manwha_list, headers)
        case '2':
            searchManwhaByGenre(manwha_list, headers)
        case '3':
            searchManwhaByStatus(manwha_list, headers)
        case _:
            print('\nOpção inválida. Retornando ao menu principal.')
            return
        

def searchManwhaByTitle(manwha_list, headers):
    title = input('\nDigite o título do manwha que deseja buscar: ').strip()
    for manwha in manwha_list:
        if manwha['title'].lower() == title.lower():
            print('\nManwha encontrado:')
            print(tabulate.tabulate([manwha], headers=headers, tablefmt="simple_grid"))
            return
        else:
            print(f'\nManwha "{title}" não encontrada na biblioteca.')
            return


def searchManwhaByGenre(manwha_list, headers):
    print('\nGêneros disponíveis para busca: Tower, Martial Arts, Action, Super Power, Fantasy, Romance, Comedy, Drama, Isekai, Adventure, Sci-fi, Time Travel, Outro')
    genre = input('\nDigite o gênero do manwha que deseja buscar: ').strip().lower()
    found_manwhas = []
    for manwha in manwha_list:
        if any(g.lower() == genre for g in manwha['genre']):
            found_manwhas.append(manwha)
    if found_manwhas == []:
        print(f'\nNenhum manwha encontrado com o gênero "{genre}".')
    else:
        print(f'\nManwhas encontrados com o gênero "{genre}":')
        print(tabulate.tabulate(found_manwhas, headers=headers, tablefmt="simple_grid"))
    

def searchManwhaByStatus(manwha_list, headers):
    print('\nStatus disponíveis para busca: Em Andamento, Concluído, Hiato, Cancelado')
    status = input('\nDigite o status do manwha que deseja buscar: ').strip().lower()
    found_manwhas = []
    for manwha in manwha_list:
        if manwha['status'].lower() == status:
            found_manwhas.append(manwha)
    if found_manwhas == []:
        print(f'\nNenhum manwha encontrado com o status "{status}".')
    else:
        print(f'\nManwhas encontrados com o status "{status}":')
        print(tabulate.tabulate(found_manwhas, headers=headers, tablefmt="simple_grid"))


def updateManwha(manwha_list):
    title = input('\nDigite o título do manwha que deseja atualizar: ').strip()
    for manwha in manwha_list:
        if manwha['title'].lower() == title.lower():
            print('\nManwha encontrado. O que deseja atualizar?')
            print('1 - Título')
            print('2 - Gênero(s)')
            print('3 - Capítulo Atual')
            print('4 - Lido até')
            print('5 - Status')
            print('6 - Idioma')
            update_option = input('\nEscolha uma opção (1 a 6): ').strip()
            match update_option:
                case '1':
                    new_title = input('\nDigite o novo título: ').strip()
                    manwha['title'] = new_title.title()
                    print('\nTítulo atualizado com sucesso!')
                    while not manwha['title']:
                        print('\nTítulo não pode ser vazio. Tente novamente.')
                        new_title = input('Digite o novo título: ').strip()
                        manwha['title'] = new_title.title()
                case '2':
                    new_genres = input('\nDigite o(s) novo(s) gênero(s) (separados por vírgula): ').strip()
                    genres_list_final = [] 
                    for g in new_genres.split(','): 
                        genres_list_final.append(g.strip().title())
                    manwha['genre'] = genres_list_final
                    print('\nGênero(s) atualizado(s) com sucesso!')
                case '3':
                    new_chapter = input('\nDigite o novo capítulo atual: ').strip()
                    if new_chapter.isdigit():
                        manwha['chapter'] = int(new_chapter)
                        print('\nCapítulo atualizado com sucesso!')
                    else:
                        print('\nEntrada inválida. Capítulo não atualizado.')
                case '4':
                    new_read_until = input('\nDigite o novo capítulo lido até: ').strip()
                    if new_read_until.isdigit():
                        manwha['read_until'] = int(new_read_until)
                        print('\nCapítulo lido até atualizado com sucesso!')
                    else:
                        print('\nEntrada inválida. Capítulo lido até não atualizado.')
                case '5':
                    print('\nStatus disponíveis: 1 - Em Andamento, 2 - Concluído, 3 - Hiato, 4 - Cancelado')
                    new_status = input('\nSelecione o novo status: ').strip()
                    match new_status:
                        case '1':
                            new_status = 'Em Andamento'
                        case '2':
                            new_status = 'Concluído'
                        case '3':
                            new_status = 'Hiato'
                        case '4':
                            new_status = 'Cancelado'
                        case _:
                            new_status = 'Em Andamento'
                    manwha['status'] = new_status.title()
                    print('\nStatus atualizado com sucesso!')
                case '6':
                    print('\nIdiomas disponíveis: 1 - pt-br (Português), 2 - en (Inglês), 3 - es (Espanhol)')
                    new_language = input('\nSelecione o novo idioma: ').strip()
                    if new_language == '1':
                        manwha['language'] = 'pt-br'
                    elif new_language == '2':
                        manwha['language'] = 'en'
                    elif new_language == '3':
                        manwha['language'] = 'es'
                    else:
                        manwha['language'] = 'pt-br'
                    print('\nIdioma atualizado com sucesso!')
            return
    print(f'\nManwha "{title}" não encontrada na biblioteca.')


def id_generator(manwha_list):
    if not manwha_list:
        id = 1
    else:
        id = manwha_list[-1]['id'] + 1  
    return id



manwha_list = [{'title': 'Solo Leveling', 'genre': ['Action', 'Fantasy', 'Adventure'], 'chapter': 178, 'read_until': 178, 'status': 'Concluído', 'language': 'pt-br', 'id': 1},
               {'title': 'Tower of God', 'genre': ['Action', 'Tower', 'Fantasy'], 'chapter': 550, 'read_until': 500, 'status': 'Em Andamento', 'language': 'en', 'id': 2},
                {'title': 'The Beginning After The End', 'genre': ['Isekai', 'Adventure', 'Fantasy', 'Action'], 'chapter': 150, 'read_until': 150, 'status': 'Em Andamento', 'language': 'pt-br', 'id': 3}]

manwha_obj = {
    'title': '',
    'genre': [],
    'chapter': 0,
    'read_until': 0,
    'status': '',
    'language': '',
    'id': 0
}

    
headers = {
    'title': 'Título',
    'genre': 'Gênero(s)',
    'chapter': 'Capítulo Atual',
    'read_until': 'Lido até',
    'status': 'Status',
    'language': 'Idioma',
    'id': 'ID'
}

print('\nBem-vindo à Biblioteca de Manwhas!\n')
while True:
    print('========== Menu Principal ==========')
    print('1 - Adicionar Manwha')
    print('2 - Listar Manwhas')
    print('3 - Buscar Manwha')
    print('4 - Atualizar Manwha')
    print('5 - Remover Manwha')
    print('6 - Sair\n')

    try:
        option = int(input('\nEscolha uma opção: '))
    except (ValueError, TypeError):
        print('\nPor favor, insira um número válido para a opção.')
        continue

    match option:
        case 1:
            print('Adicionar Manwha selecionado.')
            addManwha(manwha_list, manwha_obj)

        case 2:
            print('Listar Manwhas selecionado.')
            listManwhas(manwha_list, headers)

        case 3:
            print('Buscar Manwha selecionado.')
            searchManwha(manwha_list, headers)

        case 4:
            print('Atualizar Manwha selecionado.')
            updateManwha(manwha_list)

        case 5:
            print('Remover Manwha selecionado.')
            removeManwha(manwha_list)

        case 6:
            print('Saindo do programa.')
            break

        case _:
            print('Opção inválida. Tente novamente.')
