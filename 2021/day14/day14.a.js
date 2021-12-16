
const fs = require('fs');

const lines = fs.readFileSync(process.argv[2]).toString().split('\n');

const starting = lines[0];

const rules = lines.slice(2).reduce((amap, line) => {
  if(!line) {
    return amap;
  }
  const rule = line.split(' -> ');
  amap[rule[0]] = rule[1];
  return amap;
}, {});

function applyPairInsertion(value, rules) {
  value = value.split('');
  const new_value = [];
  value.forEach((ch, i) => {
    new_value.push(ch);
    if(i < value.length - 1) {
      const pair = ch + value[i+1];
      const ins = rules[pair];
      if(ins) {
        new_value.push(ins);
      }
    }
  });
  return new_value.join('');
}

let iterated = starting;

for(let i = 0; i < 10; i++) {
  console.log(i);
  iterated = applyPairInsertion(iterated, rules);
}

let chmap = iterated.split('').reduce((amap, ch) => {
  amap[ch] = (amap[ch] || 0) + 1;
  return amap;
}, {});

let max = Object.keys(chmap).reduce((max, ch) => chmap[ch] > max ? chmap[ch] : max, 0);
let min = Object.keys(chmap).reduce((min, ch) => chmap[ch] < min ? chmap[ch] : min, max);

console.log(max, min, max-min);
