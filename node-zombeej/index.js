const readline = require('readline')
const fs = require('fs')

const LETTERS = process.argv[2].split('')
const VALUES = require('../data/letters')
const WORDS = '../data/dictionary.txt'
const ALPHA = 'abcdefghijklmnopqrstuvwxyz'.split('')

const START = process.hrtime()

const readInterface = readline.createInterface({
  input: fs.createReadStream(WORDS, {flags: 'r'}),
  console: false
})

const lastletter = LETTERS.reduce((agg, l) => {
  return Math.max(agg, ALPHA.indexOf(l))
}, 0)

// console.log('last letter is', lastletter, ALPHA[lastletter])

let bestword = ['', 0]
let skipper = ''
let found = false

function checkWord (word) {
  let ck = [...LETTERS]
  let total = 0
  let w = 0
  for (w; w < word.length; w++) {
    const l = word[w]
    const i = ck.indexOf(l)
    if (i < 0) {
      if (w === 0) { skipper = l }
      return
    } else {
      ck.splice(i, 1)
      total = total + VALUES[l].score 
    }
  }
  
  if (word.length - w > 0) {
    return false
  }
  if (total > bestword[1]) {
    bestword = [word, total]
  }
}

readInterface.on('line', line => {
  if (found) { return }
  if (line.length > LETTERS.length) { return }
  if (line[0] === skipper) {
    return
  }
  if (ALPHA.indexOf(line[0]) > lastletter) {
    found = true
    printResult()
    readInterface.close()
    return
  }
  checkWord(line)
})

readInterface.on('close', () => {
  if (found) { return }
  printResult()
})

function  printResult () {
  const time = process.hrtime(START)
  console.log(`zombeej, Node, ${bestword[0]}, ${bestword[1]}, ${time[1] / 1000000}, aannngggeerrrr`)
}
