# test_loader.py
import os
import sys

src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
sys.path.insert(0, src_dir)

import pytest
from loader import load_from_json, load_from_regex
from automaton import DFA, NFA

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

    regex = "^J0129"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q5"}
    assert automaton.process_string("J0129") == ("ACCEPT", "String accepted")
    assert automaton.process_string("9J120") == ("REJECT", "No transition for '9' in state 'q0'")
    assert automaton.process_string("J1209") == ("REJECT", "No transition for '1' in state 'q1'")

    regex = "FAE4$"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q4"}
    assert automaton.process_string("FAE4") == ("ACCEPT", "String accepted")
    assert automaton.process_string("FAE") == ("REJECT", "String rejected")
    assert automaton.process_string("FAEFAE4") == ("REJECT", "No transition for 'F' in state 'q3'")


    regex = "0*(1234)*ABCD"
    automaton = load_from_regex(regex)
    assert isinstance(automaton, DFA)
    assert automaton.start_state == "q0"
    assert automaton.accept_states == {"q8"}
    assert automaton.process_string("000012341234ABCD") == ("ACCEPT", "String accepted")
    assert automaton.process_string("1234ABCD") == ("ACCEPT", "String accepted")
    assert automaton.process_string("ABCD") == ("ACCEPT", "String accepted")


if __name__ == "__main__":
    pytest.main() 
