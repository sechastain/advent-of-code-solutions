
const fs = require('fs');

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseInt(x));

const pair = parsed.filter(x => parsed.indexOf(2020 - x) >= 0)[0];

console.log(pair * (2020-pair));

