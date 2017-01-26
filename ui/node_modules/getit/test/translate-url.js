var assert = require('assert'),
    getit = require('../'),
    checks = {
        http: {
            before: 'http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
            after: 'http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js'
        },
        
        github: {
            before: 'github://DamonOehlman/getit/index.js',
            after: 'https://raw.github.com/damonoehlman/getit/master/index.js'
        }
    };
    
function check(section) {
    assert(getit.getUrl(section.before), section.after);
}

describe('url translation tests', function() {
    it('should leave a http url as is', function() {
        check(checks.http);
    });
    
    it('should be able to translate a github:// url', function() {
        check(checks.github);
    });
});