from itertools import chain
from itertools import permutations
import json
import os
# import random
# from string import ascii_lowercase
import sys
from time import time

USER = 'specs'
LANG = 'Python 3'
NOTES = 'strolling down the yeet'
DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')


# check input
if len(sys.argv) > 1:
    input_letters = sys.argv[1]
else:
    input_letters = ''

# start timer
start = time() * 1000

# load data
with open(os.path.join(DATA, 'dictionary.txt')) as f:
    WORDS = {w.strip() for w in f.readlines()
             if len(w.strip()) <= len(input_letters)}

with open(os.path.join(DATA, 'letters.json'))as f:
    LETTERS = json.load(f)


# function to get the score of a string
def get_score(w):
    return sum(LETTERS.get(l, {}).get('score', 0) for l in w)


# valid words and scores comprehension
words = sorted( # sort the words by score descending
    [
        (''.join(w), get_score(w)) # join the letters together and score them
        for w in
        filter( # filter out stuff not in the dictionary
            lambda x: ''.join(x) in WORDS,
            # smash it all together
            chain(
                *map(
                    # get all permutations of input
                    lambda l: permutations(input_letters, l),
                    range(1, len(input_letters) + 1)
                )
            )
        )
    ],
    key=lambda k: k[1],
    reverse=True
)
# if words in the list, the first one is the best one
if words:
    winner = words[0][0]
    score = words[0][1]
# return a wrong answer
else:
    winner = ''
    score = 0

duration = (time() * 1000) - start

print(f'{USER}, {LANG}, {winner}, {score}, {duration}, {NOTES}')
