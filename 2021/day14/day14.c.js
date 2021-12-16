
const fs = require('fs');

const lines = fs.readFileSync(process.argv[2]).toString().split('\n');

const starting = lines[0].split('');

const rules = lines.slice(2).reduce((amap, line) => {
  if(!line) {
    return amap;
  }
  const rule = line.split(' -> ');
  amap[rule[0]] = rule[1];
  return amap;
}, {});

function treeCount(ch1, ch2, rules, chmap, limit, depth) {
  if(depth < limit) {
    if(depth === 0) {
      chmap[ch1] = (chmap[ch1] || 0) + 1;
    }
    depth++;

    const str = ch1 + ch2;
    const ch3 = rules[str];
    chmap[ch3] = (chmap[ch3] || 0) + 1;

    treeCount(ch1, ch3, rules, chmap, limit, depth);
    treeCount(ch3, ch2, rules, chmap, limit, depth);
  }
}

const chmap = {};
for(let i = 0; i < starting.length-1; i++) {
  console.log(starting[i]);
  treeCount(starting[i], starting[i+1], rules, chmap, 40, 0);
}
chmap[starting.pop()] += 1;

let max = Object.keys(chmap).reduce((max, ch) => chmap[ch] > max ? chmap[ch] : max, 0);
let min = Object.keys(chmap).reduce((min, ch) => chmap[ch] < min ? chmap[ch] : min, max);

console.log(max, min, max-min);

