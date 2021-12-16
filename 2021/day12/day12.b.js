
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

function canRevisit(loc, visited) {
  if((loc === 'start' || loc === 'end') && visited[loc]) {
    return false;
  }
  if(loc.toUpperCase() === loc) {
    return true;
  }
  const twoKey = Object.keys(visited).find(k => visited[k] === 2);
  return !twoKey || !visited[loc];
}

function pathsFrom(amap, from, visited) {
  if(from === 'end') {
    return [['end']];
  }

  const revisit = canRevisit(from, visited);
  if(!revisit) {
    return [];
  }
  const isLower = from.toLowerCase() === from;
  if(isLower) {
    visited[from] = (visited[from] || 0) + 1;
  }
  const toVisit = amap[from];
  const foundPaths = [];

  toVisit.forEach(next => {
    const nextPaths = pathsFrom(amap, next, visited);
    nextPaths.forEach(np => {
      np.unshift(from);
      foundPaths.push(np);
    });
  });
  
  if(isLower) {
    visited[from] = visited[from] - 1;
  }

  return foundPaths;
}

function findPaths(amap) {
  return pathsFrom(amap, 'start', {});
}

const paths = findPaths(parsed);
console.log(paths.length);


