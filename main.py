import httpx


def question_1() -> int:
    """ Returns and Prints the number of Pokemon that have 'at' and two 'a' in their names
    :return: Number of Pokemon
    """
    url = 'https://pokeapi.co/api/v2/pokemon'
    response = httpx.get(url).json()
    params = {'limit': response['count']}
    # Retrieve all Pokemon at once
    response = httpx.get(url, params=params).json()

    count = 0
    for pokemon in response["results"]:
        name = pokemon['name']
        if verify_name(name):
            count += 1
    print(f"1. Numero de Pokemon que contienen 'at' y tienen 2 'a' en su nombre es {count}")
    return count


def question_2(name: str = 'raichu') -> int:
    """ Returns and Prints the number of species that can interbreed with the Pokemon given by parameter
    :param name: Name of Pokemon to search. Default is raichu
    :return Number of species that can interbreed with the Pokemon:
    """
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = httpx.get(url).json()

    specie_url = response['species']['url']
    response = httpx.get(specie_url).json()
    egg_groups = response['egg_groups']
    species_list = []
    for egg_group in egg_groups:
        response = httpx.get(egg_group['url']).json()
        for specie in response['pokemon_species']:
            species_list.append(specie['name'])
    species_list.remove(name)
    species_list = dict.fromkeys(species_list).keys()
    print(f"2. El número de especies que pueden procrear con {name} es {len(species_list)}")
    return len(species_list)


def question_3(pokemon_type: str = "fighting") -> list:
    """Returns a list with the maximum and minimum weight of a Pokemon type given by parameter
    :param pokemon_type: Pokemon Type to search. Default is fighting
    :return: List with the maximum weight at position 0 and minimum weight at position 1
    """
    url = f'https://pokeapi.co/api/v2/type/{pokemon_type}'
    response = httpx.get(url).json()
    min_weight = 999999
    max_weight = 0
    for pokemon in response['pokemon']:
        url = pokemon['pokemon']['url']
        pokemon_info = httpx.get(url).json()
        # Indicates if the Pokemon belongs to generation 1
        generation = False
        for indice in pokemon_info['game_indices']:
            version_name = indice['version']['name']
            # Versions of generation 1 are red,blue and yellow
            if version_name == 'red' or version_name == 'blue' or version_name == 'yellow':
                generation = True
                break
        if not generation:
            break
        if pokemon_info['weight'] < min_weight:
            min_weight = pokemon_info['weight']
        if pokemon_info['weight'] > max_weight:
            max_weight = pokemon_info['weight']

    print(f"3. El peso maximo y minimo de los pokemon de tipo {pokemon_type} es {[max_weight, min_weight]}")
    return [max_weight, min_weight]


def verify_name(name: str) -> bool:
    """ Verifies that the pokemon name contains the substring 'at' and exactly two 'a'.
        :param name: pokemon name to verify
        :return True if the name meets the condition , False otherwhise
    """
    count = 0
    for i in name:
        if i == 'a':
            count += 1
    return count == 2 and 'at' in name


question_1()
question_2()
question_3()
