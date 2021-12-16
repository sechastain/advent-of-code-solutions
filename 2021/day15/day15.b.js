
const fs = require('fs');

function increment(cell, inc) {
  cell = cell + inc;
  if(cell > 9) {
    cell = cell - 9;
  }
  return cell;
}

function expandGrid(grid) {
  grid = grid.map(row1 => {
    const row2 = row1.map(cell => increment(cell, 1));
    const row3 = row1.map(cell => increment(cell, 2));
    const row4 = row1.map(cell => increment(cell, 3));
    const row5 = row1.map(cell => increment(cell, 4));
    return [row1, row2, row3, row4, row5].flat();
  });
  const og = grid.length;
  for(let i = 1; i < 5; i++) {
    for(let row = 0; row < og; row++) {
      grid.push(grid[row].map(cell => increment(cell, i)));
    }
  }
  return grid;
}

let grid = fs.readFileSync(process.argv[2]).toString().split('\n').map(line => line && line.split('').map(x => parseInt(x)));
grid.pop();

grid = expandGrid(grid);

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
  visited[loc] = prev;
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
  if(!shortest[loc]) {
    return true;
  }
  if(path.cost >= shortest[loc].cost) {
    return false;
  }
  return path.steps.reduce((isShortest, aloc) => isShortest && path.visited[aloc] === shortest[aloc], true);
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
  let i = 0;
  while(paths.length > 0) {
    i++;
    console.log(paths.length, i % 1000, i);
    let path = paths.pop();
    if(path.current === dest) {
      if(isShorter(path, shortest)) {
        shortest[path.current] = path;
        console.log('returning');
        return;
      }
    } else {
      if(isShorter(path, shortest)) {
        shortest[path.current] = path;
        step(path, shortest).forEach(next => {
          paths.push(next);
        });
        paths = pathsReduce(paths);
        if(global.gc && i % 1000 === 0) global.gc();
      }
    }
  }
}

const shortest = {};
searchFor(makePath(start), dest, shortest);

console.log(shortest[dest].steps);
console.log(shortest[dest].cost);

