/**
  ## Custom URL Schemes

  Getit supports a number of custom url schemes to help you type less
  characters:

  ### Contributing URL Schemes

  The task of the scheme translator is to convert a url of the custom scheme
  into a standard URI that can be passed to the GET.

  To create your own scheme translator simply fork the library,
  decide on the scheme / protocol prefix (e.g. github, flickr, etc) and
  then create the relevant translator in the `lib/schemes` directory. 
  When `getit` encounters a request for a url matching your custom scheme
  translator will be required and involved before actually requesting the url.

  Simple.
**/