import json
import transition

class FiniteAutomaton:
    def __init__(self):
        self.states = []
        self.alphabet = []
        self.transitions = []
        self.start_state = None
        self.accept_states = []

    def load_from_json(self, json_data):
        
        # Parse JSON data and initialize the Automaton object
        data = json.loads(json_data)
        self.states = data["states"]
        self.alphabet = data["alphabet"]
        self.start_state = data["start_state"]
        self.accept_states = data["accept_states"]

        # Load transitions from delta function declaration
        self.transitions = [transition.Transition(t["state"], t["input"], t["next_state"]) for t in data["delta"]]

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