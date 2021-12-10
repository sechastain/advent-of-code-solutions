
const fs = require('fs');

function parseLine(line) {
  let [crit, pw] = line.split(': ');

  let [inc, ch] = crit.split(' ');

  let [min, max] = inc.split('-').map(x => parseInt(x));

  return {
    min, max, "char": ch, "password": pw
  }
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseLine(x));

function isValid(entry) {
  let count = entry.password.split('').filter(ch => ch === entry.char).length;
  return entry.min <= count && count <= entry.max;
}

console.log(parsed.filter(x => isValid(x)).length);

