# Configure paths to all the JS libs
require.config
  baseUrl: './'

  # If set to true, an error will be thrown if a script loads that does not call define() or have a shim exports string value that can be checked. See Catching load failures in IE for more information.
  enforceDefine: true

  #urlArgs: "cb=#{Math.random()}" # Cache Buster
  paths:
    jquery: '../js/lib/jquery-1.8.3'
    'jquery-ui': '../js/lib/jqueryui-1.9.2'
    'jquery-mockjax': '../js/lib/jquery.mockjax'
    bootstrap: '../js/lib/bootstrap'
    underscore: '../js/lib/underscore-1.4.3'
    backbone: '../js/lib/backbone-0.9.2'
    jasmine: '../js/lib/jasmine'
    'jasmine-html': '../js/lib/jasmine-html'
    'jasmine-ajax': '../js/lib/jasmine-ajax'
    mustache: '../js/lib/mustache'
    tagit: '../js/lib/tagit'
    spin: '../js/lib/spin'
    spec: 'spec'
    'model/tools': '../model/tools'
    'atc/lang': '../js/languagelib'
    'atc/client': '../authortools_client'
    'atc/templates': '../authortools_client_templates'
    'atc/tools': '../authortools_client_tools'
    'mockjax-routes': 'mockjax-routes'

  shim:
    jquery:
      exports: 'jQuery'
      # init: -> this.jQuery.noConflict(true)
    bootstrap:
      deps: ['jquery']
      exports: 'jQuery'

    underscore:
      exports: '_'

    backbone:
      deps: ['underscore', 'jquery']
      exports: 'Backbone'
      init: ->
        ret = @Backbone
        delete @Backbone
        ret

    jasmine:
      exports: 'jasmine'

    'jasmine-html':
      deps: ['jasmine']
      exports: 'jasmine'

    'jasmine-ajax':
      deps: ['jasmine']
      exports: 'jasmine'

    'jquery-mockjax':
      deps: ['jquery']
      exports: 'jQuery'

    mustache:
      exports: 'Mustache'

    'jquery-ui':
      deps: ['jquery']
      exports: 'jQuery'

    tagit:
      deps: ['jquery-ui']
      exports: 'jQuery'

    'atc/client':
      deps: ['jquery']
      exports: 'jQuery'

    'atc/lang':
      exports: 'Language'

    'atc/templates':
      exports: 'Templates'

    'atc/tools':
      deps: ['jquery', 'atc/lang', 'spin', 'atc/client', 'atc/templates', 'bootstrap', 'tagit']
      exports: 'Tools'

    'mockjax-routes':
      deps: ['jquery']
      init: -> true

# requirejs special-cases jQuery and allows it to be a global (doesn't call the init code below to clean up the global vars)
# To stop it from doing that, we need to delete this property
#
# unlike the other jQuery plugins bootstrap depends on a global '$' instead of 'jQuery'
#delete define.amd.jQuery
