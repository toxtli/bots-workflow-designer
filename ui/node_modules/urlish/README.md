# urlish

This is a simple module that parses an input string to determine if it
matches with a typical url syntax.  This is not a strict URL parser, and if
that behaviour is desired I would recommend looking at the core node
[url](http://nodejs.org/api/url.html) module.

This module was written to satisfy the use case of
[getit](https://github.com/DamonOehlman/getit) where url-like syntaxes
are used.


[![NPM](https://nodei.co/npm/urlish.png)](https://nodei.co/npm/urlish/)

[![Build Status](https://drone.io/bitbucket.org/DamonOehlman/urlish/status.png)](https://drone.io/bitbucket.org/DamonOehlman/urlish/latest)

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

```
ERROR: could not find: 
```

In the case above, you will notice that the hostname component is not
automatically lowercased as it is using the `url.parse` function. This is
useful when working with getit as we are using the host component to map
to a part of a real url that is case-sensitive.

## License(s)

### MIT

Copyright (c) 2013 Damon Oehlman <damon.oehlman@gmail.com>

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
