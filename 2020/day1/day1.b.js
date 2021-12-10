
const fs = require('fs');

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseInt(x));

for(let x = 0; x < parsed.length; x++) {
  for(let y = x+1; y < parsed.length; y++) {
    for(let z = y+1; z < parsed.length; z++) {
      let a = parsed[x];
      let b = parsed[y];
      let c = parsed[z];
      if(a + b + c === 2020) {
        console.log(a * b * c);
      }
    }
  }
}

