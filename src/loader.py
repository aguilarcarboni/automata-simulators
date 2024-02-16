# loader.py
import re
from automaton import DFA, NFA

def load_from_json(json_data):

    # Use json to determine if machine is DFA or NFA
    alphabet = json_data.get("alphabet", [])
    automaton_type = "NFA" if "<EPSILON>" in alphabet else "DFA"
    print(f"Loading {automaton_type} from JSON...")

    # Start building FA
    automaton = NFA() if "<EPSILON>" in alphabet else DFA()

    for state in json_data['states']:
        automaton.add_state(state)
    for transition in json_data['delta']:
        if transition['input'] == "<EPSILON>":
            automaton.add_epsilon_transition(
                transition['state'], transition['next_state']
            )
        else:
            automaton.add_transition(
                transition['state'], transition['input'], transition['next_state']
            )
    automaton.set_start_state(json_data['start_state'])
    automaton.set_accept_states(json_data['accept_states'])
    return automaton

def load_from_regex(regex):
    regex_symbols = ['*', '+', '?', '^', '$', '(',')']

    alphabet = set()
    previousSymbol = str()

    states = ['q0', 'q1', 'q2', 'q3', 'q4']
    current_state = 0

    # DFA
    automaton = DFA()
    for state in states:
        automaton.add_state(state)

    automaton.set_start_state(states[0])

    for index, symbol in enumerate(regex):
        if symbol not in regex_symbols:

            if not symbol.isalnum():
                print("Unrecognized symbol in regular expression.")
                return
            
            if symbol not in alphabet:
                alphabet.add(symbol)
                automaton.add_transition(states[current_state], symbol, states[current_state + 1])
                current_state += 1
            
            # Keep track of symbol
            previousSymbol = symbol

        else:
            #6686989*75546858
            match (symbol):
                case '*':
                    automaton.add_transition(states[current_state], previousSymbol, states[current_state])
                case '+':
                    print(current_state)
                    # Add transition from current state to next state to ensure it is typed at least once
                    automaton.add_transition(states[current_state], previousSymbol, states[current_state + 1])

                    # Go to next state
                    current_state+=1

                    # Add transition to same state to ensure it can be written 1+ times
                    automaton.add_transition(states[current_state], previousSymbol, states[current_state])
                case '?':
                    # Add transition to same state to ensure it can be read
                    automaton.add_transition(states[current_state], previousSymbol, states[current_state])
                case '^':
                    continue
                case '$':
                    continue
                case '(':
                    continue
                case _:
                    print("Symbol", symbol, "not in regex dictionary")
                    return
                
    automaton.set_accept_states([states[current_state]])
    automaton.alphabet = alphabet
    return automaton
