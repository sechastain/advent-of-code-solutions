
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

function expandRuleset(rules, expanded) {
  Object.keys(expanded).forEach(key => {
    let str = expanded[key];
    let nstr = [];
    if(str.length === 1) {
      nstr = key.split('');
      nstr.splice(1, 0, str[0]);
    } else {
      for(let i = 0; i < str.length; i++) {
        nstr.push(str[i]);
        if(i < str.length-1) {
          let akey = str[i] + str[i+1];
          let ins = rules[akey];
          if(ins) {
            nstr.push(ins);
          }
        }
      }
    }
    expanded[key] = nstr;
  });
}

let pairs = [];
starting.forEach((ch, i) => {
  if(i < starting.length-1) {
    pairs.push(ch + starting[i+1]);
  }
});
console.log(pairs);
let expanded = Object.keys(rules).reduce((nmap, key) => {
  if(pairs.indexOf(key) >= 0) {
    nmap[key] = [rules[key]];
  }
  return nmap;
}, {});


for(let i = 0; i < 40; i++) {
  console.log('round', i);
  expandRuleset(rules, expanded);
}

let chmap = {};
starting.forEach((ch, i) => {
  chmap[ch] = (chmap[ch] || 0) + 1;
  if(i < starting.length-1) {
    ch = ch + starting[i+1];
    chmap = (expanded[ch] || []).reduce((amap, ch) => {
      amap[ch] = (amap[ch] || 0) + 1;
      return amap;
    }, chmap);
  }
});


let max = Object.keys(chmap).reduce((max, ch) => chmap[ch] > max ? chmap[ch] : max, 0);
let min = Object.keys(chmap).reduce((min, ch) => chmap[ch] < min ? chmap[ch] : min, max);

console.log(max, min, max-min);

