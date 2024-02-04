# loader.py
import json
import re
from automaton import DFA, NFA

def load_from_json(json_data):
    alphabet = json_data.get("alphabet", [])
    has_epsilon = "<EPSILON>" in alphabet
    automaton_type = "NFA" if has_epsilon else "DFA"
    print(f"Loading {automaton_type} from JSON...")

    automaton = NFA() if has_epsilon else DFA()

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
    automaton = NFA()  # Assuming all regexes result in NFAs

    # Your regex to NFA conversion logic here

    return automaton