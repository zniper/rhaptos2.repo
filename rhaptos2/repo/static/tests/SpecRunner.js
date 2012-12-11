require(['jquery', 'underscore', 'jasmine-html', 'mustache', 'atc/templates', 'tagit', 'jquery-ui', 'jasmine-ajax'], function($, _, jasmine, Mustache, Templates){

  // ATC Doesn't use requirejs yet and so needs global variables to many of the packages.
  window.$ = window.jQuery = $;
  window._ = _;
  window.Mustache = Mustache;
  window.Templates = Templates;

  var jasmineEnv = jasmine.getEnv();
  jasmineEnv.updateInterval = 1000;

  var htmlReporter = new jasmine.HtmlReporter();

  jasmineEnv.addReporter(htmlReporter);

  jasmineEnv.specFilter = function(spec) {
    return htmlReporter.specFilter(spec);
  };

  var specs = [];

  specs.push('spec/RolesSpec');

  $(function(){
    require(specs, function(){
      jasmineEnv.execute();
    });
  });

});
