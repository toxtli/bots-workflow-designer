/* jshint node: true */
'use strict';

/**
  ### platform

  The platform module provides platform aware settings and tools for working
  with source files.
*/

exports.lineEnding = (process.platform == 'win32' ? '\r\n' : '\n');
