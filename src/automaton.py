class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

class Automaton:
    def __init__(self):
        self.states = {}
        self.alphabet = set()
        self.start_state = None
        self.accept_states = set()

    def add_state(self, name):
        if name not in self.states:
            self.states[name] = State(name)

    def add_transition(self, current_state, input_symbol, next_state):
        self.states[current_state].transitions[input_symbol] = next_state
        self.alphabet.add(input_symbol)

    def set_start_state(self, start_state):
        self.start_state = start_state

    def set_accept_states(self, accept_states):
        self.accept_states = set(accept_states)

class DFA(Automaton):
    def process_string(self, input_string, verbose = False):
        current_state = self.start_state

        # Track the path for verbose mode
        path = []

        # Check symbol by symbol ensuring each is in the alphabet and has a next state
        for symbol in input_string:
            if symbol not in self.alphabet:
                return "REJECT", f"Invalid symbol '{symbol}'"

            next_state = self.states[current_state].transitions.get(symbol)
            if next_state is None:
                return "REJECT", f"No transition for '{symbol}' in state '{current_state}'"

            path.append((current_state, symbol, next_state))
            current_state = next_state

        # Check if current state is final state and finish process
        if current_state in self.accept_states:

            ###
            # Verbose no sirve
            ###
            if verbose:
                return "ACCEPT", "String accepted"
            else:
                return "ACCEPT", "String accepted"
        else:
            return "REJECT", "String rejected"


class NFA(Automaton):
    def __init__(self):
        super().__init__()

    def add_transition(self, current_state, input_symbol, next_state):
        transition = NFATransition(current_state, input_symbol, next_state)
        if current_state not in self.states:
            self.states[current_state] = State(current_state)

        if input_symbol == "<EPSILON>":
            if "epsilon_transitions" not in self.states[current_state].transitions:
                self.states[current_state].transitions["epsilon_transitions"] = []
            self.states[current_state].transitions["epsilon_transitions"].append(next_state)
        else:
            if "transitions" not in self.states[current_state].transitions:
                self.states[current_state].transitions["transitions"] = []
            self.states[current_state].transitions["transitions"].append(transition)

    def process_string(self, input_string, current_state, verbose=False, path=None):
        # Track the path for verbose mode
        if path is None:
            path = []

        if not input_string:
            if current_state in self.accept_states:
                if verbose:
                    return "ACCEPT", "String accepted", path
                else:
                    return "ACCEPT", "String accepted"
            else:
                return "REJECT", "String rejected"

        symbol = input_string[0]
        remaining_input = input_string[1:]

        if current_state not in self.states:
            return "REJECT", f"Invalid state '{current_state}'"

        transitions = self.states[current_state].transitions.get("transitions", [])
        epsilon_transitions = self.states[current_state].transitions.get("epsilon_transitions", [])

        for transition in transitions:
            if transition.input_symbol == symbol:
                new_path = path + [(current_state, symbol, transition.next_state)]
                result, message = self.process_string(remaining_input, transition.next_state, verbose, new_path)
                if result == "ACCEPT":
                    return result, message

        for next_state in epsilon_transitions:
            new_path = path + [(current_state, "<EPSILON>", next_state)]
            result, message = self.process_string(input_string, next_state, verbose, new_path)
            if result == "ACCEPT":
                return result, message

        return "REJECT", f"No transition for '{symbol}' in state '{current_state}'"

class NFATransition:
    def __init__(self, state, input_symbol, next_state):
        self.state = state
        self.input_symbol = input_symbol
        self.next_state = next_state