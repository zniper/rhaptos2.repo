/* Configure paths to all the JS libs */
require.config({
  baseUrl: "./",
  //urlArgs: 'cb=' + Math.random(), // Cache Buster
  paths: {
    jquery: '../js/lib/jquery-1.8.3',
    'jquery-ui': '../js/lib/jqueryui-1.9.2',
    'jquery-mockjax': '../js/lib/jquery.mockjax',

    bootstrap: '../js/lib/bootstrap',
    underscore: '../js/lib/underscore-1.4.3',
    mustache: '../js/lib/mustache',
    tagit: '../js/lib/tagit',
    spin: '../js/lib/spin',
    spec: 'spec',
    'atc/lang': '../js/languagelib',
    'atc/client': '../authortools_client',
    'atc/templates': '../authortools_client_templates',
    'atc/tools': '../authortools_client_tools'
  },
  shim: {
    bootstrap: {
      deps: ['jquery'],
      exports: 'jquery'
    },
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
    'jquery-mockjax': {
      deps: ['jquery'],
      exports: 'jquery'
    },
    'mustache': {
      exports: 'Mustache'
    },
    'tagit': {
      deps: ['jquery']
    },

    'atc/client': {
      deps: ['jquery'],
    },
    'atc/lang': {
      exports: 'Language'
    },
    'atc/templates': {
      exports: 'Templates'
    },
    'atc/tools': {
      deps: ['jquery', 'atc/lang', 'spin', 'atc/client', 'atc/templates', 'tagit'],
      exports: 'Tools'
    }
  }
});
