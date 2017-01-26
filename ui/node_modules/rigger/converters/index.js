var events = require('events'),
    path = require('path'),
    _ = require('underscore');

function requireLocal(target) {
    var searchModules = require('module')._nodeModulePaths('.').map(function(modPath) {
            return path.join(modPath, target);
        });
    
    return [target].concat(searchModules).reduce(function(memo, targetPath) {
        // attempt to include the module
        try {
            return memo || require(targetPath);
        }
        catch (e) {
            return null;
        }
    }, null);
}

exports.require = function() {
    var emitter = new events.EventEmitter(),
        args = Array.prototype.slice.call(arguments),
        modules;
      
    process.nextTick(function() {
        var mods = args.map(requireLocal),
            missingMods = _.reject(mods, _.identity);
            
        if (missingMods.length > 0) {
            emitter.emit('error', new Error('Unable to load modules: ' + missingMods.toString()));
        }
        else {
            emitter.emit.apply(emitter, ['ok'].concat(mods));
        }
    });
    
    return emitter;
};