/* jshint node: true */
'use strict';

/**
  ### Github Includes (github://)

  ```js
  getit('github://DamonOehlman/getit/index.js', function(err, data) {
  });
  ```
**/
module.exports = function(parts) {
  var pathParts = parts.path.replace(/^\//, '').split('/');

  return 'https://raw.githubusercontent.com/' + parts.hostname + '/' +
    pathParts[0] + '/master/' + pathParts.slice(1).join('/');
};
