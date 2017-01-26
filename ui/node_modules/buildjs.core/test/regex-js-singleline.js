var test = require('tape');
var regex = require('../regexes').includeDoubleSlash;

test('//= filename.js', function(t) {
  var match;

  t.plan(4);
  match = regex.exec(t.name);

  t.ok(match);
  t.equal(match[1], ''); // leader
  t.equal(match[2], ''); // directive
  t.equal(match[3], 'filename.js'); // filename
});

test('//= path/filename.js', function(t) {
  var match;

  t.plan(4);
  match = regex.exec(t.name);

  t.ok(match);
  t.equal(match[1], ''); // leader
  t.equal(match[2], ''); // directive
  t.equal(match[3], 'path/filename.js'); // filename
});

test('//==============================', function(t) {
  var match;

  t.plan(1);
  match = regex.exec(t.name);
  t.notOk(match);
});
