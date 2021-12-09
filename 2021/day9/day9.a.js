
const fs = require('fs');

function parseLine(line) {
  return line.split('').map(x => parseInt(x));
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => parseLine(x));


function isLowest(data, rowId, colId) {
  const row = data[rowId];
  const val = row[colId];
  const up = rowId > 0 ? data[rowId-1][colId] > val : true;
  const dn = rowId < data.length-1 ? data[rowId+1][colId] > val : true;
  const lf = colId > 0 ? row[colId-1] > val : true;
  const rt = colId < row.length-1 ? row[colId+1] > val : true;
  return up && dn && lf && rt;
}

function riskLevel(data, row, col) {
  if(!isLowest(data, row, col)) {
    return 0;
  }
  return data[row][col] + 1;
}

const risk = parsed.reduce((tot, row, rowId) => tot + row.reduce((tot, col, colId) => tot + riskLevel(parsed, rowId, colId), 0), 0);

console.log(risk);

