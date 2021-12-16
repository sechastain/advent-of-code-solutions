
const fs = require('fs');

const lines = fs.readFileSync(process.argv[2]).toString().split('\n');

const starting = lines[0].split('').map((ch, i, arr) => {
  if(i < arr.length) {
    return ch + arr[i+1];
  } else {
    return null;
  }
});
starting.pop();

const startMap = starting.reduce((amap, pair, i) => {
  if(i === 0) {
    amap.first = pair;
  }
  amap[pair] = (amap[pair] || 0) + 1;
  return amap;
}, {});

const rules = lines.slice(2).reduce((amap, line) => {
  if(!line) {
    return amap;
  }
  const rule = line.split(' -> ');
  const [ch1, ch2] = rule[0].split('');
  amap[rule[0]] = [ch1 + rule[1], rule[1] + ch2];
  return amap;
}, {});

function expand(pairMap) {
  const pairs = Object.keys(pairMap);
  const newMap = {};
  pairs.forEach(pair => {
    if(pair === 'first') {
      return;
    }
    const [pair1, pair2] = rules[pair];
    const count = pairMap[pair];
    newMap[pair1] = (newMap[pair1] || 0) + count;
    newMap[pair2] = (newMap[pair2] || 0) + count;
  });
  newMap.first = rules[pairMap.first][0];
  return newMap;
}

function countLetters(pairMap) {
  const pairs = Object.keys(pairMap);
  const first = pairMap.first;
  return pairs.reduce((chmap, pair) => {
    if(pair === first) {
      chmap[pair[0]] = (chmap[pair[0]] || 0) + pairMap[pair];
    }
    chmap[pair[1]] = (chmap[pair[1]] || 0) + pairMap[pair];
    return chmap;
  }, {});
}

const pairTotals = [...new Array(40).keys()].reduce((prev, _) => expand(prev), startMap);
const chmap = countLetters(pairTotals);

let max = Object.keys(chmap).reduce((max, ch) => chmap[ch] > max ? chmap[ch] : max, 0);
let min = Object.keys(chmap).reduce((min, ch) => chmap[ch] < min ? chmap[ch] : min, max);

console.log(max, min, max-min);

