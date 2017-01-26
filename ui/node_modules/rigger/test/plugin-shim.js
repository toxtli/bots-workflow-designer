var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    getit = require('getit');

describe('shim plugin tests', function() {
    it('it should convert a single shim request into a single include', function(done) {
        rigger.process('//=shim Array.indexOf', function(err, output) {
            assert.ifError(err);
            
            getit('github://buildjs/shims/array/indexof.js', function(err, reference) {
                assert.ifError(err, 'Could not retrieve reference sample from github');
                assert.equal(output, reference);
                
                done();
            });
        });
    });
    
    it('should be able to convert space delimited shim requests into concatenated includes', function(done) {
        rigger.process('//=shim Array.indexOf String.trim', function(err, output) {
            var referenceFiles = [
                'github://buildjs/shims/array/indexof.js',
                'github://buildjs/shims/string/trim.js'
            ];
            
            assert.ifError(err);
            async.map(referenceFiles, getit, function(err, results) {
                assert.ifError(err, 'Could not retrieve reference samples from github');

                assert.equal(output, results.join('\n'));
                done();
            });
        });
    });
});