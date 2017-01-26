var reSplit = /[\,\s]\s*/;

module.exports = function(rigger, requested) {
    // split the requested shims
    var lines = requested.split(reSplit).map(function(shim) {
        return '//= github://buildjs/shims/' + shim.replace('.', '/').toLowerCase() + '.js';
    });
    
    this.done(null, lines.join('\n'));
};