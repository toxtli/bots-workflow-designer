var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    inputPath = path.resolve(__dirname, 'input-remote'),
    outputPath = path.resolve(__dirname, 'output'),
    reIgnoreFiles = /^DS_Store/i,

    // load the test files
    files = fs.readdirSync(inputPath).filter(function(file) {
        return !reIgnoreFiles.test(file);
    });

function rigAndCompare(file, done) {
    // read the output file
    fs.readFile(path.join(outputPath, file), 'utf8', function(refErr, reference) {
        assert.ifError(refErr);

        rigger(path.join(inputPath, file), function(parseErr, parsed) {
            assert.ifError(parseErr);
            assert.equal(parsed, reference);
        
            done(parseErr);
        });
    });
}

// run tests for each of the input files
describe('remote rigging tests', function() {
    // create a test for each of the input files
    (files || []).forEach(function(file) {
        it('should be able to rig: ' + file, rigAndCompare.bind(null, file));
    });

    it('should be able to rig all local files in parallel', function(done) {
        async.forEach(files, rigAndCompare, done);
    });
});