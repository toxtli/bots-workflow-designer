var test = require('tape');
var expect = require('./helpers/expect');

test('gist://DamonOehlman:6999398', expect({
  scheme: 'gist',
  hostname: 'DamonOehlman',
  port: 6999398,
  path: ''
}));