
const fs = require('fs');

const grid = fs.readFileSync(process.argv[2]).toString().split('\n').map(line => line && line.split('').map(x => parseInt(x)));
grid.pop();

const moves = {};
grid.forEach((row, rowId) => {
  row.forEach((cell, colId) => {
    const loc = '' + rowId + '.' + colId;
    const poss = [];
    moves[loc] = poss;
    if(colId > 0) {
      poss.push(['' + rowId + '.' + (colId-1), grid[rowId][colId-1]]); // left
    }
    if(colId < row.length - 1)  {
      poss.push(['' + rowId + '.' + (colId+1), grid[rowId][colId+1]]); // right
    }
    if(rowId > 0) {
      poss.push(['' + (rowId-1) + '.' + colId, grid[rowId-1][colId]]); // up
    }
    if(rowId < grid.length - 1) {
      poss.push(['' + (rowId+1) + '.' + colId, grid[rowId+1][colId]]); // down
    }
  });
});

const start = '0.0';
const dest = '' + (grid.length-1) + '.' + (grid[grid.length-1].length-1);

console.log('start', start, moves[start]);
console.log('dest', dest, moves[dest]);

function makePath(loc, prev, cost) {
  const visited = prev && prev.visited ? Object.assign({}, prev.visited) : {};
  visited[loc] = true;
  const steps = prev && prev.steps ? prev.steps.slice() : [];
  steps.push(loc);
  const totalcost = (cost ? cost : 0) + (prev && prev.cost ? prev.cost : 0);
  const ret = {
    visited,
    steps,
    current: loc,
    cost: totalcost
  };
  return ret;
}

function isShorter(path, shortest) {
  const loc = path.current;
  return !shortest[loc] || (path.cost < shortest[loc].cost);
}

function step(path, shortest) {
  const visited = path.visited;
  const current = path.steps[path.steps.length-1];
  const currMoves = moves[current];
  const paths = [];
  currMoves.forEach(move => {
    const [npos, cost] = move;
    let nvisited = makePath(npos, path, cost);
    if(!visited[npos] && isShorter(nvisited, shortest)) {
      paths.push(nvisited);
    } 
  });
  return paths;
}

function findSmallest(loc, queue) {
  const paths = queue[loc] || [];
  delete queue[loc];
  if(paths.length > 0) {
    return paths.reduce((smallest, path) => path.cost < smallest.cost ? path : smallest);
  }
  return null;
}

function pathsReduce(paths) {
  const pathMap = paths.reduce((amap, path) => {
    amap[path.current] = isShorter(path, amap) ? path : amap[path.current];
    return amap;
  }, {});
  const newPaths = Object.keys(pathMap).map(k => pathMap[k]);
  newPaths.sort((l, r) => r.cost - l.cost);
  return newPaths;
}

function searchFor(start, dest, shortest) {
  let paths = [start];
  while(paths.length > 0) {
    //console.log(paths.length);
    let path = paths.pop();
    if(path.current === dest) {
      if(isShorter(path, shortest)) {
        shortest[path.current] = path;
        return;
      }
    } else {
      if(isShorter(path, shortest)) {
        shortest[path.current] = path;
        step(path, shortest).forEach(next => {
          paths.push(next);
        });
        paths = pathsReduce(paths);
      }
    }
  }
}
const shortest = {};
searchFor(makePath(start), dest, shortest);

console.log(shortest[dest].cost);

