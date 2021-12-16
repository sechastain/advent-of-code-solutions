
const fs = require('fs');

function parseLine(amap, line) {
  let [pt1, pt2] = line.split('-');
  let pt1nav = amap[pt1] = amap[pt1] || [];
  pt1nav.push(pt2);
  let pt2nav = amap[pt2] = amap[pt2] || [];
  pt2nav.push(pt1);

  return amap;
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).reduce((result, line) => parseLine(result, line), {});

function pathsFrom(amap, from, visited) {
  if(from === 'end') {
    return [['end']];
  }

  const toVisit = amap[from];
  const foundPaths = [];

  const revisit = from.toUpperCase() === from;
  console.log('revisit', revisit);
  if(!revisit) {
    visited.push(from);
  }

  toVisit.forEach(next => {
    if(visited.indexOf(next) === -1) {
      const nextPaths = pathsFrom(amap, next, visited);
      nextPaths.forEach(np => {
        np.unshift(from);
        foundPaths.push(np);
      });
    }
  });
  
  if(!revisit) {
    visited.pop();
  }

  return foundPaths;
}

function findPaths(amap) {
  return pathsFrom(amap, 'start', []);
}

const paths = findPaths(parsed);
console.log(paths);
console.log(paths.length);


