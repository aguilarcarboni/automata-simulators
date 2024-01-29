import json
import re

class Transition:
    def __init__(self, state, input_symbol, next_state):
        self.state = state
        self.input_symbol = input_symbol
        self.next_state = next_state

class FiniteAutomaton:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.start_state = None
        self.accept_states = []

    def load_from_json(self, json_data):
        # Parse JSON data and initialize the FA object
        data = json.loads(json_data)
        self.states = data["states"]
        self.alphabet = data["alphabet"]
        self.start_state = data["start_state"]
        self.accept_states = data["accept_states"]
        self.transitions = [Transition(t["state"], t["input"], t["next_state"]) for t in data["delta"]]

    def is_accepted(self, input_string):
        # Check if the input string is accepted by the FA
        current_state = self.start_state

        for symbol in input_string:
            next_state = self.get_next_state(current_state, symbol)
            if next_state is None:
                return False
            current_state = next_state

        return current_state in self.accept_states

    def get_next_state(self, current_state, input_symbol):
        # Get the next state based on the current state and input symbol
        for transition in self.transitions:
            if transition.state == current_state and transition.input_symbol == input_symbol:
                return transition.next_state
        return None

    def print_fa(self):
        # Print the FA details
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Transitions:")
        for transition in self.transitions:
            print(f"  {transition.state} --({transition.input_symbol})--> {transition.next_state}")
        print("Start State:", self.start_state)
        print("Accept States:", self.accept_states)


class RegexAutomaton(FiniteAutomaton):
    def build_from_regex(self, regex):
        # Build an automaton from a subset of regex
        # Implement this method to handle regex operations

        pass

# CLI Interface
def main():
    automaton = None

    while True:
        command = input(">> ").split()
        if command[0] == "load" and len(command) == 3 and command[1] == "--input":
            with open(command[2], "r") as file:
                json_data = file.read()
                automaton = FiniteAutomaton()
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
            automaton = RegexAutomaton()
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
