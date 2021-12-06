
const fs = require('fs');

const fishy_input = fs.readFileSync(process.argv[2]).toString().split(',').map(x => parseInt(x));

function build_age_groups(fish_ages) {
  return fish_ages.reduce((groups, fish) => {
    groups[fish] = (groups[fish] || 0) + 1;
    return groups;
  }, {});
}

function cycle_fish(fish_ages) {
  return Object.keys(fish_ages).reduce((group, age) => {
    let new_age = age-1;
    if(new_age === -1) {
      group[6] = (group[6] || 0) + fish_ages[age];
      group[8] = fish_ages[age];
    } else if(new_age === 6) {
      group[6] = (group[6] || 0) + fish_ages[age];
    } else {
      group[new_age] = fish_ages[age];
    }
    return group;
  }, {});
}

let school = build_age_groups(fishy_input);

console.log(school);

[...new Array(80).keys()].forEach(_ => {
  school = cycle_fish(school);
});

console.log(school);

console.log('--------');

console.log(Object.keys(school).reduce((tot, x) => tot + school[x], 0));

