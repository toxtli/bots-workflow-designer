var assert = require('assert'),
    async = require('async'),
    debug = require('debug')('transpile'),
    rigger = require('..'),
    fs = require('fs'),
    path = require('path'),
    _ = require('underscore'),
    inputPath = path.resolve(__dirname, 'input-transpile'),
    outputPath = path.resolve(__dirname, 'output'),
    riggerOpts = {
        encoding: 'utf8',
        stylus: {
            plugins: [ require('nib') ]
        }
    },
    targetContext = {
        js: '.js',
        coffee: '.js',
        roy: '.js',
        styl: '.css',
        pegjs: '.js'
    },
    
    reIgnoreFiles = /^.DS_Store/i,
    isIncluded = function(file) {
        return !reIgnoreFiles.test(file);
    },
    
    // find the files to read
    files = fs.readdirSync(inputPath).filter(isIncluded);
    
function rigAndCompare(file, done) {
    debug('processing input: ' + file);

    fs.stat(path.join(inputPath, file), function(err, stats) {
        var targetExt = targetContext[path.extname(file).slice(1)] || path.extname(file),
            extname = path.extname(file),
            outputFile;
        
        // skip directories
        if (stats.isDirectory()) {
            done();
            return;
        }
        
        // initialise the output filename
        outputFile = path.join(outputPath, path.basename(file, extname)) + targetExt;
        
        // read the output file
        fs.readFile(outputFile, 'utf8', function(refErr, reference) {
            assert.ifError(refErr);

            rigger(
                path.join(inputPath, file), 
                _.extend({}, riggerOpts, { targetType: path.extname(outputFile) }),
                function(parseErr, parsed) {
                    assert.ifError(parseErr);

                    assert.equal(
                        parsed.replace(/\r\n/g, '\n'),
                        reference.replace(/\r\n/g, '\n')
                    );
                    done(parseErr);
                }
            );
        });
    });
}

// run tests for each of the input files
describe('transpiling tests', function() {
    // create a test for each of the input files
    files.forEach(function(file) {
        it('should be able to rig: ' + file, rigAndCompare.bind(null, file));
    });
    
    it('should be able to rig all local files in parallel', function(done) {
        async.forEach(files, rigAndCompare, done);
    });
});