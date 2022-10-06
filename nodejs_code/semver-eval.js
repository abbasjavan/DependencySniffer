var myArgs = process.argv.slice(2);
// var argv = require('minimist')(process.argv.slice(2));
// console.log(argv._[0]);
// console.log(argv._[1]);
// <"['1.2.1','1.3.0','1.3.1','2.0.0']" "^1.2.3"> results in <1.3.1>

const semver = require('semver')
// const JSON5 = require('json5')
// //var array = JSON.parse(myArgs[0]);
// console.log(argv._)
// console.log(myArgs[0])
// console.log(myArgs[1])
// console.log(myArgs[1])
// console.log(myArgs)

////var myArray = ['1.2.1','1.3.0','1.3.1','2.0.0']
array = myArgs[0].replace(/'/g, '"')
// console.log(array)
array = JSON.parse(array)
// console.log(array)
//var thisArray = JSON.stringify(myArray)
//console.log(thisArray)
console.log(semver.maxSatisfying(array, myArgs[1]))



