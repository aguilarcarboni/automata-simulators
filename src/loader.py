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

    # DFA
    automaton = DFA()

    current_state = 0
    automaton.add_state("q0")
    automaton.set_start_state("q0")

    current_state, automaton = parse_regex(regex, current_state, automaton)
    
    automaton.set_accept_states([f"q{current_state}"])
    return automaton


def parse_regex(regex, current_state, automaton):

    regex_symbols = ['*', '+', '?', '^', '$', '(',')']

    alphabet = set()
    previousSymbol = str()

    expression_size = 0

    for index, symbol in enumerate(regex):
        if symbol not in regex_symbols:
            expression_size += 1
            if not symbol.isalnum():
                print("Unrecognized symbol in regular expression.")
                return
            
            # Keep track of symbol
            previousSymbol = symbol
            
            if symbol not in alphabet:
                alphabet.add(symbol)

                # Skip adding transition if current symbol will be modified by regex
                if index < len(regex) - 1 and regex[index + 1] in regex_symbols and (regex[index + 1] != ')' and regex[index + 1] != '('):
                    continue
                
                # Create transition between states that handles new symbol
                automaton.add_state(f"q{current_state}")
                automaton.add_state(f"q{current_state + 1}")
                automaton.add_transition(f"q{current_state}", symbol, f"q{current_state + 1}")
                current_state += 1

        else:
            if previousSymbol:
                match (symbol):
                    case '*':
                        
                        # Add transition loop to same state
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

                    case '$':
                        automaton.add_transition(f"q{current_state}", regex[index - 1], f"q{current_state + 1}")
                        current_state += 1
                    case '^':
                        continue
                    case '(':

                        # Reset expression size counter
                        expression_size = 0

                    case ')':
                        previousSymbol = None

                        # Check if there are any characters after the sub-expression
                        if index < len(regex) - 1:

                            # Check type of regex expression
                            match (regex[index + 1]):
                                case '*':

                                    # Add transition back to state where sub-expression started
                                    automaton.add_transition(f"q{current_state}", regex[index - expression_size], f"q{current_state - expression_size + 1}")

                                    if index < len(regex) - 2:

                                        # Add transition from initial sub-expression state to final sub-expression state
                                        automaton.add_transition(f"q{current_state - expression_size}", regex[index + 2], f"q{current_state + 1}")

                                case '+':

                                    # Add transition back to state where sub-expression started
                                    automaton.add_transition(f"q{current_state}", regex[index - expression_size], f"q{current_state - expression_size + 1}")

                                case '?':

                                    # If there is a symbol after the sub-expresion
                                    if index < len(regex) - 2:

                                        # Add transition from initial state to final state
                                        automaton.add_transition(f"q{current_state - expression_size}", regex[index + 2], f"q{current_state + 1}")
                                    else:
                                        print(current_state - expression_size)
                                        automaton.add_transition(f"q{current_state}", '', f"q{current_state - expression_size}")
                                        current_state = current_state - expression_size
                                case '$':
                                    continue
                                case '^':
                                    continue
                                case _:
                                    print("Symbol", symbol, "not in regex dictionary")
                                    return None
                    case _:
                        print("Symbol", symbol, "not in regex dictionary")
                        return None
            
    return current_state, automaton