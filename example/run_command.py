import subprocess
import signal

TIMEOUT = 120

def execute_command(command):
    try:

        process = subprocess.Popen(command, shell=True)

        process.wait(timeout=TIMEOUT)
    except subprocess.TimeoutExpired:

        process.kill()

        process.communicate()
        print("fail")
    except Exception as e:

        print(f"An error occurred: {e}")

def main():

    with open('../benchmark/command-line.txt', 'r') as file:
        commands = file.readlines()


    for command in commands:
        command = command.strip()
        if command:
            print(f"Executing: {command}")
            execute_command(command)

if __name__ == "__main__":
    main()
