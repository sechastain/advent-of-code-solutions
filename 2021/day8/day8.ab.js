
const fs = require('fs');

function buildSortedDigits(lineSeg) {
  return lineSeg.split(' ').map(x => {
    x = x.split('');
    x.sort();
    return x.join('');
  });
}

function parseLine(line) {
  let x = line.split(' | ');
  return {
    "wires": buildSortedDigits(x[0]),
    "disp": buildSortedDigits(x[1])
  };
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseLine(x));

const simpleDigitLengths = [2, 3, 4, 7];
function isSimpleDigit(digit) {
  return simpleDigitLengths.indexOf(digit.length) >= 0;
}

function countDistinctDigits(parsedInput) {
  return parsedInput.reduce((tot, line) => {
    line.disp.forEach(x => {
      tot += isSimpleDigit(x) ? 1 : 0;
    });
    return tot;
  }, 0);
}
console.log('Simple Digits', countDistinctDigits(parsed));

function charrMatch(charr, num) {
  return charr.reduce((res, c) => {
    return res && (num.indexOf(c) >= 0);
  }, true);
}

function decodeSixes(sixes, digimap) {
  const four = digimap[4].split('');
  const one = digimap[1].split('');
  
  const nine = sixes.filter(x => charrMatch(four, x))[0];
  sixes.splice(sixes.indexOf(nine), 1);
  
  const zero = sixes.filter(x => charrMatch(one, x))[0];
  sixes.splice(sixes.indexOf(zero), 1);
  
  const six = sixes[0];

  digimap[zero] = 0;
  digimap[0] = zero;
  digimap[six] = 6;
  digimap[6] = six;
  digimap[nine] = 9;
  digimap[9] = nine;
}

function decodeFives(fives, digimap) {
  const one = digimap[1].split('');
  const four = digimap[4].split('');
  
  const three = fives.filter(x => charrMatch(one, x))[0];
  fives.splice(fives.indexOf(three), 1);
  
  const first = fives[0];
  
  const matches = four.reduce((tot, c) => (tot + (first.indexOf(c) >= 0 ? 1 : 0)), 0);
  const five = matches === 3 ? first : fives[1];
  const two = matches === 3 ? fives[1] : first;
  
  digimap[two] = 2;
  digimap[2] = two;
  digimap[three] = 3;
  digimap[3] = three;
  digimap[five] = 5;
  digimap[5] = five;
}

const knownDigits = [1, 7, 4, 8];
function decodeKnowns(wires, digimap) {
  knownDigits.forEach((val, idx) => {
    idx = idx < 3 ? idx : 9;
    digimap[val] = wires[idx];
    digimap[wires[idx]] = val;
  });  
}

function decodeDigits(wires) {
  wires.sort((l, r) => l.length - r.length);
  let fives = wires.slice(3, 6);
  let sixes = wires.slice(6, 9);

  const digimap = {};
  decodeKnowns(wires, digimap);
  decodeSixes(sixes, digimap);
  decodeFives(fives, digimap);
  
  return digimap;
}

function decodeDisplay(disp, digimap) {
  return disp.reduce((tot, x) => (tot * 10 + digimap[x]), 0);
}

console.log('Digi sum', parsed.reduce((tot, x) => (tot + decodeDisplay(x["disp"], decodeDigits(x["wires"]))), 0));


