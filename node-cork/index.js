const USERNAME = 'cork'
      LANGUAGE = 'Node'
      NOTES = 'Put some FP and async on it'

const fs = require('fs')
      util = require('util')
      path = require('path')
      readline = require('readline')
      readFile = util.promisify(fs.readFile)

const dataPath = path.join(__dirname, '..', 'data')
      INPUT = process.argv[2] || null

const readJSONFile = async filePath => {
  const data = await readFile(filePath)
  return JSON.parse(data)
}

const getLetterCount = str => {
  return str.split('').reduce((acc, letter) => {
    acc[letter] = acc[letter] + 1 || 1
    return acc
  }, {})
}

const isTooManyLetters = (word, input) => {
  const maxCount = getLetterCount(input)
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

const scoreWord = (word, dict, minScore) => {
  let score = word.split('')
    .map(letter => {
      return dict[letter].score
    })
    .reduce((a, b) => {
      return a + b
    })

  return { score: score, word: word }
}

const writeOutput = (winner) => {
  const END_TIME = process.hrtime.bigint()
  const EXECUTION_TIME = parseInt(END_TIME - START_TIME) / 1000000

  const OUTPUTS = [
    USERNAME,
    LANGUAGE,
    winner.word,
    winner.score,
    EXECUTION_TIME,
    NOTES]

  console.log(OUTPUTS.join(', '))
}

const getBestWord = async inputLetters => {
  const inputStream = fs.createReadStream(dataPath + '/dictionary.txt')
        reader = readline.createInterface({ input: inputStream })
        invalidCharRegex = RegExp(`[^${INPUT}]`)

  const lettersDict = await readJSONFile(dataPath + '/letters.json')

  let topWord = { score: 0, word: null }

  reader.on('line', line => {
    if (line.length > inputLetters.length) return
    if (invalidCharRegex.test(line)) return
    if (isTooManyLetters(line, inputLetters)) return

    const contender = scoreWord(line, lettersDict, topWord.score)
    if (contender.score > topWord.score) { topWord = contender }
  })

  reader.on('close', () => {
    writeOutput(topWord)
  })
}

const START_TIME = process.hrtime.bigint()

getBestWord(INPUT)
