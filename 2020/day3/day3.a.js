
const fs = require('fs');

const input = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => x.split(''));

function countTrees(treeMap, run, fall) {
  let row = 0, col = 0;
  let treeCount = 0;
  while(row < treeMap.length) {
    if(treeMap[row][col] === '#') {
      treeCount++;
    }
    col = (col + run) % treeMap[row].length;
    row = row + fall;
  }
  return treeCount;
}

console.log(countTrees(input, 3, 1));

const partb = [[1,1], [3,1], [5,1], [7,1], [1,2]];
console.log(partb.reduce((tot, [run, fall]) => tot * countTrees(input, run, fall), 1));


