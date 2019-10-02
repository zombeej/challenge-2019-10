const USERNAME = 'cork'
      LANGUAGE = 'Node'
      NOTES = 'move regex to global scope'

const fs = require('fs')
      path = require('path')
      readline = require('readline')

const dataPath = path.join(__dirname, '..', 'data')
      INPUT = process.argv[2] || null
      invalidCharRegex = RegExp(`[^${INPUT}]`)

const readJSONFile = path => {
  const data = fs.readFileSync(path)
  return JSON.parse(data)
}

const scoreWord = word => {
  let score = word.split('')
    .map(letter => {
      return lettersDict[letter].score
    })
    .reduce((a, b) => {
      return a + b
    })

  if (score > topScoringWord.score) {
    topScoringWord = { score: score, word: word }
  }
}

const writeOutput = () => {
  const END_TIME = process.hrtime.bigint()
  const EXECUTION_TIME = parseInt(END_TIME - START_TIME) / 1000000

  const OUTPUTS = [
    USERNAME,
    LANGUAGE,
    topScoringWord.word,
    topScoringWord.score,
    EXECUTION_TIME,
    NOTES]

  console.log(OUTPUTS.join(', '))
}

const START_TIME = process.hrtime.bigint()

let topScoringWord = { score: 0, word: null }

// Synchronous fileRead - is blocking
const lettersDict = readJSONFile(dataPath + '/letters.json')

const inputStream = fs.createReadStream(dataPath + '/dictionary.txt')
      reader = readline.createInterface({
        input: inputStream,
      })

const isInvalidWord = word => {
  return invalidCharRegex.test(word)
}

const isTooLongWord = word => {
  return word.length > INPUT.length
}

const getLetterCount = str => {
  return str.split('').reduce((acc, letter) => {
    acc[letter] = acc[letter] + 1 || 1
    return acc
  }, {})
}

const isTooManyLetters = word => {
  const maxCount = getLetterCount(INPUT)
  const letterCount = getLetterCount(word)
  const letters = Object.keys(letterCount)

  for (let i = 0; i < letters.length; i++) {
    const letter = letters[i]
    if (letterCount[letter] > maxCount[letter]) {
      return true
    }
  }
  return false
}

reader.on('line', line => {
  if (isTooLongWord(line)) { return }
  if (isInvalidWord(line)) { return }
  if (isTooManyLetters(line)) { return }

  scoreWord(line)
})

reader.on('close', () => {
  writeOutput()
})
