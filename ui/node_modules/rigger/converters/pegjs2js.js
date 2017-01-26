var debug = require('debug')('rigger-pegjs'),
    path = require('path'),
    converters = require('./');

module.exports = function(input, opts, callback) {
    var rigger = this;
    
    converters
        .require('pegjs')
        .on('error', callback)
        .on('ok', function(PEG) {
            // create the parser
            var output = PEG.buildParser(input, {
                    output: 'source'
                }),
                basename;
                
            // if we have a current file that we are converting, then 
            // derive the basename from that file
            if (opts.filename) {
                basename = path.basename(opts.filename, path.extname(opts.filename));
            }
            
            // fallback to the rigger basename or just parser
            basename = basename || rigger.basename || 'parser';
            
            // fire the callback
            callback(null, 'var ' + basename + ' = ' + output + ';', opts);
        });
};