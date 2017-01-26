var assert = require('assert'),
    getit = require('../'),
    testContent;
    
describe('gcode scheme test', function() {
    before(function(done) {
        getit('https://leveldb.googlecode.com/git/README', function(err, content) {
            testContent = content;
            done(err);
        });
    });
    
    it('should be able to download a file using the gcode scheme', function(done) {
        getit('gcode://leveldb/git/README', function(err, content) {
            assert.ifError(err);
            assert.equal(content, testContent);
            
            done(err);
        });
    });
});