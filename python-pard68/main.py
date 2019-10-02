import string
import sys
from timeit import default_timer as timer
from collections import Counter


# Filthy Globals
scores = (1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10)


def get_dict(dictionary='../data/dictionary.txt', length=100):
	"""
	Takes a string referencing the location of a text file
	Optionally takes the length of the letters we're finding a word for
	Reads that file line by line into a set, removing whitespace
	"""

	with open(dictionary, 'r') as f:
		words = set()
		for line in f:
			if len(line) <= length + 1:
				words.add(line.strip())
	return words


def get_values(scores=scores):
	"""
	Zips alphabet with scores and returns as a dict
	where the key is the letter and the score is the value
	"""

	return dict(zip(string.ascii_lowercase, scores))


def tally(word, values):
	"""
	Takes a string and a dictionary of scrabble letter vlaues
	Returns the same of each char's value in the string
	"""

	return sum([values[x] for x in word])


def find_words(tiles, dictionary):
	tiles = Counter(tiles)
	valid_words = []
	for word in dictionary:
		if len(tiles) >= len(word) and not (Counter(word) - tiles):
			valid_words.append(word)
	return valid_words


def get_highest_scoring(candidates):
	return sorted(candidates.items(), key=lambda kv: kv[1])[-1]


if __name__ == "__main__":
	"""
	Does the stuff
	"""

	# start the timer!
	start = timer()

	# setup
	word = sys.argv[1]
	print(len(word))
	dictionary = get_dict(length=len(word))
	values = get_values()

	# DO IT!
	candidates = {word:tally(word, values) for word in find_words(word, dictionary)}
	word, value = get_highest_scoring(candidates)

	# end the timer and return the results
	end = timer()
	print(f"pard68, Python3, {word}, {value}, {(end - start) * 1000}, gotta eat your yeeties!")
