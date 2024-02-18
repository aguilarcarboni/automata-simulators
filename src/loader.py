# loader.py
import re
from automaton import DFA, NFA

def load_from_json(json_data):

    # Use json to determine if machine is DFA or NFA
    alphabet = set(json_data.get("alphabet", []))
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
    automaton.alphabet = alphabet
    return automaton

def load_from_regex(regex):
    regex_symbols = ['*', '+', '?', '^', '$', '(',')']

    alphabet = set()
    previousSymbol = str()

    # DFA
    automaton = DFA()

    current_state = 0
    automaton.add_state("q0")
    automaton.set_start_state("q0")

    for index, symbol in enumerate(regex):

        if symbol not in regex_symbols:
            if not symbol.isalnum():
                print("Unrecognized symbol in regular expression.")
                return
            
            # Keep track of symbol
            previousSymbol = symbol
            
            if symbol not in alphabet:
                alphabet.add(symbol)

                # Skip adding transition if current symbol will be modified by regex
                if index < len(regex) - 1 and regex[index + 1] in regex_symbols:
                    continue
                
                # Create transition between states that handles new symbol
                automaton.add_state(f"q{current_state}")
                automaton.add_state(f"q{current_state + 1}")
                automaton.add_transition(f"q{current_state}", symbol, f"q{current_state + 1}")
                current_state += 1

        else:
            match (symbol):
                case '*':
                    
                    automaton.add_transition(f"q{current_state}", previousSymbol, f"q{current_state}")

                case '+':

                    # Add transition from current state to next state to ensure symbol is typed at least once
                    automaton.add_state(f"q{current_state + 1}")
                    automaton.add_transition(f"q{current_state}", previousSymbol, f"q{current_state + 1}")
                    current_state+=1

                    # Add transition to same state to ensure it can be written 1+ times
                    automaton.add_transition(f"q{current_state}", previousSymbol, f"q{current_state}")

                case '?':

                    # Add transition from current state to new state that covers case where symbol appears
                    automaton.add_state(f"q{current_state + len(regex)}")
                    automaton.add_transition(f"q{current_state}", previousSymbol, f"q{current_state + len(regex)}")

                    # Check if there is another symbol next to this expression
                    if index + 1 < len(regex) - 1:

                        # Add transition from new state to the next state in order
                        automaton.add_transition(f"q{current_state + len(regex)}", regex[index + 1], f"q{current_state + 1}")

                case '(':
                    if index < len(regex) - 4 and regex[index + 4] == ')':
                        print("Lol")
                    continue
                case _:
                    print("Symbol", symbol, "not in regex dictionary")
                    return None
    automaton.set_accept_states([f"q{current_state}"])
    automaton.alphabet = alphabet
    return automaton
