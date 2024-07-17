import os
import subprocess
import time
from collections import defaultdict

# Ottenere la directory corrente
current_dir = os.getcwd()

# Costruire i percorsi
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
model_path = os.path.join(current_dir, "Minizinc Code.mzn")
input_dir = os.path.join(current_dir, "instancesMinizinc", "easy")
output_dir = os.path.join(current_dir, "output")    

# Crea la cartella di output se non esiste
os.makedirs(output_dir, exist_ok=True)

# Funzione per eseguire il modello MiniZinc e misurare il tempo di esecuzione
def run_minizinc(model, data_file, solver):
    start_time = time.time()
    result = subprocess.run(
        ["minizinc", "--solver", solver, model, data_file],
        capture_output=True,
        text=True
    )
    end_time = time.time()
    execution_time = end_time - start_time
    return result.stdout, result.stderr, result.returncode, execution_time

# Itera su tutti i file di input nella cartella specificata
for filename in os.listdir(input_dir):
    if filename.endswith(".dzn"):
        input_path = os.path.join(input_dir, filename)
        output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_output.txt")

        # Struttura per ordinare i risultati per team
        team_results = defaultdict(list)

        # Esegui per Gecode
        output_gecode, error_gecode, return_code_gecode, exec_time_gecode = run_minizinc(model_path, input_path, "Gecode")
        
        # Esegui per Chuffed
        output_chuffed, error_chuffed, return_code_chuffed, exec_time_chuffed = run_minizinc(model_path, input_path, "Chuffed")

        # Salva i risultati nel file di output
        with open(output_file_path, "w") as f:
            f.write(f"Input file: {filename}\n")
            f.write("Input data:\n")
            with open(input_path, "r") as input_file:
                f.write(input_file.read())
            f.write("\nOutput Gecode:\n")

            # Controlla l'output di Gecode
            if "unsatisfiable" in output_gecode.lower():
                f.write("Il problema non è soddisfacibile con Gecode.\n")
            else:
                f.write(output_gecode)

            f.write(f"\nTempo di esecuzione Gecode: {exec_time_gecode:.2f} secondi\n")
            if error_gecode:
                f.write("\nErrors Gecode:\n")
                f.write(error_gecode)
            if return_code_gecode != 0:
                f.write(f"\nProcess Gecode returned error code: {return_code_gecode}\n")

            f.write("\nOutput Chuffed:\n")

            # Controlla l'output di Chuffed
            if "unsatisfiable" in output_chuffed.lower():
                f.write("Il problema non è soddisfacibile con Chuffed.\n")
            else:
                f.write(output_chuffed)

            f.write(f"\nTempo di esecuzione Chuffed: {exec_time_chuffed:.2f} secondi\n")
            if error_chuffed:
                f.write("\nErrors Chuffed:\n")
                f.write(error_chuffed)
            if return_code_chuffed != 0:
                f.write(f"\nProcess Chuffed returned error code: {return_code_chuffed}\n")

        print(f"Processed {filename} - output saved to {output_file_path}")

print("All files processed.")
