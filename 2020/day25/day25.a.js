
function countLoops(subjectNum, value, publicKey) {
  let loops = 0;
  while(value != publicKey) {
    loops++;
    value = (value * subjectNum) % 20201227;
  }
  return loops;
}

function loopEncrypt(subjectNum, value, loops) {
  while(loops > 0) {
    value = (value * subjectNum) % 20201227;
    loops--;
  }
  return value;
}

let loops = countLoops(7, 1, 2069194);
let key = loopEncrypt(16426071, 1, loops);

console.log(key);


