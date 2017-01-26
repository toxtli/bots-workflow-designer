var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    inputPath = path.resolve(__dirname, 'input-errors'),
    targetContext = {
        coffee: '.js',
        styl: '.css'
    },
    files = fs.readdirSync(inputPath);

function rigAndCompare(file, done) {
    var targetExt = targetContext[path.extname(file).slice(1)] || path.extname(file),
        targetPath = path.join(inputPath, file);
    
    fs.stat(targetPath, function(err, stats) {
        if ((! err) && stats.isFile()) {
            rigger(targetPath, { targetType: targetExt }, function(parseErr, parsed) {
                assert(parseErr, 'Did not receive an error when one was expected');
                done();
            });
        }
        else {
            done(err);
        }
    });
}

// run tests for each of the input files
describe('rigger error handling tests', function() {
    
    // create a test for each of the input files
    (files || []).forEach(function(file) {
        it('should produce an error when rigging: ' + file, rigAndCompare.bind(null, file));
    });

    // ensure they can run in parallel
    it('should be able to rig all in parallel', function(done) {
        async.forEach(files, rigAndCompare, done);
    });
});