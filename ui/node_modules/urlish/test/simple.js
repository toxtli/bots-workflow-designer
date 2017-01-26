var test = require('tape');
var expect = require('./helpers/expect');

test('http://google.com/', expect({
  scheme: 'http',
  hostname: 'google.com',
  port: 80,
  path: '/'
}));

