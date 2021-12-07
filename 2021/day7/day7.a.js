
const fs = require('fs');

const crabby_input = fs.readFileSync(process.argv[2]).toString().split(',').map(x => parseInt(x));

crabby_input.sort((l, r) => l-r);

const median = crabby_input[Math.ceil(crabby_input.length/2)];

const cost = crabby_input.map(x => Math.abs(x - median)).reduce((tot, x) => tot + x, 0);

console.log(median);
console.log(cost);

