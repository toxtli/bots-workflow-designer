/* jshint node: true */
'use strict';

var debug = require('debug')('getit-gist');

/**
  ### Github Gists (gist://)

  To get the default file (first file) from a particular gist:

  ```js
  getit('gist://DamonOehlman:6999398', function(err, content) {
  });
  ```

  To get a specific file from a particular gist:

  ```js
  getit('gist://DamonOehlman:6877717/index.js', function(err, content) {
  });
  ```

  __NOTE:__ Github recently changed the way gist raw urls were formatted
  which has meant a change is needed in the getit format.  You must now also
  include the username of the owner of the gist when requesting the file
  as shown in the examples above.

**/
module.exports = function(parts, original) {
  var endpoint;
  
  debug('running gist scheme remapper on: ' + original, parts);
  
  // map the endpoint to the gist first of all
  endpoint = 'https://gist.githubusercontent.com/' + parts.hostname + '/' + parts.port + '/raw';
  // 'https://raw.github.com/gist/' + parts.host;
  
  // if a pathname has been extracted from the original url, then append
  // that to the request
  if (parts.path) {
    endpoint += '/' + parts.path.replace(/^\//, '');
  }

  return endpoint;
};