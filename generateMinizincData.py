import os
import random

# Parametri generali delle istanze
NUM_INSTANCES = 30

# Definizione delle cartelle per le diverse difficoltà
EASY_FOLDER = 'instancesMinizinc/easy'
MEDIUM_FOLDER = 'instancesMinizinc/medium'
HARD_FOLDER = 'instancesMinizinc/hard'

# Creazione delle cartelle se non esistono già
os.makedirs(EASY_FOLDER, exist_ok=True)
os.makedirs(MEDIUM_FOLDER, exist_ok=True)
os.makedirs(HARD_FOLDER, exist_ok=True)

# Funzione per generare istanze di benchmark con varie complessità
def generate_instance(instance_id, difficulty):
    # Definizione dei range per i parametri in base alla difficoltà
    if difficulty == 'facile':
        n = random.randint(7,14) // 7 * 7
        num_pairs = random.randint(0,1)
        k = random.randint(1, 2)
        if(k == 1):
            num_pairs=0
        folder = EASY_FOLDER
    elif difficulty == 'medio':
        n = random.randint(21, 35) // 7 * 7  
        num_pairs = random.randint(1, 3)
        k = random.randint(2, 3)
        folder = MEDIUM_FOLDER
    elif difficulty == 'difficile':
        n = random.randint(35, 70) // 7 * 7
        num_pairs = random.randint(1, 5)
        k = random.randint(1, 5)
        folder = HARD_FOLDER
    
    roles = []
    for _ in range(n):
        # Ogni giocatore deve scegliere esattamente due ruoli possibili
        player_roles = random.sample(['g', 'd', 'm', 'f'], 2)
        roles.append('{' + ', '.join(f'{role}' for role in player_roles) + '}')

   # Genera player1 e player2 in modo che siano diversi tra loro
    player1 = random.sample(range(1, n + 1), num_pairs)
    player2 = random.sample(sorted(set(range(1, n + 1)) - set(player1)), num_pairs)

    # Percorso completo del file .dzn
    file_path = os.path.join(folder, f'data_{instance_id}.dzn')

    # Generazione del file .dzn per ogni istanza
    with open(file_path, 'w') as f:
        f.write(f'n = {n};\n')
        f.write(f'k = {k};\n')
        f.write('roles = [\n')
        f.write(',\n'.join(roles) + '\n')
        f.write('];\n')
        f.write(f'num_pairs = {num_pairs};\n')
        f.write('player1 = [' + ', '.join(map(str, player1)) + '];\n')
        f.write('player2 = [' + ', '.join(map(str, player2)) + '];\n')

    print(f'Generated {file_path} with difficulty {difficulty}')

# Generazione delle 30 istanze con varie complessità
for i in range(1, NUM_INSTANCES + 1):
    if i <= 10:
        generate_instance(i, 'facile')
    elif i <= 20:
        generate_instance(i, 'medio')
    else:
        generate_instance(i, 'difficile')
