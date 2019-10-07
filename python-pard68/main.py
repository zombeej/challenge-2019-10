import string
import sys
from timeit import default_timer as timer
from collections import Counter


# Filthy Globals
scores = (1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10)


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


def contains(word, tiles):
	"""
	Takes two lists of a string.
	First checks if each letter in the word
	is in the tile set. If true then it will
	check each letter in the tile, removing
	it from the word and if at the end the 
	word is a blank list it will return true.
	TBH, it's probably not perfect, but it's
	passed all the tests so far...
	"""
	word = list(word)
	if [x for x in word if x in tiles] == word:
		for c in tiles:
			try:
				word.remove(c)
			except:
				pass
			if word == []:
				return True
	return False


def find_best(tiles, dictionary_path='../data/dictionary.txt'):
	"""
	Takes the input tiles and a path to a dictionary.
	Iterate through the dict file, if the line is not
	longer than the tiles, and the line's possible score
	is not less than the current score it checks if the
	tiles can create the word on the line.
	If so this is the new best word. If this word's score
	is the maximum possible score given the tiles, return
	else keep walking through the file
	"""
	values = get_values()
	best = 'a'
	best_score = 0
	max_length = len(tiles)
	tiles_comp = list(tiles)
	max_score = tally(tiles, values)
	with open(dictionary_path, 'r') as f:
		for line in f:
			if len(line) <= max_length + 1:
				word = line.strip()
				if tally(word, values) > best_score:
					if contains(list(word), tiles_comp):
						best = word
						best_score = tally(best, values)
						if best_score == max_score:
							return best, best_score
	return best, best_score


if __name__ == "__main__":
	"""
	Does the stuff
	"""

	# start the timer!
	start = timer()

	# setup
	word = sys.argv[1]

	# DO IT!
	word, value = find_best(word)

	# end the timer and return the results
	end = timer()
	print(f"pard68, Python3, {word}, {value}, {(end - start) * 1000}, snek can snek into snek")
