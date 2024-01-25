# prompt: create a finite state automata

import re

# Define the states of the automaton
states = ['q0', 'q1', 'q2']

# Define the alphabet of the automaton
alphabet = ['0', '1']

# Define the transition function
transitions = {
  'q0': {'0': 'q1', '1': 'q2'},
  'q1': {'0': 'q0', '1': 'q1'},
  'q2': {'0': 'q2', '1': 'q0'}
}

# Define the start state
startState = 'q0'

# Define the accepting states
finalStates = ['q2']

# Create the automaton
automaton = (states, alphabet, transitions, startState, finalStates)

# Test the automaton
string = '01010'
currentState = startState
for char in string:
  currentState = transitions[currentState][char]
if currentState in finalStates:
  print('The string is accepted by the automaton.')
else:
  print('The string is not accepted by the automaton.')
