#include <iostream>
#include <cmath>
#include <sstream>
#include <limits>
#include <cstdlib>
#include <ctime>
#include <string>
#include <set>
#include <vector>
#include <fstream>
#include <map>
#include <tuple>

#include "timer.h"

using namespace std;

const short letterValues[] = { 1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10 };
static set<string> dictionary;

short valueForLetter(char letter) {
    short diff = (short)letter - (short)'a';
    return letterValues[diff];
}

short scoreForVector(const string& vec) {
    short score = 0;
    
    for (const char c : vec) {
	score += valueForLetter(c);
    }

    return score;
}

bool wordInDictionary(const string& word) {
    return dictionary.count(word);
}

void combinationsNR(string& soFar,
                    string& remaining,
		    string& bestWord,
		    short& bestScore) {
    short score = scoreForVector(soFar);
    if (score > bestScore) {
	if (wordInDictionary(soFar)) {
	    bestScore = score;
	    bestWord = soFar;
	}
    }
    
    for (short i = 0 ; i < remaining.size() ; i++) {
	soFar.push_back(remaining[i]);
	string remainingWithoutI(remaining);
	remainingWithoutI.erase(remainingWithoutI.begin()+i);
	combinationsNR(soFar, remainingWithoutI, bestWord, bestScore);
	soFar.pop_back();
    }
    
}

map<char,short> lettersToMap(char* letters) {
    short i = 0;
    map<char,short> lettersMap;
    char letter = letters[i];;
    while (letter != NULL) {
	if (lettersMap.count(letter)) {
	    lettersMap[letter]++;
	} else {
	    lettersMap[letter] = 1;
	}
	i++;
	letter = letters[i];
    }
    return lettersMap;
}

bool lettersCanMadeWordWithoutCardinality(const string& word,
					  map<char,short>& letters) {
    for (int i = 0 ; i < word.size() ; i++) {
	if (!letters.count(word[i])) {
	    return false;
	}
    }
    return true;
}

bool lettersCanMadeWordWithCardinality(string word,
				       map<char,short>& letters) {
    map<char,short> occurrences;
    for (int i = 0 ; i < word.size() ; i++) {
	if (occurrences.count(word[i])) {
	    occurrences[word[i]]++;
	} else {
	    occurrences[word[i]] = 1;
	}
    }

    for (const auto letterOccurrence : occurrences) {
	short occurrence = letterOccurrence.second;
	if (occurrence == 1) {
	    continue;
	}
	char letter = letterOccurrence.first;

	if (letters[letter] < occurrence) {
	    return false;
	}
    }

    return true;
}


tuple<string,short> getDictionaryFromFile(map<char,short> letters) {
    //auto id_read = Timer::timerBegin();
    short maxWordLength = 0;
    for (const auto& l : letters) {
	maxWordLength += l.second;
    }
    vector<string> dictVector;
    std::ifstream file;
    file.open("../data/dictionary.txt");

    string word, bestWord;
    short score, bestScore = 0;
    while(getline(file,word)) {
	if (word.size() > maxWordLength) { // Word isn't useful if it's over the max word length
	    continue;
	}
	score = scoreForVector(word);
	//cout << word << " " << score << " " << bestScore << endl;
	if (score > bestScore) {
	    if (lettersCanMadeWordWithoutCardinality(word, letters)) {
		if (lettersCanMadeWordWithCardinality(word, letters)) {
		    //if (score == maxPossibleScore) { // i.e. if all the letters are used
		    //	return {word, score};
		    //}
		    bestWord = word;
		    bestScore = score;
		}
	    }
	}
    }
    
    //auto time_read = Timer::timerEnd(id_read);
    //auto id_put = Timer::timerBegin();

    //auto time_put_in_dictionary = Timer::timerEnd(id_put);
    //cout << "id read " << time_read << " id put " << time_put_in_dictionary << endl; exit(0);

    return {bestWord, bestScore};
}

int main(int argc, char* argv[]) {
    auto id = Timer::timerBegin();
    string bestWord; short bestScore;
    tie(bestWord, bestScore) = getDictionaryFromFile(lettersToMap(argv[1]));
    auto time = Timer::timerEnd(id);
    cout << "plusuncold, C++, " << bestWord << ", " << bestScore << ", "
	      << time / 1000 << "," << endl;
    return 0;
}
