
// <!--
// Copyright (c) Rice University 2012-3
// This software is subject to
// the provisions of the GNU Affero General
// Public License Version 3 (AGPLv3).
// See LICENCE.txt for details.
// -->


(function() {

  define('SpecRunner', ['jquery', 'jasmine-html'], function(jQuery, jasmine) {
    var htmlReporter, jasmineEnv, specs;
    specs = ['spec/MetadataSpec.js'];
    jasmineEnv = jasmine.getEnv();
    jasmineEnv.updateInterval = 1000;
    htmlReporter = new jasmine.HtmlReporter();
    jasmineEnv.addReporter(htmlReporter);
    jasmineEnv.specFilter = function(spec) {
      return htmlReporter.specFilter(spec);
    };
    return jQuery(function() {
      return require(specs, function() {
        return jasmineEnv.execute();
      });
    });
  });

}).call(this);

