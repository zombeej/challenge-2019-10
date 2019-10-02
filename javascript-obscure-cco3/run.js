const fs = require('fs')

const start = Date.now()
const letters = require(__dirname + '/../data/letters')

const imap = {}
'abcdefghijklmnopqrstuvwxyz'.split('')
  .concat(process.argv.pop().split(''))
  .forEach(c => imap[c] = imap[c] ? imap[c] + 1 : 1)
const body = Object.entries(imap)
  .map(([k, v]) => `(?:${k}.*){${v}}`)
  .join('|')
const re = new RegExp(`(?:${body})`)
console.log(re)

const max = fs.readFileSync(__dirname + '/../data/dictionary.txt', 'utf8')
  .split(/\s+/)
  .map(word => word.replace(/[^a-z]/g, ''))
  .filter(word => !word.match(re))
  .reduce((acc, cur) => {
    const s = [...cur].reduce((x, y) => x + letters[y].score, 0)
    return s > acc[1] ? [cur, s] : acc
  }, ['', 0])

const ms = Date.now() - start
console.log(`cco3, javascript, ${max[0]}, ${max[1]}, ${ms}, obscure`)
