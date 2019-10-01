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
NOTES = 'inefficient'
DATA = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'data')

# def get_random_letters():
#     letters = LETTERS
#     word_length = random.randint(4, 10)
#     word = ''

#     while len(word) < word_length:
#         l = random.choice(ascii_lowercase)
#         if letters[l]['occurrence'] > 0:
#             word += l
#             letters[l]['occurrence'] -= 1

#     vowel_check = [l for l in 'aeiouy' if l in word]
#     if not vowel_check:
#         return get_random_letters()
#     else:
#         return word

# check input
if len(sys.argv) > 1:
    input_letters = sys.argv[1]
else:
    # input_letters = get_random_letters()
    input_letters = ''

# start timer
start = time() * 1000

# load data
with open(os.path.join(DATA, 'dictionary.txt')) as f:
    WORDS = [w.strip() for w in f.readlines()
             if len(w.strip()) <= len(input_letters)]

with open(os.path.join(DATA, 'letters.json'))as f:
    LETTERS = json.load(f)


def get_score(w):
    return sum(LETTERS.get(l, {}).get('score', 0) for l in w)


words = sorted(
    [
        (''.join(w), get_score(w))
        for w in
        filter(
            lambda x: ''.join(x) in WORDS,
            chain(
                *map(
                    lambda l: permutations(input_letters, l),
                    range(1, len(input_letters) + 1)
                )
            )
        )
    ],
    key=lambda k: k[1],
    reverse=True
)
if words:
    winner = words[0][0]
    score = words[0][1]
else:
    winner = ''
    score = 0

duration = (time() * 1000) - start

print(f'{USER}, {LANG}, {winner}, {score}, {duration}, {NOTES}')
