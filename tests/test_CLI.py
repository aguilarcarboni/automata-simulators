from unittest.mock import patch
from io import StringIO
import json
import pytest
import os
import sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

from loader import load_from_json, load_from_regex
from automaton import DFA, NFA
from main import main

def test_main_load_json_invalid_command():
    with patch("builtins.input", side_effect=["load --input= test.json", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == "Invalid load command."

def test_main_load_json_valid_command():
    # Asegurar que el archivo test.json existe o proporcionar una ruta correcta hacia él
    test_file_path = "test.json"
    with open(test_file_path, "w") as test_file:
        json.dump({
            "alphabet": ["0", "1", "<EPSILON>"],
            "states": ["q0", "q1"],
            "delta": [
                { "state": "q0", "input": "0", "next_state": "q1" },
                { "state": "q0", "input": "1", "next_state": "q0" }
            ],
            "start_state": "q0",
            "accept_states": ["q1"]
        }, test_file)

    with patch("builtins.input", side_effect=["load --input=file test.json", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == "Loading NFA from JSON..."

    # Eliminar el archivo de prueba después de usarlo
    os.remove(test_file_path)

def test_main_process_string_dfa_verbose():
    with patch("builtins.input", side_effect=["load --input=file assets/data.json", "process aa --verbose", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        output_text = output.getvalue()
        assert "ACCEPT String accepted" in output_text
        assert "q0 --(a)--> q1" in output_text
        assert "q1 --(a)--> q1" in output_text

def test_main_process_string_dfa():
    with patch("builtins.input", side_effect=["load --input=file assets/data.json", "process aa", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert "ACCEPT String accepted" in output.getvalue()

def test_main_process_string_nfa_verbose():
    with patch("builtins.input", side_effect=["load --input=file assets/data_nfa.json", "process aε --verbose", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        output_text = output.getvalue()
        assert "ACCEPT String accepted" in output_text
        assert "q0 --(a)--> q1" in output_text
        assert "q1 --(ε)--> q1" in output_text

def test_main_process_string_nfa_verbose_failure():
    with patch("builtins.input", side_effect=["load --input=file assets/data.json", "process ab --verbose", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        output_text = output.getvalue()
        assert "REJECT Invalid symbol 'b'" in output_text
        assert "q0 --(a)--> q1" in output_text


def test_main_process_string_nfa():
    with patch("builtins.input", side_effect=["load --input=file assets/data_nfa.json", "process aε", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert "ACCEPT String accepted" in output.getvalue()

def test_main_process_string_nfa_failure():
    with patch("builtins.input", side_effect=["load --input=file assets/data_nfa.json", "process ε", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert "REJECT No transition for 'ε' in state 'q0'" in output.getvalue()

def test_main_process_string_no_automaton_loaded():
    with patch("builtins.input", side_effect=["process aa", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == "No automaton loaded."

def test_main_regex():
    with patch("builtins.input", side_effect=["regex test a+b?", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == "Loaded DFA from Regular Expression."

def test_main_print_with_automaton_loaded():
    with patch("builtins.input", side_effect=["load --input=file assets/data.json", "print", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert "Alphabet" in output.getvalue()
        assert "States" in output.getvalue()
        assert "Start State" in output.getvalue()
        assert "Accept States" in output.getvalue()

def test_main_print_no_automaton_loaded():
    with patch("builtins.input", side_effect=["print", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == "No automaton loaded."

def test_main_invalid_command():
    with patch("builtins.input", side_effect=["invalid", "exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert "Invalid command" in output.getvalue()

def test_main_exit():
    with patch("builtins.input", side_effect=["exit"]), patch("sys.stdout", new=StringIO()) as output:
        main()
        assert output.getvalue().strip() == ""




def test_load_from_json_DFA_success():
    json_data = {
        "alphabet": ["a", "b"],
        "states": ["q0", "q1"],
        "delta": [
            {"state": "q0", "input": "a", "next_state": "q1"},
            {"state": "q1", "input": "b", "next_state": "q0"}
        ],
        "start_state": "q0",
        "accept_states": ["q1"]
    }
    automaton = load_from_json(json_data)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q1"}
    assert automaton.process_string("a") == ("ACCEPT", "String accepted")

def test_load_from_json_DFA_failure():
    json_data = {
        "alphabet": ["a", "b"],
        "states": ["q0", "q1"],
        "delta": [
            {"state": "q0", "input": "a", "next_state": "q1"},
            {"state": "q1", "input": "b", "next_state": "q0"}
        ],
        "start_state": "q0",
        "accept_states": ["q1"]
    }
    automaton = load_from_json(json_data)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q1"}
    assert automaton.process_string("ab") == ("REJECT", "String rejected")

def test_load_from_json_NFA_success():
    json_data = {
        "alphabet": ["0", "1", "<EPSILON>"],
        "states": ["q0", "q1", "q2"],
        "delta": [
            { "state": "q0", "input": "0", "next_state": "q1" },
            { "state": "q0", "input": "1", "next_state": "q0" },
            { "state": "q0", "input": "ε", "next_state": "q2" },
            { "state": "q1", "input": "0", "next_state": "q2" },
            { "state": "q1", "input": "1", "next_state": "q0" },
            { "state": "q2", "input": "0", "next_state": "q2" },
            { "state": "q2", "input": "1", "next_state": "q2" }
        ],
        "start_state": "q0",
        "accept_states": ["q2"]
    }
    automaton = load_from_json(json_data)
    assert isinstance(automaton, NFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q2"}
    assert automaton.process_string("011ε01", "q0") == ("ACCEPT", "String accepted")

def test_load_from_json_NFA_failure():
    json_data = {
        "alphabet": ["0", "1", "<EPSILON>"],
        "states": ["q0", "q1", "q2"],
        "delta": [
            { "state": "q0", "input": "0", "next_state": "q1" },
            { "state": "q0", "input": "1", "next_state": "q0" },
            { "state": "q0", "input": "ε", "next_state": "q2" },
            { "state": "q1", "input": "0", "next_state": "q2" },
            { "state": "q1", "input": "1", "next_state": "q0" },
            { "state": "q2", "input": "0", "next_state": "q2" },
            { "state": "q2", "input": "1", "next_state": "q2" }
        ],
        "start_state": "q0",
        "accept_states": ["q2"]
    }
    automaton = load_from_json(json_data)
    assert isinstance(automaton, NFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q2"}
    assert automaton.process_string("10ε", "q0") == ("REJECT", "No transition for '1' in state 'q0'")

def test_load_from_regex_():
    regex = "a*"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q0"}
    assert automaton.process_string("aaaa") == ("ACCEPT", "String accepted")
    assert automaton.process_string("") == ("ACCEPT", "String accepted")
    assert automaton.process_string("a9") == ("REJECT", "Invalid symbol '9'")

    regex = "a+b?"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q1"}
    assert automaton.process_string("ab") == ("REJECT", "String rejected") #Deberia ser accepted no?
    assert automaton.process_string("a") == ("ACCEPT", "String accepted")
    assert automaton.process_string("b") == ("REJECT", "No transition for 'b' in state 'q0'")

    regex = "F?1234"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q4"}
    assert automaton.process_string("F1234") == ("ACCEPT", "String accepted")
    assert automaton.process_string("1234") == ("ACCEPT", "String accepted")
    assert automaton.process_string("F") == ("REJECT", "String rejected")

    regex = "346+"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q3"}
    assert automaton.process_string("346") == ("ACCEPT", "String accepted")
    assert automaton.process_string("34") == ("REJECT", "String rejected")
    assert automaton.process_string("3466666") == ("ACCEPT", "String accepted")

    '''
    regex = "^J0129"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q3"}
    assert automaton.process_string("J0129") == ("ACCEPT", "String accepted")
    assert automaton.process_string("9J120") == ("REJECT", "String rejected")
    assert automaton.process_string("J1209") == ("REJECT", "String rejected")
    '''

    '''
    regex = "FAE4$"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q3"}
    assert automaton.process_string("J0129") == ("ACCEPT", "String accepted")
    assert automaton.process_string("9J120") == ("REJECT", "String rejected")
    assert automaton.process_string("J1209") == ("REJECT", "String rejected")
    '''

    '''
    regex = "0*(1234)*ABCD"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q3"}
    assert automaton.process_string("J0129") == ("ACCEPT", "String accepted")
    assert automaton.process_string("9J120") == ("REJECT", "String rejected")
    assert automaton.process_string("J1209") == ("REJECT", "String rejected")
    '''


def test_nfa_construction():
    nfa = NFA()
    assert isinstance(nfa, NFA)
    assert len(nfa.states) == 0
    assert len(nfa.alphabet) == 0
    assert nfa.start_state is None
    assert len(nfa.accept_states) == 0

def test_add_state():
    nfa = NFA()
    nfa.add_state("q0")
    assert "q0" in nfa.states
    assert len(nfa.states) == 1

def test_add_transition():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_transition("q0", "a", "q1")
    assert "a" in nfa.alphabet
    assert nfa.states["q0"].transitions["transitions"][0].next_state == "q1"


def test_add_epsilon_transition():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_transition("q0", "<EPSILON>", "q1")
    assert "q1" in nfa.states["q0"].transitions["epsilon_transitions"]


def test_set_start_state():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.set_start_state("q0")
    assert nfa.start_state == "q0"

def test_set_accept_states():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.set_accept_states(["q1"])
    assert "q1" in nfa.accept_states

def test_process_string_accept():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.set_start_state("q0")
    nfa.set_accept_states(["q1"])
    nfa.add_transition("q0", "a", "q1")
    assert nfa.process_string("a", "q0") == ("ACCEPT", "String accepted")

def test_process_string_reject():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.set_start_state("q0")
    nfa.set_accept_states(["q1"])
    nfa.add_transition("q0", "b", "q1")  # No transition for 'a'
    assert nfa.process_string("a", "q0") == ("REJECT", "No transition for 'a' in state 'q0'")

def test_process_string_empty_string():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.set_start_state("q0")
    nfa.set_accept_states(["q0"]) 
    assert nfa.process_string("", "q0") == ("ACCEPT", "String accepted")

def test_process_string_with_epsilon_transitions_in_between():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_state("q2")
    nfa.add_transition("q0", "<EPSILON>", "q1")
    nfa.add_transition("q1", "a", "q2")
    nfa.set_start_state("q0")
    nfa.set_accept_states(["q2"])  # Acepta desde el estado q2
    assert nfa.process_string("a", "q0") == ("ACCEPT", "String accepted")

def test_process_string_with_multiple_transitions():
    nfa = NFA()
    nfa.add_state("q0")
    nfa.add_state("q1")
    nfa.add_state("q2")
    nfa.add_state("q3")
    nfa.add_transition("q0", "a", "q1")
    nfa.add_transition("q0", "a", "q2")
    nfa.add_transition("q1", "b", "q3")
    nfa.add_transition("q2", "b", "q3")
    nfa.set_start_state("q0")
    nfa.set_accept_states(["q3"])
    assert nfa.process_string("ab", "q0") == ("ACCEPT", "String accepted")


def test_dfa_construction():
    dfa = DFA()
    assert isinstance(dfa, DFA)
    assert len(dfa.states) == 0
    assert len(dfa.alphabet) == 0
    assert dfa.start_state is None
    assert len(dfa.accept_states) == 0

def test_add_state():
    dfa = DFA()
    dfa.add_state("q0")
    assert "q0" in dfa.states
    assert len(dfa.states) == 1

def test_add_transition():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.add_transition("q0", "a", "q1")
    assert "a" in dfa.alphabet
    assert dfa.states["q0"].transitions["a"] == "q1"

def test_set_start_state():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.set_start_state("q0")
    assert dfa.start_state == "q0"

def test_set_accept_states():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_accept_states(["q1"])
    assert "q1" in dfa.accept_states

def test_process_string_accept():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    assert dfa.process_string("a") == ("ACCEPT", "String accepted")

def test_process_string_reject():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "b", "q1")  # No transition for 'a'
    assert dfa.process_string("a") == ("REJECT", "Invalid symbol 'a'")

def test_empty_dfa_construction():
    dfa = DFA()
    assert isinstance(dfa, DFA)
    assert len(dfa.states) == 0
    assert len(dfa.alphabet) == 0
    assert dfa.start_state is None
    assert len(dfa.accept_states) == 0

def test_add_transition_with_epsilon_symbol():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.add_transition("q0", "<EPSILON>", "q1")
    assert "<EPSILON>" in dfa.alphabet
    assert dfa.states["q0"].transitions["<EPSILON>"] == "q1"

def test_process_empty_string():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q0"])  # Acepta desde el estado inicial
    assert dfa.process_string("") == ("ACCEPT", "String accepted")

def test_add_duplicate_state():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q0")  # Intentar agregar un estado duplicado
    assert len(dfa.states) == 1  # Solo debe haber un estado q0

def test_process_string_with_missing_transitions():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    # Falta la transición para el símbolo 'a' desde el estado 'q0' al estado 'q1'
    assert dfa.process_string("a") == ("REJECT", "Invalid symbol 'a'")

def test_process_string_with_circular_transitions():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    dfa.add_transition("q1", "b", "q0")  # Transición circular de 'q1' a 'q0'
    assert dfa.process_string("ab") == ("REJECT", "String rejected")

def test_process_string_with_special_symbols():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "<SPACE>", "q1")  # Transición con símbolo especial "<SPACE>"
    assert dfa.process_string(" ") == ("REJECT", "Invalid symbol ' '")

def test_verbose_mode():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    assert dfa.process_string("a", verbose=True) == ("ACCEPT", "String accepted", [("q0", "a", "q1")])

def test_process_string_with_long_string():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    # Prueba con una cadena muy larga
    long_string = "a" * 10000
    assert dfa.process_string(long_string) == ("REJECT", "No transition for 'a' in state 'q1'")
    
if __name__ == "__main__":
    pytest.main()
