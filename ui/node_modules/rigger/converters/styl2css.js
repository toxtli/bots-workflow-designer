var debug = require('debug')('rigger'),
    path = require('path'),
    converters = require('./'),
    _ = require('underscore');

module.exports = function(input, opts, callback) {
    var opts, renderer;

    // initialise the stylus opts, specifying the paths as the rigger cwd
    opts = _.extend((this.opts || {}).stylus || {}, {
        paths: [ this.opts.cwd ]
    });
    
    converters
        .require('stylus')
        .on('error', callback)
        .on('ok', function(stylus) {
            // create the renderer
            renderer = stylus(input, opts);
            
            // iterate through any plugins and use them
            (opts.plugins || []).forEach(function(plugin) {
                debug('loaded plugin: ', plugin);
                renderer.use(plugin(opts));
            });
            
            // render stylus (pass through opts)
            debug('running stylus conversion, opts = ', opts);
            renderer.render(function(err, data) {
                callback(err, data, opts);
            });
        });
};