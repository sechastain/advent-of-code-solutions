
const fs = require('fs');

function parseInput(lines) {
  const entries = [];
  let curr = {};
  lines.forEach(line => {
    if(line === '') {
      entries.push(curr);
      curr = {};
    } else {
      line.split(' ').forEach(pair => {
        let [key, val] = pair.split(':');
        curr[key] = val;
      });
    }
  });

  return entries;
}

const haircodes = ['a', 'b', 'c', 'd', 'e', 'f', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
const eyecodes  = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'];
const fieldRules = {
  "byr": function (byr) {
    try {
      byr = parseInt(byr);
      return 1920 <= byr && byr <= 2002;
    } catch (error) {
      return false;
    }
  },
  "iyr": function (iyr) {
    try {
      iyr = parseInt(iyr);
      return 2010 <= iyr && iyr <= 2020;
    } catch (error) {
      return false;
    }
  },
  "eyr": function (eyr) {
    try {
      eyr = parseInt(eyr);
      return 2020 <= eyr && eyr <= 2030;
    } catch (error) {
      return false;
    }
  },
  "hgt": function (hgt) {
    try {
      const len = hgt.length;
      const unit = hgt.slice(len-2, len);
      const meas = parseInt(hgt.slice(0, len-2));
      return (unit === 'cm' && 150 <= meas && meas <= 193) || (unit === 'in' && 59 <= meas && meas <= 76)
    } catch (error) {
      return false;
    }
  },
  "hcl": function (hcl) {
    try {
      hcl = hcl.split('');
      return hcl.length === 7 && hcl[0] === '#' && hcl.slice(1).reduce((res, ch) => res && haircodes.indexOf(ch) >= 0, true);
    } catch (error) {
      return false;
    }
  },
  "ecl": function (ecl) {
    try {
      return eyecodes.indexOf(ecl) >= 0;
    } catch (error) {
      return false;
    }
  },
  "pid": function (pid) {
    try {
      return pid.length === 9 && parseInt(pid);
    } catch (error) {
      return false;
    }
  },
  "cid": function (cid) {
    return true;
  }
};

const requiredFields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"];
function isValid(entry) {
  const fields = Object.keys(entry);
  const present = requiredFields.reduce((res, fld) => res && (fields.indexOf(fld) >= 0), true);
  if(present) {
    return fields.reduce((res, fld) => res && fieldRules[fld](entry[fld]), true);
  } else {
    return false;
  }
}

const input = fs.readFileSync(process.argv[2]).toString().split('\n');
const entries = parseInput(input);


console.log(entries.length);
console.log(entries.filter(entry => isValid(entry)).length);

