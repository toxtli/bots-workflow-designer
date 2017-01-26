/* jshint node: true */
'use strict';

/**
  ### regexes

**/

var regexes = module.exports = {
  lineBreak: /\r?\n/,
  trailingReturn: /\r$/,
  leadingDot: /^\./,
  trailingDot: /\.$/,
  leadingSlash: /^\//,
  trailingSlash: /\/$/,

  // a regex that can be used to remove trailing whitespace from a line
  trailingWhitespace: /\s+\r?$/,

  multiTarget: /^(.*?)\[(.*)\]$/,

  // alias definitions: blah!optional-trailing-section
  alias: /^([\w\-]+)\!(.*)$/,

  // js single line include //=
  includeDoubleSlash: /^(\s*)\/\/\=(\w*)\s*([^=]*)$/,

  // css, js multiline include /*=  */
  includeSlashStar: /^(\s*)\/\*\=(\w*)\s*(.*?)\s*\*\/$/,

  // coffeescript single line include #=
  includeHash: /^(\s*)\#\=(\w*)\s*(.*)$/,

  // leading and trailing quote capture
  quotesLeadAndTrail: /(^[\"\']|[\"\']$)/g,

  fallbackDelim: /\s+\:\s+/
};

// specify the include regexes
// these regexes specify the include patterns that are supported for different
// types of files
regexes.includes = {
  // core supported file types
  js:     [ regexes.includeDoubleSlash, regexes.includeSlashStar ],
  css:    [ regexes.includeSlashStar ],

  // other cool languages that I use every now and again
  coffee: [ regexes.includeHash ],
  roy:    [ regexes.includeDoubleSlash ],
  styl:   [ regexes.includeDoubleSlash ]
};
