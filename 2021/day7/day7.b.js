
const fs = require('fs');

const crabby_input = fs.readFileSync(process.argv[2]).toString().split(',').map(x => parseInt(x));

crabby_input.sort((l, r) => l-r);

const average = Math.floor(crabby_input.reduce((tot, x) => tot + x, 0) / crabby_input.length);

const cost = crabby_input.map(x => {
  const dist = Math.abs(x - average);
  const cost = dist > 1 ? ((dist + 1) * (dist/2)) : dist;
  return cost;
}).reduce((tot, x) => tot + x, 0);

console.log(average);
console.log(cost);

