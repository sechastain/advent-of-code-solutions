
const fs = require('fs');

function parseLine(line) {
  let [crit, pw] = line.split(': ');

  let [inc, ch] = crit.split(' ');

  let [min, max] = inc.split('-').map(x => parseInt(x));
  min--;
  max--;

  return {
    min, max, "char": ch, "password": pw.split('')
  }
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseLine(x));

function isValid(entry) {
  const a = entry.password[entry.min] === entry.char;
  const b = entry.password[entry.max] === entry.char;
  return (a && !b) || (!a && b);
}

console.log(parsed.filter(x => isValid(x)).length);

