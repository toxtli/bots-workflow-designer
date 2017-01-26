var async = require('async'),
    rigger = require('./'),
    path = require('path'),
    fs = require('fs'),
    basePath = path.resolve(__dirname, 'src'),
    mkdirp = require('mkdirp'),
    outputPath = path.resolve(__dirname),
    finder = require('findit').find(basePath),
    files = [];
    
function jsOnly(filename) {
    return path.extname(filename).slice(1).toLowerCase() === 'js';
}
    
finder.on('file', function(file, stat) {
    files.push(file);
});

finder.on('end', function() {
    async.forEach(
        files.filter(jsOnly),
        function(file, itemCallback) {
            var targetPath = path.resolve(outputPath, file.slice(basePath.length + 1));
            
            console.log('rigging: ' + file);
            
            rigger(
                file,
                { output: path.resolve(__dirname) },
                function(err, content) {
                    console.log('writing: ' + targetPath);
                    mkdirp(path.dirname(targetPath), function(err) {
                        fs.writeFile(targetPath, content, 'utf8', itemCallback);
                    });
                }
            );
        },
        
        function(err) {
            console.log('done', err);
        }
    );
});