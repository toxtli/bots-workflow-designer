var assert = require('assert'),
    fs = require('fs'),
    path = require('path'),
    getit = require('../'),
    testContent,
    opts = {
        cwd: __dirname
    };
    
describe('local loading test', function() {
    before(function(done) {
        fs.readFile(path.resolve(__dirname, 'files/test.txt'), 'utf8', function(err, data) {
            if (! err) {
                testContent = data;
            }
            
            done(err);
        });
    });
    
    it('should be able to load a local file', function(done) {
        getit('files/test.txt', opts, function(err, data) {
            assert.ifError(err);
            assert.equal(data, testContent);
            done(err);
        });
    });
    
    it('should be able to load a remote file', function(done) {
        getit('github://DamonOehlman/getit/test/files/test.txt', opts, function(err, data) {
            assert.equal(data, testContent);
            done(err);
        });
    });
    
    it('should return an error for a non-existant remote file', function(done) {
        getit('github://DamonOehlman/getit/test/files/test2.txt', opts, function(err, data) {
            assert(err);
            done();
        });
    });
});