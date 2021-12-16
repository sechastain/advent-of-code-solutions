
const fs = require('fs');

const hexMap = {
  '0': [0, 0, 0, 0],
  '1': [0, 0, 0, 1],
  '2': [0, 0, 1, 0],
  '3': [0, 0, 1, 1],
  '4': [0, 1, 0, 0],
  '5': [0, 1, 0, 1],
  '6': [0, 1, 1, 0],
  '7': [0, 1, 1, 1],
  '8': [1, 0, 0, 0],
  '9': [1, 0, 0, 1],
  'A': [1, 0, 1, 0],
  'B': [1, 0, 1, 1],
  'C': [1, 1, 0, 0],
  'D': [1, 1, 0, 1],
  'E': [1, 1, 1, 0],
  'F': [1, 1, 1, 1],
};

const opMap = {
  0: function sum(packet) {
    return packet.subs.reduce((tot, sub) => tot + sub.value, 0);
  },
  1: function mul(packet) {
    return packet.subs.reduce((tot, sub) => tot * sub.value, 1);
  },
  2: function min(packet) {
    return packet.subs.map(p => p.value).reduce((left, right) => left < right ? left : right);
  },
  3: function max(packet) {
    return packet.subs.map(p => p.value).reduce((left, right) => left > right ? left : right);
  },
  4: function val(packet) {
    return packet.value;
  },
  5: function gt(packet) {
    return packet.subs[0].value > packet.subs[1].value ? 1 : 0;
  },
  6: function lt(packet) {
    return packet.subs[0].value < packet.subs[1].value ? 1 : 0;
  },
  7: function eq(packet) {
    return packet.subs[0].value === packet.subs[1].value ? 1 : 0;
  },
};

function parseLine(line) {
  if(!line) return;
  return line.split('').map(ch => hexMap[ch].slice()).flat();
}

const parsed = fs.readFileSync(process.argv[2]).toString().split('\n').filter(x => x != '').map(line => parseLine(line));

function readAsInt(buff, off, len) {
  const val = buff.slice(off, off+len).reduce((val, bit) => 2 * val + bit, 0);
  return [val, off+len];
}

function readLiteral(buff, off) {
  let isLast = false;
  let value = 0;
  while(!isLast) {
    if(buff[off] === 0) {
      isLast = true;
    }
    value = value * 16 + readAsInt(buff, off+1, 4)[0];
    off += 5;
  }
  let align = off % 4;
  //off += ((4 - align) % 4);
 
  return [value, off];
}

function readBitsSubpackets(buff, off) {
  const [bits, boff] = readAsInt(buff, off, 15);
  const subs = [];
  let soff = boff;
  let sub;
  while(soff < (boff + bits)) {
    [sub, soff] = readPacket(buff, soff);
    subs.push(sub);
  }
  return [subs, soff];
}

function readNumSubpackets(buff, off) {
  const [num, noff] = readAsInt(buff, off, 11);
  const subs = [];
  let soff = noff;
  let sub;
  for(let i = 0; i < num; i++) {
    [sub, soff] = readPacket(buff, soff);
    subs.push(sub);
  }
  return [subs, soff];
}

function readPacket(buff, off) {
  const [version, voff] = readAsInt(buff, off, 3);
  const [type, toff] = readAsInt(buff, voff, 3);
  const packet = {
    version,
    type,
    offset: off
  };
  let eob;
  if(type === 4) {
    const [value, valoff] = readLiteral(buff, toff);
    packet.value = value;
    eob = valoff;
  } else {
    const [subs, suboff] = buff[toff] === 0 ? readBitsSubpackets(buff, toff + 1) : readNumSubpackets(buff, toff + 1);
    packet.subs = subs;
    eob = suboff;
  }
  return [packet, eob];
}

function sumVersions(packet) {
  return packet.version + (packet.type === 4 ? 0 : packet.subs.reduce((tot, sub) => tot + sumVersions(sub), 0)); 
}

function evalPacket(packet) {
  if(packet.subs) {
    packet.subs.forEach(sub => evalPacket(sub));
  }
  packet.value = opMap[packet.type](packet);
  return packet.value;
}

//console.log(JSON.stringify(readPacket(parseLine('38006F45291200'), 0), null, '  '));
//console.log(JSON.stringify(readPacket(parseLine('EE00D40C823060'), 0), null, '  '));

//console.log(JSON.stringify(readPacket(parseLine('8A004A801A8002F478'), 0), null, '  '));

//console.log(JSON.stringify(readPacket(parseLine('620080001611562C8802118E34'), 0), null, '  '));

//console.log(sumVersions(readPacket(parseLine('C0015000016115A2E0802F182340'), 0)[0]));

//console.log(evalPacket(readPacket(parseLine('880086C3E88112'), 0)[0]));

console.log(sumVersions(readPacket(parsed[0], 0)[0]));
console.log(evalPacket(readPacket(parsed[0], 0)[0]));

