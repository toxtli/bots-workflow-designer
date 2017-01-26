/**
  # buildjs.core

  This library is a set of core settings and utilities that are shared across
  the BuildJS tools.  The library is made up of a number of modules that can
  be accessed by using `require('buildjs.core/modulename')`.

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

**/
