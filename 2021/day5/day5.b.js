
const fs = require('fs');

let lines = fs.readFileSync(process.argv[2]).toString().split('\n');

function buildSegment(line) {
  let [pt1, _, pt2] = line.split(' ');
  pt1 = pt1.split(',');
  pt2 = pt2.split(',');
  return {
    x1: parseInt(pt1[0]),
    y1: parseInt(pt1[1]),
    x2: parseInt(pt2[0]),
    y2: parseInt(pt2[1])
  };
}

function isHorVer(segment) {
  return segment.x1 === segment.x2 || segment.y1 === segment.y2;
}

function plotHorizontal(x1, y1, x2, y2) {
  let sign = x2 > x1 ? 1 : -1
  return [...Array(Math.abs(x2-x1) + 1).keys()].map(off => {
    return {
      x: x1 + sign * off,
      y: y1
    };
  });
}

function plotVertical(x1, y1, x2, y2) {
  let sign = y2 > y1 ? 1 : -1
  return [...Array(Math.abs(y2-y1) + 1).keys()].map(off => {
    return {
      x: x1,
      y: y1 + sign * off
    }
  });
}

function plot45(x1, y1, x2, y2) {
  let ysign = y2 > y1 ? 1 : -1
  let xsign = x2 > x1 ? 1 : -1
  return [...Array(Math.abs(x2-x1) + 1).keys()].map(off => {
    return {
      x: x1 + xsign * off,
      y: y1 + ysign * off
    }
  });
}

function plotSegment(segment) {
  let {x1, y1, x2, y2} = segment;
  if(x1 === x2) {
    return plotVertical(x1, y1, x2, y2);
  } else if(y1 === y2) {
    return plotHorizontal(x1, y1, x2, y2);
  } else {
    return plot45(x1, y1, x2, y2);
  }
}

function applyPlot(plotmap, plotpoints) {
  plotpoints.forEach(pt => {
    let xcol = plotmap[pt.x] = plotmap[pt.x] || {};
    xcol[pt.y] = (xcol[pt.y] || 0) + 1
  });
  return plotmap;
}

const segments = lines.filter(x => !!x).map(buildSegment);
const plotted = segments.map(plotSegment).reduce(applyPlot, {});

let intersections = 0;
Object.keys(plotted).forEach(xcol => {
  let col = plotted[xcol];
  Object.keys(col).forEach(y => {
    intersections += (col[y] > 1 ? 1 : 0);
  });
});

console.log(intersections);




