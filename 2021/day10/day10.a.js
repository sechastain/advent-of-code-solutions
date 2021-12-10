
const fs = require('fs');

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => !!x).map(x => x.split(''));

const openers = ['<', '[', '{', '('];

const openCloser = {
  '<': '>',
  '[': ']',
  '{': '}',
  '(': ')'
};

function isOpenChar(ch) {
  return openers.indexOf(ch) >= 0;
}

function parseChunk(line, offset, autocomplete) {
  const chunks = [];
  const ch = line[offset];

  if(offset === line.length) {
    return [undefined, offset];
  } else if(!isOpenChar(ch)) {
    return [undefined, offset];
  }

  let nxtoff = offset+1;
  do {
    [child_chunks, nxtoff] = parseChunk(line, nxtoff, autocomplete);
    if(child_chunks) {
      chunks.push(child_chunks);
    }
  } while(isOpenChar(line[nxtoff]));

  if(nxtoff >= line.length) {
    if(!autocomplete) {
      throw ['incomplete', line.length];
    } else {
      line.autocomplete = line.autocomplete || [];
      line.autocomplete.push(openCloser[ch]);
      return [chunks, nxtoff+1];
    }
  } else if(openCloser[ch] === line[nxtoff]) {
    return [chunks, nxtoff+1];
  } else {
    throw [line[nxtoff], nxtoff];
  }
}

function parseLine(line, autocomplete) {
  return parseChunk(line, 0, autocomplete);
}

function scoreIllegalCharacters(input) {
  const scoreMap = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
  };

  const scoreCounter = {};

  input.forEach(line => {
    try {
      parseLine(line);
    } catch (error) {
      let [err, index] = error;
      scoreCounter[err] = (scoreCounter[err] || 0) + 1;
    }
  });

  return Object.keys(scoreCounter).reduce((tot, x) => (tot + ((scoreMap[x] || 0) * scoreCounter[x])), 0);

}

function scoreIncompleteLines(input) {
  const scoreMap = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
  };

  const autocompletes = [];
  input.forEach(line => {
    try {
      parseLine(line);
    } catch (error) {
      let [err, index] = error;
      if(err === 'incomplete') {
        parseLine(line, true);
        autocompletes.push(line.autocomplete);
      }
    }
  });

  const scores = autocompletes.map(x => x.reduce((tot, y) => tot * 5 + scoreMap[y], 0));
  scores.sort((l, r) => r - l);
  return scores[Math.floor(scores.length/2)];
}

console.log(scoreIllegalCharacters(parsed));

console.log(scoreIncompleteLines(parsed));

