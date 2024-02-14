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
    prev = ''

    # DFA
    automaton = DFA()
    automaton.add_state("q0")
    for index, symbol in enumerate(regex):
        if symbol not in regex_symbols:

            if not symbol.isalnum():
                print("Unrecognized symbol in regular expression.")
                return
            
            # Add current symbol to alphabet
            alphabet.add(symbol)

            automaton.set_start_state("q0")

            prev = symbol
            print(symbol)

        else:
            print(symbol)
            match (symbol):
                case '*':
                    print(prev)
                    automaton.add_transition("q0", prev, "q0")
                    continue
                case '+':
                    continue
                case '?':
                    continue
                case '^':
                    continue
                case '$':
                    continue
                case '(':
                    continue
                case _:
                    print("Symbol not in regex dictionary")
                    return
        automaton.set_accept_states("q0")

    return automaton
