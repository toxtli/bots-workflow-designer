var assert = require('assert'),
    async = require('async'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    inputPath = path.resolve(__dirname, 'input-variables'),
    outputPath = path.resolve(__dirname, 'output'),
    settings = {
        noincludes: {
            filename: 'noincludes'
        }
    },
    files = fs.readdirSync(inputPath);

function rigAndCompare(file, done) {
    var targetPath = path.join(inputPath, file);
    
    fs.stat(targetPath, function(err, stats) {
        if ((! err) && stats.isFile()) {
            // read the output file
            fs.readFile(path.join(outputPath, file), 'utf8', function(refErr, reference) {
                var testSettings = settings[path.basename(file, '.js')] || {};
                
                assert.ifError(refErr, 'No output file found for test');

                rigger(path.join(inputPath, file), { settings: testSettings }, function(parseErr, parsed) {
                    if (! parseErr) {
                        assert.equal(parsed, reference);
                    }

                    done(parseErr);
                });
            });
        }
        else {
            done(err);
        }
    });
}

describe('variable expansion rigging tests', function() {
    // create a test for each of the input files
    (files || []).forEach(function(file) {
        it('should be able to rig: ' + file, rigAndCompare.bind(null, file));
    });

    it('should be able to rig all local files in parallel', function(done) {
        async.forEach(files, rigAndCompare, done);
    });
});