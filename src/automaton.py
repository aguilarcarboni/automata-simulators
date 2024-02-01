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
    def process_string(self, input_string, verbose=False):
        current_state = self.start_state

        path = []  # Track the path for verbose mode

        for symbol in input_string:
            if symbol not in self.alphabet:
                return "REJECT", f"Invalid symbol '{symbol}'"

            next_state = self.states[current_state].transitions.get(symbol)
            if next_state is None:
                return "REJECT", f"No transition for '{symbol}' in state '{current_state}'"

            path.append((current_state, symbol, next_state))
            current_state = next_state

        if current_state in self.accept_states:
            if verbose:
                return "ACCEPT", "String accepted", path
            else:
                return "ACCEPT", "String accepted"
        else:
            return "REJECT", "String rejected"

class NFA(Automaton):
    def process_string(self, input_string, verbose=False):
        current_states = {self.start_state}
        path = []

        for symbol in input_string:
            if symbol not in self.alphabet:
                return "REJECT", f"Invalid symbol '{symbol}'"

            next_states = set()
            for state in current_states:
                next_state = self.states[state].transitions.get(symbol)
                if next_state:
                    next_states.add(next_state)

            if not next_states:
                return "REJECT", f"No transition for '{symbol}' in states {current_states}"

            path.append((current_states, symbol, next_states))
            current_states = next_states

        if any(state in self.accept_states for state in current_states):
            if verbose:
                return "ACCEPT", "String accepted", path
            else:
                return "ACCEPT", "String accepted"
        else:
            return "REJECT", "String rejected"