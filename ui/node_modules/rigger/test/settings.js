var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    inputPath = path.resolve(__dirname, 'input-settings'),
    outputPath = path.resolve(__dirname, 'output'),
    files = fs.readdirSync(inputPath);
    
function notJSON(file) {
    return path.extname(file).toLowerCase() !== '.json';
}

function rigAndCompare(file, done) {
    // open the json datafile
    fs.readFile(path.join(inputPath, path.basename(file, '.js') + '.json'), 'utf8', function(err, content) {
        var comparison = JSON.parse(content);
        
        // read the output file
        rigger(path.join(inputPath, file), { settings: { test: false } }, function(parseErr, parsed, settings) {
            assert.ifError(parseErr);
            assert.deepEqual(settings, comparison);
            
            done(parseErr);
        });
    });
}

// run tests for each of the input files
describe('setting parser tests', function() {
    
    // create a test for each of the input files
    (files || []).filter(notJSON).forEach(function(file) {
        it('should be able to rig: ' + file, rigAndCompare.bind(null, file));
    });

    it('should be able to rig all in parallel', function(done) {
        async.forEach(files.filter(notJSON), rigAndCompare, done);
    });
});