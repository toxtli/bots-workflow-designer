var _ = require('underscore');

exports.encode = function(rigger, matchData, sourceLine, callback) {
    callback(null, {
        filename: matchData[3],
        start: sourceLine
    });
};

exports.decode = function(text) {
};