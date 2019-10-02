const fs = require('fs')
const readline = require('readline')

const start = Date.now()
const card = []
Object.entries(require(__dirname + '/../data/letters')).forEach(([k, v]) => {
  card[k.charCodeAt(0) - 97] = v.score
})

const input = process.argv.pop()
const imap = []
for (let i = 0; i < input.length; i++) {
  const id = input.charCodeAt(i) - 97
  const v = imap[id]
  imap[id] = v ? v + 1 : 1
}

let max = ['', 0]
for (let i = 0; i < input.length; i++) {
  const s = card[input.charCodeAt(i) - 97]
  if (s > max[1]) max = [input.charAt(i), s]
}

const rl = readline.createInterface({
    input: fs.createReadStream(__dirname + '/../data/dictionary.txt')
})

rl.on('line', word => {
  if (word.length > input.length) return
  let s = 0
  for (let i = 0; i < word.length; i++) {
    const id = word.charCodeAt(i) - 97
    if (!imap[id]) return
    s += card[id]
  }
  if (s <= max[1]) return

  const newmap = []
  for (let i = 0; i < word.length; i++) {
    const id = word.charCodeAt(i) - 97
    let v = newmap[id]
    v = v ? v + 1 : 1
    if (v > imap[id]) return
    newmap[id] = v
  }
  max = [word, s]
});

rl.on('close', () => {
  const ms = Date.now() - start
  console.log(`cco3, javascript, ${max[0]}, ${max[1]}, ${ms}, sparse arrays`)
});
