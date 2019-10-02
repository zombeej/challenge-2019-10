'use strict'

const readline = require('readline')
const fs = require('fs')

const LETTERS = process.argv[2].split('')
const VALUES = require('../data/letters')
const WORDS = '../data/dictionary.txt'

// console.log(LETTERS, VALUES)

const START = Date.now()

const readInterface = readline.createInterface({
  input: fs.createReadStream(WORDS),
  console: false
})

let bestword = ['', 0]
// let numwords = 0

function checkWord (word) {
  let ck = [...LETTERS]
  let wd = word.split('')
  let total = 0
  let w = 0
  for (w; w < word.length; w++) {
    const l = word[w]
    const i = ck.indexOf(l)
    if (i > -1) {
      // console.log(word, l, i, ck.length, ck)
      ck.splice(i, 1)
      total = total + VALUES[l].score 
    } else {
      break
    }
  }
  
  if (word.length - w > 0) {
    return false
  }
  // console.log(word)
  if (total > bestword[1]) {
    bestword = [word, total]
  }
}

readInterface.on('line', line => {
  if (line.length <= LETTERS.length) {
    // numwords ++
    checkWord(line)
  }
})

readInterface.on('close', () => {
  const time = Date.now() - START
  // console.log('checked words:', numwords)
  // console.log('found', bestword)
  // console.log(time)
  console.log(`zombeej, Node, ${bestword[0]}, ${bestword[1]}, ${time}, hoooo doggy`)
})
