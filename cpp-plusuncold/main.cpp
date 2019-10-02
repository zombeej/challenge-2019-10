#include <iostream>
#include <cmath>
#include <sstream>
#include <limits>
#include <cstdlib>
#include <ctime>
#include <string>
#include <set>
#include <vector>

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

void getDictionaryFromFile() {
    //auto id_read = Timer::timerBegin();
    vector<string> dictVector;
    FILE* file = fopen("../data/dictionary.txt","r");
    char buf[50];
    while(fgets(buf, sizeof buf, file) != NULL) {
	string word(buf);
	word.pop_back();
	dictVector.push_back(word);
    }
    //auto time_read = Timer::timerEnd(id_read);
    //auto id_put = Timer::timerBegin();

    dictionary.insert(dictVector.begin(), dictVector.end());
    //auto time_put_in_dictionary = Timer::timerEnd(id_put);
    //cout << "id read " << time_read << " id put " << time_put_in_dictionary << endl; exit(0);
}

int main(int argc, char* argv[]) {
    auto id = Timer::timerBegin();
    string bestWord;
    string currentGuess;
    short bestScore = 0;
    string letters(argv[1]);
    getDictionaryFromFile();

    combinationsNR(currentGuess, letters, bestWord, bestScore);

    auto time = Timer::timerEnd(id);
    cout << "plusuncold, C++, " << bestWord << ", " << bestScore << ", "
	      << time / 1000 << "," << endl;
    return 0;
}
