import subprocess
import sys


with open('../benchmark/command-line.txt', 'r') as file:

    for line in file:

        command = line.strip()

        if command:
            print(f"Executing command: {command}")
            try:

                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                print(result.stdout.decode())

                if result.stderr:
                    print("Error:", result.stderr.decode(), file=sys.stderr)
            except subprocess.CalledProcessError as e:

                print(f"An error occurred while executing command: {command}", file=sys.stderr)
                print(e, file=sys.stderr)
