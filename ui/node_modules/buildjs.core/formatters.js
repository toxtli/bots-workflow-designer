/* jshint node: true */
'use strict';

var regexes = require('./regexes');
var reTrailingWhitespace = regexes.trailingWhitespace;

/**
  ### formatters

  Formatting helper functions.
**/

/**
  #### stripTrailingWhitespace(line)
**/
exports.stripTrailingWhitespace = function(line) {
  return line.replace(reTrailingWhitespace, '');
};

/**
  #### normalizeExt(ext)
**/
exports.normalizeExt = function(ext) {
  return (ext || '').replace(regexes.leadingDot, '').toLowerCase();
};
