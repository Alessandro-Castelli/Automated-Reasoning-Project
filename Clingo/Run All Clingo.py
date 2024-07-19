import os
import subprocess
import time
from collections import defaultdict

def run_clingo(model, data_file, time_limit):
    start_time = time.time()
    try:
        result = subprocess.run(
            ["clingo", model, data_file, "--opt-mode=optN", "--time-limit", str(time_limit), "--models=1"],
            capture_output=True,
            text=True,
            timeout=time_limit  # Limite di tempo in secondi
        )
        end_time = time.time()
        execution_time = end_time - start_time
        return result.stdout, result.stderr, result.returncode, execution_time
    except subprocess.TimeoutExpired:
        return "", "Il processo ha superato il limite di tempo.", 1, time_limit

def process_directory(model_path, input_dir, output_dir, time_limit):
    # Crea la cartella di output se non esiste
    os.makedirs(output_dir, exist_ok=True)

    print(f"Model path: {model_path}")
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")

    # Itera su tutti i file di input nella cartella specificata
    for filename in os.listdir(input_dir):
        if filename.endswith(".lp"):
            input_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_output.txt")

            print(f"Processing file: {filename}")
            print(f"Input path: {input_path}")
            print(f"Output file path: {output_file_path}")

            # Esegui Clingo con un limite di tempo specificato
            output_clingo, error_clingo, return_code_clingo, exec_time_clingo = run_clingo(model_path, input_path, time_limit)

            # Salva i risultati nel file di output
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(f"Input file: {filename}\n")
                f.write("Input data:\n")
                with open(input_path, "r") as input_file:
                    f.write(input_file.read())
                f.write("\nOutput Clingo:\n")

                # Controlla l'output di Clingo
                if "unsatisfiable" in output_clingo.lower():
                    f.write("Il problema non è soddisfacibile con Clingo.\n")
                else:
                    f.write(output_clingo)

                f.write(f"\nTempo di esecuzione Clingo: {exec_time_clingo:.2f} secondi\n")
                if error_clingo:
                    f.write("\nErrors Clingo:\n")
                    f.write(error_clingo)

            print(f"Processed {filename} - output saved to {output_file_path}")

    print(f"All files in directory {input_dir} processed.")

def main():
    # Ottenere la directory corrente
    current_dir = os.getcwd()

    # Percorso del modello
    model_path = os.path.join(current_dir, "implASP.lp")

    # Directory di input e output per ciascuna difficoltà
    difficulties = ["easy", "medium", "hard"]
    time_limit = 300  # Limite di tempo in secondi (5 minuti)

    for difficulty in difficulties:
        input_dir = os.path.join(current_dir, "instancesClingo", difficulty)
        output_dir = os.path.join(current_dir, f"output_clingo_{difficulty}")
        process_directory(model_path, input_dir, output_dir, time_limit)

if __name__ == "__main__":
    main()
