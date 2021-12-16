
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

const ruleMap = {};

function mapRule(str) {
  let mymap = ruleMap[str] = {};
  let depths = mymap.depths = [];
  let doLoop = true;
  str = str.split('');
  while(doLoop) {
    let foundNew = false;
    depths.push(str);
    let expanded = [];
    for(let i = 0; i < str.length - 1; i++) {
      expanded.push(str[i]);
      let astr = str[i] + str[i+1];
      if(!mymap[astr]) {
        foundNew = true;
        mymap[astr] = rules[astr];
      }
      let ins = rules[astr];
      if(ins) {
        expanded.push(ins);
      }
    }
    if(foundNew) {
      expanded.push(str[str.length-1]);
      str = expanded;
    } else {
      doLoop = false;
    }
  }
  mymap.sums = mymap.depths.map(str => str.reduce((amap, ch) => {
    amap[ch] = (amap[ch] || 0) + 1;
    return amap;
  }, {}));
  mymap.pairs = mymap.depths.map(str => str.reduce((amap, ch, i, arr) => {
    if(i < arr.length - 1) {
      const str = ch + arr[i+1];
      amap[str] = (amap[str] || 0) + 1;
    }
    return amap;
  }, {}));

}

Object.keys(rules).forEach(pair => {
  mapRule(pair, rules)
});

function scaleSums(sums, scalar) {
  return Object.keys(sums).reduce((res, ch) => {
    res[ch] = sums[ch] * scalar;
    return res;
  }, {});
}

function countChars(pair, depth, scalar) {
  if(depth > 30) {
    console.log('tempo 1');
  } else if(depth > 20) {
    console.log('  tempo 2');
  }
  const mymap = ruleMap[pair];
  console.log('depth', depth, 'avail', mymap.depths.length);
  if(depth < mymap.depths.length) {
    console.log('chars', mymap.depths[depth].length, scalar);
    return scaleSums(mymap.sums[depth], scalar);
  } else {
    const mydepth = mymap.depths[mymap.depths.length - 1];
    const pairCounts = mymap.pairs[mymap.pairs.length - 1];
    const firstPair = mydepth[0] + mydepth[1];
    const pairs = Object.keys(pairCounts);
    const firstIndex = pairs.indexOf(firstPair);
    pairs.splice(firstIndex, 1);
    pairs.splice(0, 0, firstPair);

    console.log('pairs for', pair, pairs); 

    const scores = scorePairs(pairs, depth - mymap.depths.length, false, pairCounts);

    const stitched = Object.keys(scores).reduce((tot, ch) => tot + scores[ch], 0);

    console.log('pairs for', pair, pairs, 'stitched', stitched); 

    return scaleSums(scores, scalar);
  }
}

function makePairs(str) {
  let pairs = str.map((ch, i) => i < str.length - 1 ? ch + str[i+1] : null);
  pairs.pop();
  return pairs;
}

function scorePairs(pairs, depth, first, pairCounts) {
  const chmap = {};
  pairCounts = pairCounts || {};
  pairs.forEach((pair, i) => {
    console.log('--------\n', pair, '\n----------');
    const scalar = pairCounts[pair] || 1;
    const sums = countChars(pair, depth, scalar);
    if(i > 0 && first) {
      sums[pair[0]]--;
    }
    Object.keys(sums).forEach(ch => {
      chmap[ch] = (chmap[ch] || 0) + sums[ch];
    });
  });
  return chmap;
}

const startPairs = makePairs(starting);
const chmap = scorePairs(startPairs, 5, true);

console.log(chmap);

let max = Object.keys(chmap).reduce((max, ch) => chmap[ch] > max ? chmap[ch] : max, 0);
let min = Object.keys(chmap).reduce((min, ch) => chmap[ch] < min ? chmap[ch] : min, max);

console.log(max, min, max-min);


