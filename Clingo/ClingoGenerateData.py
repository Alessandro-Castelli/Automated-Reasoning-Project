import os
import random

# Parametri generali delle istanze
NUM_INSTANCES = 30

# Definizione delle cartelle per le diverse difficoltà
EASY_FOLDER = 'instancesClingo/easy'
MEDIUM_FOLDER = 'instancesClingo/medium'
HARD_FOLDER = 'instancesClingo/hard'

# Creazione delle cartelle se non esistono già
os.makedirs(EASY_FOLDER, exist_ok=True)
os.makedirs(MEDIUM_FOLDER, exist_ok=True)
os.makedirs(HARD_FOLDER, exist_ok=True)

# Funzione per generare istanze di benchmark con varie complessità
def generate_instance(instance_id, difficulty):
    # Definizione dei range per i parametri in base alla difficoltà
    if difficulty == 'facile':
        n = random.randint(14,14) // 7 * 7
        num_teams = random.randint(1, 2)
        folder = EASY_FOLDER
    elif difficulty == 'medio':
        n = random.randint(14, 21) // 7 * 7  
        num_teams = random.randint(2, 3)
        folder = MEDIUM_FOLDER
    elif difficulty == 'difficile':
        n = random.randint(28, 35) // 7 * 7
        num_teams = random.randint(2, 4)
        folder = HARD_FOLDER

    # Impostazione di num_pairs a 0 se num_teams è 1
    num_pairs = random.randint(0, 1) if num_teams > 1 else 0

    roles = ['difensore', 'attaccante', 'centrocampista', 'portiere']
    
    # Generazione dei ruoli per i giocatori
    players = []
    for player_id in range(1, n + 1):
        player_roles = random.sample(roles, 2)
        players.append(f'player({player_id}, {player_roles[0]}, {player_roles[1]}).')
    
    # Generazione delle squadre che devono essere diverse
    different_teams = []
    all_teams = random.sample(range(1, num_teams + 1), num_teams)
    for i in range(1, num_teams + 1):
        for j in range(i + 1, num_teams + 1):
            different_teams.append(f'different_team({i}, {j}).')

    # Selezione casuale di coppie di giocatori per vincoli di differenza
    all_players = list(range(1, n + 1))
    pairs = random.sample([(p1, p2) for p1 in all_players for p2 in all_players if p1 < p2], num_pairs)
    pair_constraints = [f'different_team({p1}, {p2}).' for (p1, p2) in pairs]

    # Percorso completo del file
    file_path = os.path.join(folder, f'instance_{instance_id}.lp')

    # Generazione del file con i dati
    with open(file_path, 'w') as f:
        f.write(f'num_squadre({num_teams}).\n')
        f.write('\n'.join(players) + '\n')
        f.write('\n'.join(different_teams) + '\n')
        f.write('\n'.join(pair_constraints) + '\n')

    print(f'Generated {file_path} with difficulty {difficulty}')

# Generazione delle 30 istanze con varie complessità
for i in range(1, NUM_INSTANCES + 1):
    if i <= 10:
        generate_instance(i, 'facile')
    elif i <= 20:
        generate_instance(i, 'medio')
    else:
        generate_instance(i, 'difficile')
