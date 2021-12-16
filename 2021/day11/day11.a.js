
const fs = require('fs');

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => x.split('').map(y => parseInt(y)));

function power(rows, row, col, flashers, flashed) {
  const sliceSize = col === -1 ? 2 : 3;
  col = col === -1 ? 0 : col;
  for(let i = col; i < col + sliceSize && i < rows[row].length; i++) {
    rows[row][i]++;
    if(rows[row][i] > 9) {
      flashers.push([row, i]);
    }
  }
}

function flash(rows, point, flashers, flashed) {
  let [row, col] = point;

  let flashedRow = flashed[row] = flashed[row] || [];

  if(flashedRow.indexOf(col) >= 0) {
    return; // do nothing - already flashed
  }
  flashedRow.push(col);

  if(row > 0) {
    power(rows, row-1, col-1, flashers, flashed);
  }

  power(rows, row, col-1, flashers, flashed);

  if(row < rows.length-1) {
    power(rows, row+1, col-1, flashers, flashed);
  }
}

function findFlashers(rows) {
  const flashed = {};
  let flashers = [];
  rows.forEach((row, rowId) => {
    row.forEach((col, colId) => {
      if(col > 9) {
        flashers.push([rowId, colId]);
      }
    });
  });

  for(let i = 0; i < flashers.length; i++) {
    flash(rows, flashers[i], flashers, flashed);
  }

  flashers = Object.keys(flashed).map(row => flashed[row].map(col => [parseInt(row), col])).flat();
  flashers.forEach(pt => {
    let [row, col] = pt;
    rows[row][col] = 0;
  });

  return flashers;
}

function step(rows) {
  rows = rows.map(row => row.map(col => col + 1));
  return [rows, findFlashers(rows)];
}

let lastMap = parsed;
let maps = [];
let mapped_flashers = [];
for(let generation = 0; generation < 100; generation++) {
  let [newMap, newFlashers] = step(lastMap);
  maps.push(newMap);
  mapped_flashers.push(newFlashers);
  lastMap = newMap;
}

console.log(mapped_flashers.reduce((tot, flashers) => tot + flashers.length, 0));


