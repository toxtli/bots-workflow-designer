var assert = require('assert'),
    getit = require('../'),
    snippet1, snippet2;

describe('gist scheme test', function() {
    before(function(done) {
        getit('https://gist.githubusercontent.com/DamonOehlman/6999398/raw', function(err, content) {
            snippet1 = content;
            done(err);
        });
    });
    
    before(function(done) {
        getit('https://gist.githubusercontent.com/DamonOehlman/6877717/raw/index.js', function(err, content) {
            snippet2 = content;
            done(err);
        });
    });

    it('should get the first file by gist id only', function(done) {
        getit('gist://DamonOehlman:6999398', function(err, content) {
            assert.ifError(err);
            assert.equal(content, snippet1);

            done(err);
        });
    });
    
    it('should get a specified file when specified', function(done) {
        getit('gist://DamonOehlman:6999398/Makefile', function(err, content) {
            assert.ifError(err);
            assert.equal(content, snippet1);
        
            done(err);
        });
    });
    
    it('should error when a non-existant file is requested', function(done) {
        getit('gist://DamonOehlman:6999398/test.js', function(err, content) {
            assert(err);
            done();
        });
    });
    
    it('should get a specified file when the gist has more than one file', function(done) {
        getit('gist://DamonOehlman:6877717/index.js', function(err, content) {
            assert.ifError(err);
            assert.equal(content, snippet2);
            
            done();
        });
    });
});