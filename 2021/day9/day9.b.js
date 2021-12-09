
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

function findLowestPoints(data) {
  const lowest = [];
  data.forEach((row, rowId) => {
    row.forEach((val, colId) => {
      if(isLowest(data, rowId, colId)) {
        lowest.push([rowId, colId]);
      }
    });
  });

  return lowest;
}

function nextPoints(point, visited) {
  const [row, col] = point;
  const ret = [];

  visited[row-1] = visited[row-1] || {};
  visited[row+1] = visited[row+1] || {};

  if(row > 0 && !visited[row-1][col]) {
    ret.push([row-1, col]);
  }
  if(row < parsed.length-2 && !visited[row+1][col]) {
    ret.push([row+1, col]);
  }
  if(col > 0 && !visited[row][col-1]) {
    ret.push([row, col-1]);
  }
  if(col < parsed[0].length-2 && !visited[row][col+1]) {
    ret.push([row, col+1]);
  }

  return ret;
}

function explorePoint(data, point, visited) {
  const [row, col] = point;
  const val = data[row][col];
  if(val === 9) {
    return;
  }

  visited[row] = visited[row] || {};
  visited[row][col] = true;

  const next = nextPoints(point, visited);

  next.forEach(pt => explorePoint(data, pt, visited));
}

function sizeBasin(data, point) {
  visited = {};

  explorePoint(data, point, visited);

  return Object.keys(visited).reduce((tot, row) => tot + Object.keys(visited[row]).length, 0);
}

const lowest = findLowestPoints(parsed);
const basinSizes = lowest.map(pt => sizeBasin(parsed, pt));
basinSizes.sort((l, r) => r - l);
console.log(basinSizes.slice(0, 3).reduce((tot, x) => tot * x, 1));

