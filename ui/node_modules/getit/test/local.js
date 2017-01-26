var assert = require('assert'),
    fs = require('fs'),
    path = require('path'),
    getit = require('../'),
    testfile = path.resolve(__dirname, 'test.txt'),
    testContent,
    opts = {
        cwd: __dirname
    };

describe('streamed download test', function() {
    before(function(done) {
        fs.readFile(path.resolve(__dirname, 'files/test.txt'), 'utf8', function(err, data) {
            if (! err) {
                testContent = data;
            }

            done(err);
        });
    });
    
    it('should be able to get a local file', function(done) {
      getit('files/test.txt', opts, function(err, data) {
        assert.ifError(err);
        assert.equal(data, testContent);
  
        done();
      });
    });
});