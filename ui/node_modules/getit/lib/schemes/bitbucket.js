/* jshint node: true */
'use strict';

module.exports = function(parts) {
  var pathParts = parts.path.replace(/^\//, '').split('/');

  return 'https://bitbucket.org/' + parts.hostname + '/' +
    pathParts[0] + '/raw/master/' + pathParts.slice(1).join('/');
};