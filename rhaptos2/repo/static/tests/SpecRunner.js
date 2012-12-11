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


/* Configure paths to all the JS libs */
require.config({
  baseUrl: "./",
  //urlArgs: 'cb=' + Math.random(), // Cache Buster
  paths: {
    jquery: '../js/lib/jquery-1.8.3',
    'jquery-ui': '../js/lib/jqueryui-1.9.2',
    underscore: '../js/lib/underscore-1.4.3',
    backbone: '../js/lib/backbone-0.9.2',
    //'backbone.localStorage': 'lib/backbone.localStorage',
    jasmine: '../js/lib/jasmine',
    'jasmine-html': '../js/lib/jasmine-html',
    'jasmine-ajax': '../js/lib/jasmine-ajax',
    mustache: '../js/lib/mustache',
    tagit: '../js/lib/tagit',
    spec: 'spec',
    'atc/lang': '../js/languagelib',
    'atc/templates': '../authortools_client_templates',
    'atc/tools': '../authortools_client_tools'
  },
  shim: {
    underscore: {
      exports: "_"
    },
    backbone: {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    jasmine: {
      exports: 'jasmine'
    },
    'jasmine-html': {
      deps: ['jasmine'],
      exports: 'jasmine'
    },
    'jasmine-ajax': {
      deps: ['jasmine'],
      exports: 'jasmine'
    },
    'mustache': {
      exports: 'Mustache'
    },
    'tagit': {
      deps: ['jquery']
    },

    'atc/lang': {
      exports: 'Language'
    },
    'atc/templates': {
      exports: 'Templates'
    },
    'atc/tools': {
      deps: ['jquery', 'atc/lang'],
      exports: 'Tools'
    }
  }
});
