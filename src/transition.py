class Transition:
    def __init__(self, state, input_symbol, next_state):
        self.state = state
        self.input_symbol = input_symbol
        self.next_state = next_state