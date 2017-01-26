var debug = require('debug')('rigger:coffeescript');
var converters = require('./');
var _ = require('underscore');

module.exports = function(input, opts, callback) {
    opts = _.extend({}, this.opts, opts);

    converters
        .require('coffee-script')
        .on('error', callback)
        .on('ok', function(coffee) {
            debug('running coffeescript with opts: ', opts);
            callback(null, coffee.compile(input, opts));
        });
};
