/* jshint node: true */
'use strict';

var regexes = require('./regexes');
var reAlias = regexes.alias;

/**
  ### expand(input, aliases)

  The expand function is used to locate aliases within the given input string
  and return their expanded equivalents.
**/
var expand = exports.expand = function(input, aliases) {
  var match = reAlias.exec(input);
  var base;

  // ensure we have an aliases object
  aliases = aliases || {};

  // if the target is an aliases, then construct into an actual target
  if (match) {
    /*
    // if the alias is not valid, then fire the invalid alias event
    if (! aliases[match[1]]) {
        this.emit('alias:invalid', match[1]);
    }
    */

    // update the base reference
    base = (aliases[match[1]] || '').replace(regexes.trailingSlash, '');

    // update the target, recursively expand
    input = expand(
      base + '/' + match[2].replace(regexes.leadingSlash, ''),
      aliases
    );
    // debug('found alias, ' + match[1] + ' expanding target to: ' + target);
  }

  return input;
};