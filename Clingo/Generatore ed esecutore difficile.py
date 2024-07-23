import os
import random
import subprocess
import time
import csv
import re

# Parametri generali delle istanze
NUM_INSTANCES = 30

# Definizione delle cartelle per le diverse difficoltà
BASE_FOLDER = 'NEWinstancesClingo'
EASY_FOLDER = os.path.join(BASE_FOLDER, 'NEWeasy')
MEDIUM_FOLDER = os.path.join(BASE_FOLDER, 'NEWmedium')
HARD_FOLDER = os.path.join(BASE_FOLDER, 'NEWhard')

# Creazione delle cartelle se non esistono già
os.makedirs(EASY_FOLDER, exist_ok=True)
os.makedirs(MEDIUM_FOLDER, exist_ok=True)
os.makedirs(HARD_FOLDER, exist_ok=True)

def generate_instance(instance_id, difficulty):
    if difficulty == 'NEWfacile':
        n = random.randint(21, 28) // 7 * 7
        num_teams = random.randint(1, 2)
        folder = EASY_FOLDER
    elif difficulty == 'NEWmedio':
        n = random.randint(28, 35) // 7 * 7  
        num_teams = random.randint(2, 4)
        folder = MEDIUM_FOLDER
    elif difficulty == 'NEWdifficile':
        n = random.randint(63, 70) // 7 * 7
        num_teams = random.randint(4, 8)
        folder = HARD_FOLDER

    # Aumenta num_pairs in base alla difficoltà e al numero di squadre
    if num_teams > 1:
        if difficulty == 'NEWfacile':
            num_pairs = random.randint(1, 2)
        elif difficulty == 'NEWmedio':
            num_pairs = random.randint(4, 6)
        elif difficulty == 'NEWdifficile':
            num_pairs = random.randint(6, 8)
    else:
        num_pairs = 0

    roles = ['difensore', 'attaccante', 'centrocampista', 'portiere']
    
    players = []
    for player_id in range(1, n + 1):
        player_roles = random.sample(roles, 2)
        players.append(f'player({player_id}, {player_roles[0]}, {player_roles[1]}).')
    
    different_teams = []
    all_teams = random.sample(range(1, num_teams + 1), num_teams)
    for i in range(1, num_teams + 1):
        for j in range(i + 1, num_teams + 1):
            different_teams.append(f'different_team({i}, {j}).')

    all_players = list(range(1, n + 1))
    pairs = random.sample([(p1, p2) for p1 in all_players for p2 in all_players if p1 < p2], num_pairs)
    pair_constraints = [f'different_team({p1}, {p2}).' for (p1, p2) in pairs]

    file_path = os.path.join(folder, f'instance_{instance_id}.lp')

    with open(file_path, 'w') as f:
        f.write(f'num_squadre({num_teams}).\n')
        f.write('\n'.join(players) + '\n')
        f.write('\n'.join(different_teams) + '\n')
        f.write('\n'.join(pair_constraints) + '\n')

    print(f'Generated {file_path} with difficulty {difficulty}')
    return num_teams, n

def run_clingo(model, data_file, time_limit):
    start_time = time.time()
    try:
        result = subprocess.run(
            ["clingo", model, data_file, "--opt-mode=optN", "--time-limit", str(time_limit), "--models=1"],
            capture_output=True,
            text=True,
            timeout=time_limit
        )
        end_time = time.time()
        execution_time = end_time - start_time
        return result.stdout, result.stderr, result.returncode, execution_time
    except subprocess.TimeoutExpired:
        return "", "Il processo ha superato il limite di tempo.", 1, time_limit

def extract_execution_time(output):
    # Usa una regex per trovare la riga che contiene il tempo
    match = re.search(r'Time\s+:\s+([\d\.]+)s', output)
    if match:
        return float(match.group(1))
    return None

def process_directory(model_path, input_dir, output_dir, time_limit, results):
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".lp"):
            input_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_output.txt")

            output_clingo, error_clingo, return_code_clingo, exec_time_clingo = run_clingo(model_path, input_path, time_limit)

            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(f"Input file: {filename}\n")
                f.write("Input data:\n")
                with open(input_path, "r") as input_file:
                    f.write(input_file.read())
                f.write("\nOutput Clingo:\n")

                if "unsatisfiable" in output_clingo.lower():
                    f.write("Il problema non è soddisfacibile con Clingo.\n")
                else:
                    f.write(output_clingo)

                f.write(f"\nTempo di esecuzione Clingo: {exec_time_clingo:.2f} secondi\n")
                if error_clingo:
                    f.write("\nErrors Clingo:\n")
                    f.write(error_clingo)

            # Estrai i dati dal file di input per la tabella
            with open(input_path, "r") as input_file:
                lines = input_file.readlines()
                num_squadre = int(lines[0].split('(')[1].split(')')[0])
                num_giocatori = sum(1 for line in lines if line.startswith('player'))

            # Estrai il tempo di esecuzione specifico dall'output
            extracted_time = extract_execution_time(output_clingo)
            if extracted_time is None:
                extracted_time = exec_time_clingo  # Usa il tempo di esecuzione di default se non trovato

            results.append([filename, num_squadre, num_giocatori, extracted_time])
            print(f"Processed {filename} - output saved to {output_file_path}")

def main():
    current_dir = os.getcwd()
    model_path = os.path.join(current_dir, "implASP.lp")

    difficulties = ["NEWeasy", "NEWmedium", "NEWhard"]
    time_limit = 300

    results = []

    for i in range(1, NUM_INSTANCES + 1):
        if i <= 10:
            difficulty = 'NEWfacile'
        elif i <= 20:
            difficulty = 'NEWmedio'
        else:
            difficulty = 'NEWdifficile'
        num_teams, num_players = generate_instance(i, difficulty)
        results.append([f'instance_{i}.lp', num_teams, num_players, 0])  # Placeholder for execution time

    for difficulty in difficulties:
        input_dir = os.path.join(current_dir, "NEWinstancesClingo", difficulty)
        output_dir = os.path.join(current_dir, f"NEWoutput_clingo_{difficulty}")
        process_directory(model_path, input_dir, output_dir, time_limit, results)

    # Salva i risultati in un file CSV
    csv_file_path = os.path.join(current_dir, "clingo_results.csv")
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "NumSquadre", "NumGiocatori", "TempoEsecuzione"])
        writer.writerows(results)

    print(f"Results saved to {csv_file_path}")

if __name__ == "__main__":
    main()
