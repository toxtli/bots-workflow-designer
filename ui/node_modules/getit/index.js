/* jshint node: true */
'use strict';

var debug = require('debug')('getit');
var fs = require('fs');
var path = require('path');
var request = require('hyperquest');
var urlish = require('urlish');

// regexes
var reRemote = /^\w[\w\.\+\-]+\:\/\//;
var reStatusCached = /^304$/;
var reStatusOK = /^(2|3)\d+/;
    
// cache helpers
var cache = require('./cache');

/**
  # getit

  This is a simple remote file loader that makes it easy to open both local 
  and remote files in a simple (and consistent) way.  Behind the scenes getit
  uses [hyperquest](https://github.com/substack/hyperquest) module to to the
  heavy lifting.

  ## Example Usage

  Getting a file:

  ```js
  getit('files/test.txt', function(err, data) {
      
  });
  ```

  Getting some online content:

  ```js
  getit('http://www.google.com/', function(err, data) {
      
  });
  ```

  ### Specifying the Current Working Directory

  By default, all files are resolved to the current working directory through 
  using `path.resolve`. The default directory resolved against can be
  overriden, however, by passing options to the `getit` function call:

  ```js
  getit('files/test.txt', { cwd: __dirname }, function(err, data) {
      
  });
  ```

  Specifying the `cwd` option has no effect on remote requests, but there 
  might be other options added in time to tweak the default
  hyperquest behaviour eventually.  The general principle is you should be 
  able to use `getit` to get the content of both local and remote resources
  without having to dramatically change the way you use the library.

  ## GetIt Options

  The `getit` function supports a second argument for providing options to
  change the default getit behaviour.  

  ### Caching use `cachePath`

  If you provide an optional `cachePath`, then getit will cache a copy of 
  the data retrieved in the specified path.  In addition to the data
  retrieved, an [etag](http://en.wikipedia.org/wiki/HTTP_ETag) value will
  be stored in a lookup file.  This will be used in subsequent lookups
  using the `If-None-Match` header.

  By default, caching will only occur on a server that provides an etag
  value, but this can be overridden by also setting the `cacheAny`
  option to true.

  ```js
  var opts = {
    cachePath: '/tmp'
  };

  getit(
    'github://DamonOehlman/getit/test/files/test.txt',
    opts,
    function(err, data) {
      
    }
  );
  ```

  Finally, if you would prefer not to wait around for a HTTP request and
  a `304` response, then you can provide the `preferLocal` option always
  used the cached copy of a file if it exists in the cache folder.

  ### Aggressive caching with `preferLocal`

  If you __really__ want to avoid a round-trip to web servers to check the
  freshness of the cache, then it might be worth using the `preferLocal`
  option also.  This instructs getit to skip the `etag` check if it finds
  the required file in the cache directory.

  If you do decide to implement this functionality, it's recommended that
  you provide some option in your application to allow users to clear the
  local cache path.

**/
    
var getit = module.exports = function(target, opts, callback) {
  var targetUrl;
  var requestOpts;

  // check for options being omitted
  if (typeof opts == 'function') {
    callback = opts;
    opts = {};
  }
  
  // initialise opts
  opts = opts || {};
  opts.cwd = opts.cwd || process.cwd();

  // if not a remote url, then get local
  if (! isRemote(target)) {
    return getLocal(target, opts, callback);
  }

  // get the target url
  targetUrl = getUrl(target);

  // initialise the request opts
  requestOpts = {
    method: 'GET',
    uri: targetUrl
  };

  // if we don't have a callback, return a request stream
  if (! callback) {
    debug('creating stream for retrieving: ' + targetUrl);
    return request(requestOpts);
  }

  // check the cache
  cache.get(target, opts, function(cacheData) {
    // if we have cache data then add the if-none-match header
    if (cacheData.etag) {
      requestOpts.headers = {
        'If-None-Match': cacheData.etag
      };
    }

    // if we have cache data and prefer local is set, then return that data
    if (opts.preferLocal && cacheData.data) {
      return callback(null, cacheData.data);
    }

    debug('requesting resource: ' + targetUrl +', for target: ' + target);
    request(requestOpts)
      // handle the response
      .on('response', function(res) {
        var body = '';

        debug('received response for target: ' + target);
        // if cached, then return the catched content
        if (reStatusCached.test(res.statusCode)) {
          return callback(null, cacheData.data, true);
        }

        // otherwise, if not ok, then return an error
        if (! reStatusOK.test(res.statusCode)) {
          return callback(new Error(((res.headers || {}).status ||
            'Not found')) + ': ' + targetUrl);
        }

        // otherwise, proceed to download the content
        res.on('data', function(buffer) {
          body += buffer.toString('utf8');
        });

        res.on('end', function() {
          cache.update(target, opts, null, res, body, function() {
            callback(null, body);
          });
        });
      })
      .on('error', callback);
  });

  return null;
};

var getLocal = getit.local = function(target, opts, callback) {
  var targetFile = path.resolve(opts.cwd, target);

  // if we don't have a callback, return a stream
  if (! callback) {
    return fs.createReadStream(targetFile);
  }

  // if a callback is defined, then read the file using the 
  debug('reading file: ' + targetFile);
  fs.readFile(targetFile, 'utf8', function(err, data) {
    debug('read file: ' + targetFile + ', err: ' + err);

    callback(err, data);
  });
  
  return null;
};

var getUrl = getit.getUrl = function(target) {
  var parts = urlish(target);
  var translator;

  // if we have no parts, just return the target
  if (! parts) {
    return target;
  }
      
  // try and include the scheme translator
  try {
    translator = require('./lib/schemes/' + parts.scheme);
  }
  catch (e) {
    // no translator found, leave the handler blank
  }
  
  // if we have a translator, then use it
  if (translator) {
    target = translator(parts, target);
  }
  
  // return the target
  return target;
};

var isRemote = getit.isRemote = function(target) {
  return reRemote.test(target);
};


getit.getCacheTarget = cache.getTarget;