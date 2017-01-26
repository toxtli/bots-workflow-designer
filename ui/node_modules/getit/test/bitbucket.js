var assert = require('assert'),
    fs = require('fs'),
    getit = require('..'),
    path = require('path'),
    testfile = path.resolve(__dirname, 'test.txt'),
    testContent,
    opts = {
        cwd: __dirname
    };
    
describe('bitbucket scheme test', function() {
    before(function(done) {
        getit('https://bitbucket.org/puffnfresh/roy/raw/master/README.md', function(err, content) {
            testContent = content;
            done(err);
        });
    });
    
    it('should be able to download a file using the bitbucket scheme', function(done) {
        getit('bitbucket://puffnfresh/roy/README.md', function(err, content) {
            assert.ifError(err);
            assert.equal(content, testContent);
            
            done(err);
        });
    });
});