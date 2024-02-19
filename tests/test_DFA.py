import pytest
import os
import sys
from io import StringIO
from contextlib import redirect_stdout

# Agregamos el directorio src al path para importar el módulo DFA
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

# Importamos la clase DFA del módulo automaton
from automaton import DFA, Automaton

def test_dfa_construction():
    dfa = DFA()
    assert isinstance(dfa, DFA)
    assert isinstance(dfa, Automaton)
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
    assert isinstance(dfa, Automaton)
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

def test_verbose_mode():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    assert dfa.process_string("a", verbose=True) == ("ACCEPT", "String accepted", [("q0", "a", "q1")])

def test_process_string_verbose_false():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    assert dfa.process_string("a", verbose=False) == ("ACCEPT", "String accepted")

def test_process_string_with_path():
    dfa = DFA()
    dfa.add_state("q0")
    dfa.add_state("q1")
    dfa.set_start_state("q0")
    dfa.set_accept_states(["q1"])
    dfa.add_transition("q0", "a", "q1")
    dfa.add_transition("q1", "b", "q0")

    # Modo verbose
    result, message, path = dfa.process_string("ab", verbose=True)
    assert result == "REJECT"
    assert message == "String rejected"
    assert path == [("q0", "a", "q1"), ("q1", "b", "q0")]

    # Modo no verbose
    result, message = dfa.process_string("ab", verbose=False)
    assert result == "REJECT"
    assert message == "String rejected"


if __name__ == "__main__":
    pytest.main()
