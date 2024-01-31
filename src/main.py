import regex_processing as regex_processing
import automaton as automata

# CLI Interface
def main():
    automaton = None

    while True:
        command = input(">> ").split()
        if command[0] == "load" and len(command) == 3 and command[1] == "--input":
            with open(command[2], "r") as file:
                json_data = file.read()
                automaton = automata.FiniteAutomaton()
                automaton.load_from_json(json_data)
                print("Automaton loaded successfully.")
        elif command[0] == "process" and len(command) == 3 and command[1] == "--input":
            if automaton:
                result = automaton.is_accepted(command[2])
                if result:
                    print("ACCEPT")
                else:
                    print("REJECT")
            else:
                print("Error: Automaton not loaded.")
        elif command[0] == "regex" and len(command) == 3 and command[1] == "--input":
            automaton = regex_processing.RegexAutomaton()
            automaton.build_from_regex(command[2])
            print("Automaton built from regex.")
        elif command[0] == "print" and len(command) == 1:
            if automaton:
                automaton.print_fa()
            else:
                print("Error: Automaton not loaded.")
        elif command[0] == "exit" and len(command) == 1:
            break
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
