var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    inputPath = path.resolve(__dirname, 'input-plugins'),
    outputPath = path.resolve(__dirname, 'output'),
    riggerOpts = {
        encoding: 'utf8'
    },
    files = fs.readdirSync(inputPath);
    
function rigAndCompare(file, done) {
    fs.stat(path.join(inputPath, file), function(err, stats) {
        // skip directories
        if (stats.isDirectory()) {
            done();
            return;
        }
        
        // read the output file
        fs.readFile(path.join(outputPath, file), 'utf8', function(refErr, reference) {
            assert.ifError(refErr);

            rigger(path.join(inputPath, file), riggerOpts, function(parseErr, parsed) {
                assert.ifError(parseErr);
                assert.equal(parsed, reference);

                done(parseErr);
            });
        });
    });
}

// run tests for each of the input files
describe('local rigging (via plugins) tests', function() {
    // create a test for each of the input files
    (files || []).forEach(function(file) {
        it('should be able to rig: ' + file, rigAndCompare.bind(null, file));
    });

    // run the tests in parallel
    it('should be able to rig all local files in parallel', function(done) {
        async.forEach(files, rigAndCompare, done);
    });
});