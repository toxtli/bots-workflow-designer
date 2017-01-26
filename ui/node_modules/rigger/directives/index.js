var async = require('async'),
    debug = require('debug')('rigger'),
    _ = require('underscore'),
    reCommentInclude = /^(.*)?\=(.*)$/,
    actionDirectives = {
        'include': {
            pre:  ['INC'],
            post: ['EOI']
        }
    },
    trailingComments = {
        '/*': ' */'
    };

exports.decode = function(input) {
    var args = Array.prototype.slice.call(arguments, 1);
    
    require('./' + directive.toLowerCase()).decode.apply(null, args);
};

exports.wrap = function(rigger, output, matchData, sourceLine, callback) {
    var action = matchData[2],
        directives = actionDirectives[action],
        allDirectives = (directives.pre || []).concat(directives.post || []),
        commentLeader = matchData[0].replace(reCommentInclude, '$1'),
        commentTrailer = trailingComments[commentLeader] || '';
    
    // if we don't have directives, then trigger the callback joining the lines
    if (! directives) return callback(null, output.join(rigger.lineEnding));
    
    // run the directives
    async.map(
        allDirectives,
        function(code, itemCallback) {
            var encoder = require('./' + code.toLowerCase()).encode;
            
            // if we have no encoder, then proceed to the next item
            if (! encoder) return itemCallback(null, { code: code });
            
            // trigger the encoder, and pass on the result
            encoder(rigger, matchData, sourceLine, function(err, data) {
                itemCallback(err, err ? null : _.defaults(data, { code: code }));
            });
        },
        function(err, results) {
            if (err) return callback(err);
            
            // iterate through the results and format appropriately
            _.filter(results, _.identity).forEach(function(result) {
                var directive = result.code.toUpperCase(),
                    isPre = (directives.pre || []).indexOf(result.code) >= 0,
                    arrayTweak = Array.prototype[isPre ? 'unshift' : 'push'];
                    
                // remove the directive from the result
                delete result.code;
                
                // add the directive line
                arrayTweak.call(
                    output, 
                    commentLeader + ' ' + directive + '>>> ' +
                        JSON.stringify(result) + commentTrailer
                );
            });
            
            // return the output
            callback(null, output.join(rigger.lineEnding));
        }
    );
};