# buildjs.core

This library is a set of core settings and utilities that are shared across
the BuildJS tools.  The library is made up of a number of modules that can
be accessed by using `require('buildjs.core/modulename')`.


[![NPM](https://nodei.co/npm/buildjs.core.png)](https://nodei.co/npm/buildjs.core/)

[![stable](https://img.shields.io/badge/stability-stable-green.svg)](https://github.com/badges/stability-badges) [![Build Status](https://img.shields.io/travis/buildjs/core.svg?branch=master)](https://travis-ci.org/buildjs/core) 

## Components

The list of modules and their purpose is outlined below:

- `buildjs.core/regexes`

  Regular expressions that are used within the BuildJS tools.  Prior to the
  creation of this core library there was a lot of repitition (and opportunity
  for error) with regular expressions in each of the modules.

- `buildjs.core/formatters`

  General formatting helpers (strip trailing whitespace, etc)

- `buildjs.core/aliases`

  Helper tools for dealing with BuildJS aliases.

- `buildjs.core/platform`

  Platform aware settings and helpers.

## Reference

### expand(input, aliases)

The expand function is used to locate aliases within the given input string
and return their expanded equivalents.

### formatters

Formatting helper functions.

#### stripTrailingWhitespace(line)

#### normalizeExt(ext)

### regexes

## License(s)

### MIT

Copyright (c) 2014 Damon Oehlman <damon.oehlman@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
