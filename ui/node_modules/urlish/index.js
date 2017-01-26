/* jshint node: true */
'use strict';

var reUrl = /^(\w+)\:\/\/([^\/\:]*)(\:\d+)?(\/?.*)$/;

/**
  # urlish

  This is a simple module that parses an input string to determine if it
  matches with a typical url syntax.  This is not a strict URL parser, and if
  that behaviour is desired I would recommend looking at the core node
  [url](http://nodejs.org/api/url.html) module.

  This module was written to satisfy the use case of
  [getit](https://github.com/DamonOehlman/getit) where url-like syntaxes
  are used.

  ## So what is URLish?

  In very simple terms we are looking for something that matches the
  following format:

  ```
  [scheme]://[hostname](:[port])?(/[path])?
  ```

  At this stage, things like usernames and passwords are not looked at
  and no querystring or hash parsing is attempted either.

  ## Example Usage

  The following demonstrates the usage of `urlish` within the context
  of the `getit` module:

  <<< examples/gist.js

  In the case above, you will notice that the hostname component is not
  automatically lowercased as it is using the `url.parse` function. This is
  useful when working with getit as we are using the host component to map
  to a part of a real url that is case-sensitive.

**/
module.exports = function(input, opts) {
  var match = reUrl.exec(input);

  // if we didn't get a match, return false
  if (! match) {
    return false;
  }

  // otherwise, split the url into the component parts
  return {
    scheme: match[1],
    hostname: match[2],
    port: (match[3] && parseInt(match[3].slice(1), 10)) || 80,
    path: match[4]
  };
};