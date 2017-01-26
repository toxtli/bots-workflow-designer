/* jshint node: true */
'use strict';

module.exports = function(parts) {
  return 'https://' + parts.hostname + '.googlecode.com/' +
    parts.path.replace(/^\//, '');
};