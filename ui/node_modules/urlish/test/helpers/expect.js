var urlish = require('../..');

module.exports = function(expected) {
  return function(t) {
    t.plan(1);
    t.deepEqual(urlish(t.name), expected, t.name + ' => ' + JSON.stringify(expected));
  };
};