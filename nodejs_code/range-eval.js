var myArgs = process.argv.slice(2);
// var argv = require('minimist')(process.argv.slice(2));
// console.log(argv._[0]);
// console.log(argv._[1]);
// <"['1.2.1','1.3.0','1.3.1','2.0.0']" "^1.2.3"> results in <1.3.1>

const semver = require('semver')

// array = myArgs[0].replace(/'/g, '"')

// array = JSON.parse(array)

// console.log(semver.maxSatisfying(array, myArgs[1]))

console.log(semver.validRange(myArgs[0]))





