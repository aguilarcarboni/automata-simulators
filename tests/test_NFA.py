import pytest
import os
import sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

from automaton import NFA

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


if __name__ == "__main__":
    pytest.main()
