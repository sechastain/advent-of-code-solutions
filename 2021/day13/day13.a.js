
const fs = require('fs');

function parseLine(amap, line) {
  const isPt = !amap.folds && line !== '';
  if(!isPt && !amap.folds) {
    amap.folds = [];
  } else if(!isPt && line !== '') {
    let parts = line.split('=');
    let axis = parts[0].split('').pop();
    let val = parseInt(parts[1]);
    amap.folds.push([axis, val]);
  } else if(isPt) {
    amap.points = amap.points || [];
    amap.points.push(line.split(',').map(x => parseInt(x)));
  }

  return amap;
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').reduce((amap, line) => parseLine(amap, line), {});

function foldCol(themap, col) {
  col++;
  return themap.map(row => {
    const nrow = row.slice(0, col);
    const copy = row.slice(col);
    copy.forEach((val, i) => {
      nrow[col - 2 - i] = (nrow[col - 2 - i] || 0) + val;
    });
    return nrow;
  });
}

function foldRow(themap, rowLine) {
  rowLine++;
  themap = themap.map(x => x.slice(0));
  const newmap = themap.slice(0, rowLine);
  const copy = themap.slice(rowLine);
  copy.forEach((row, rowId) => {
    const maprow = newmap[rowLine - 2 - rowId] = newmap[rowLine - 2 - rowId] || [];
    row.forEach((cell, colId) => {
      maprow[colId] = (maprow[colId] || 0) + cell;
    });
  });
  return newmap;
}

const foldFn = {
  'x': foldCol,
  'y': foldRow
};

function foldMap(themap, folds) {
  return folds.reduce((amap, fold) => foldFn[fold[0]](amap, fold[1]), themap);
}

function createMap(points) {
  const themap = [];
  points.forEach(([colId, rowId]) => {
    let row = themap[rowId] = themap[rowId] || [];
    row[colId] = 1;
  });
  return themap;
}

function genOutput(amap) {
  const maxw = amap.reduce((max, line) => max > line.length ? max : line.length, 0);
  let ret = '';
  for(let row = 0; row < amap.length; row++) {
    amap[row] = amap[row] || [];
    for(let col = 0; col < amap[row].length; col++) {
      let val = amap[row][col];
      ret += (!!val ? '#' : ' ');
    }
    ret += '\n';
  }
  return ret;
};

let omap = createMap(parsed.points);
let foldedMap = foldMap(omap, parsed.folds.slice(0, 1));

console.log(foldedMap.reduce((tot, row) => tot + row.reduce((cnt, cell) => cnt + (cell > 0 ? 1:0), 0), 0));
console.log('--------');
foldedMap = foldMap(omap, parsed.folds);
console.log(genOutput(foldedMap));

