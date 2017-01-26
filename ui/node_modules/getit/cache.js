/* jshint node: true */
'use strict';

var mkdirp = require('mkdirp');
var path = require('path');
var fs = require('fs');
var reCharset = /^.*charset\=(.*)$/;
var reInvalidCacheChars = /(\:\/+|\/+|\.(?!\w+$))/g;

/**
## getit cache helpers

### cache.get(target, opts, callback)
**/
exports.get = function(target, opts, callback) {
  var cacheData = {};
  var cacheFile;
  var metaFile;

  // if we have no cache folder, then trigger the callback with no data
  if (! opts.cachePath) {
    callback(cacheData);
  }
  // otherwise, look for an etag file
  else {
    cacheFile = path.resolve(opts.cachePath, getCacheTarget(target));
    metaFile = cacheFile + '.meta';
          
    // read the etag file
    fs.readFile(metaFile, 'utf8', function(err, data) {
      var match;
      var encoding;
      
      if (! err) {
        cacheData = JSON.parse(data);
        
        // look for an encoding specification in the metadata
        match = reCharset.exec(cacheData['content-type']);
        encoding = match ? match[1] : 'utf8';
        
        fs.readFile(cacheFile, encoding, function(err, data) {
          if (! err) {
            cacheData.data = data;
          }
          
          callback(cacheData);
        });
      }
      else {
        callback(cacheData);
      }
    });
  }
};

/**
### cache.update(target, opts, resErr, res, body, callback)
**/
exports.update = function(target, opts, resErr, res, body, callback) {
  var cacheFile;
  var meta;
  var cacheable = opts.cachePath && (! resErr) && res.headers &&
      (opts.cacheAny || res.headers.etag);

  // if not cacheable return
  if (! cacheable) {
    return callback();
  }

  // initialise the cache filename and metafile
  cacheFile = path.resolve(opts.cachePath, getCacheTarget(target));
  meta = cacheFile + '.meta';
  
  // do the caching thing
  mkdirp(opts.cachePath, function(err) {
    if (err) {
      return callback(err);
    }

    // create the metadata file
    fs.writeFile(meta, JSON.stringify(res.headers), 'utf8', function() {
      var match = reCharset.exec(res.headers['content-type']);
      var encoding = match ? match[1] : 'utf8';
      
      fs.writeFile(cacheFile, body, encoding, function() {
        callback();
      });
    });
  });
};

/* internals */

var getCacheTarget = exports.getTarget = function(target) {
  return target.replace(reInvalidCacheChars, '-');
};