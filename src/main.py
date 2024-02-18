import json
from loader import load_from_json, load_from_regex
from automaton import DFA, NFA

def main():
    automaton_in_memory = None

    while True:
        command = input(">> ").strip().split()

        if command[0] == "load":
            if command[1] == "--input=file":
                with open(command[2]) as file:
                    data = json.load(file)
                    automaton_in_memory = load_from_json(data)
            else:
                print("Invalid load command.")
        elif command[0] == "process":
            if automaton_in_memory:
                input_string = command[1]

                # Check if --verbose is provided in the command
                verbose = "--verbose" in command

                if verbose:
                    if isinstance(automaton_in_memory, DFA):
                        result, message, path = automaton_in_memory.process_string(input_string, verbose=True)
                        print(f"{result} {message}")
                        for step in path:
                            print(f"{step[0]} --({step[1]})--> {step[2]}")
                    elif isinstance(automaton_in_memory, NFA):
                        result, message, path = automaton_in_memory.process_string(input_string, automaton_in_memory.start_state, verbose=True)
                        print(f"{result} {message}")
                        for step in path:
                            print(f"{step[0]} --({step[1]})--> {step[2]}")
                else:
                    if isinstance(automaton_in_memory, DFA):
                        result, message = automaton_in_memory.process_string(input_string)
                    elif isinstance(automaton_in_memory, NFA):
                        result, message = automaton_in_memory.process_string(input_string, automaton_in_memory.start_state)
                    print(f"{result} {message}")
            else:
                print("No automaton loaded.")
        elif command[0] == "regex":
            automaton_in_memory = load_from_regex(command[2])
            print("Loaded DFA from Regular Expression.")
        elif command[0] == "print":
            if automaton_in_memory:
                automaton_in_memory.print_fa()
            else:
                print("No automaton loaded.")
        elif command[0] == "exit":
            break
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
